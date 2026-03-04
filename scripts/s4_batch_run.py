
import os
import json
from dotenv import load_dotenv
import requests
from s1_extract_memo import extract_memo
from s2_generate_agent_spec import generate_agent_spec
from s3_apply_patch import apply_patch
load_dotenv()

# ─── PATHS ────────────────────────────────────────────────
TRANSCRIPTS_DIR = "data/transcripts"
OUTPUTS_DIR     = "outputs/accounts"

# ─── TRELLO CONFIG ────────────────────────────────────────
TRELLO_API_KEY  = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN    = os.getenv("TRELLO_TOKEN")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")

# List IDs
LIST_DEMO_RECEIVED = "69a8501783e2bcb896813faf"  # To Do
LIST_V1_GENERATED  = "69a8501783e2bcb896813fb0"  # Doing
LIST_V2_COMPLETE   = "69a8501783e2bcb896813fb1"  # Done


# ─── TRELLO FUNCTIONS ─────────────────────────────────────

def clear_trello_board():
    """Delete all existing cards on the board before fresh run — makes pipeline idempotent."""
    try:
        response = requests.get(
            f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/cards",
            params={"key": TRELLO_API_KEY, "token": TRELLO_TOKEN}
        )
        cards = response.json()
        for card in cards:
            requests.delete(
                f"https://api.trello.com/1/cards/{card['id']}",
                params={"key": TRELLO_API_KEY, "token": TRELLO_TOKEN}
            )
        print(f"[Trello] 🧹 Cleared {len(cards)} existing cards — fresh run starting")
    except Exception as e:
        print(f"[Trello] Warning: Could not clear board: {e}")


def create_trello_card(account_id: str, company: str, version: str, unknowns: list):
    """Create a Trello card when an account is processed."""

    if version == "demo":
        list_id = LIST_DEMO_RECEIVED
        name    = f"📥 {account_id} - Demo Call Received"
        desc    = (
            f"Demo call transcript received.\n"
            f"Account ID: {account_id}\n"
            f"Status: Processing now — extracting memo and generating v1 agent spec."
        )

    elif version == "v1":
        list_id  = LIST_V1_GENERATED
        name     = f"⚙️ {account_id} - {company} - v1 Agent Generated"
        unknown_text = (
            "\n".join(f"  - {q}" for q in unknowns)
            if unknowns
            else "  None — fully configured"
        )
        desc = (
            f"Pipeline A complete for {company}.\n"
            f"Account ID: {account_id}\n"
            f"Version: v1\n\n"
            f"Files generated:\n"
            f"  - outputs/accounts/{account_id}/v1/account_memo.json\n"
            f"  - outputs/accounts/{account_id}/v1/agent_spec.json\n\n"
            f"Open Questions ({len(unknowns)}):\n"
            f"{unknown_text}\n\n"
            f"Status: Awaiting onboarding call to confirm missing fields."
        )

    else:  # v2
        list_id = LIST_V2_COMPLETE
        name    = f"✅ {account_id} - {company} - v2 Complete"
        desc    = (
            f"Pipeline B complete for {company}.\n"
            f"Account ID: {account_id}\n"
            f"Version: v2\n\n"
            f"Files generated:\n"
            f"  - outputs/accounts/{account_id}/v2/account_memo.json\n"
            f"  - outputs/accounts/{account_id}/v2/agent_spec.json\n"
            f"  - changelog/{account_id}/changes.md\n\n"
            f"Status: Ready for Retell deployment."
        )

    try:
        response = requests.post(
            "https://api.trello.com/1/cards",
            params={
                "key":   TRELLO_API_KEY,
                "token": TRELLO_TOKEN
            },
            json={
                "name":   name,
                "desc":   desc,
                "idList": list_id
            }
        )
        if response.status_code == 200:
            print(f"[Trello] ✅ Card created: {name}")
        else:
            print(f"[Trello] ⚠️  Warning: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[Trello] ⚠️  Error creating card: {e}")


# ─── HELPERS ──────────────────────────────────────────────

def get_account_id(filename: str) -> str:
    """Extract account ID from filename e.g. demo_ACC001.txt -> ACC001"""
    name  = filename.replace(".txt", "").replace(".json", "")
    parts = name.split("_")
    for part in parts:
        if part.startswith("ACC"):
            return part
    return ""


# ─── PIPELINE A ───────────────────────────────────────────

def run_pipeline_a(filename: str, account_id: str):
    """Demo call -> v1 memo + agent spec + Trello cards"""
    transcript_path = os.path.join(TRANSCRIPTS_DIR, filename)
    v1_dir          = os.path.join(OUTPUTS_DIR, account_id, "v1")

    print(f"\n=== PIPELINE A: {account_id} ===")

    # Step 1 — Create Demo Received card in To Do list FIRST
    create_trello_card(account_id, account_id, "demo", [])

    # Step 2 — Extract memo from transcript
    memo = extract_memo(transcript_path, account_id, v1_dir)

    # Step 3 — Generate agent spec
    generate_agent_spec(memo, v1_dir)

    # Step 4 — Move card to v1 Generated (Doing list)
    company  = memo.get("company_name") or account_id
    unknowns = memo.get("questions_or_unknowns", [])
    create_trello_card(account_id, company, "v1", unknowns)

    print(f"=== DONE: {account_id} v1 ===")


# ─── PIPELINE B ───────────────────────────────────────────

def run_pipeline_b(filename: str, account_id: str):
    """Onboarding call -> v2 memo + agent spec + changelog + Trello card"""
    transcript_path = os.path.join(TRANSCRIPTS_DIR, filename)
    v1_dir          = os.path.join(OUTPUTS_DIR, account_id, "v1")
    v2_dir          = os.path.join(OUTPUTS_DIR, account_id, "v2")

    # Check v1 exists before patching
    v1_memo_path = os.path.join(v1_dir, "account_memo.json")
    if not os.path.exists(v1_memo_path):
        print(f"[WARNING] No v1 found for {account_id}. Run Pipeline A first.")
        return

    print(f"\n=== PIPELINE B: {account_id} ===")

    # Step 1 — Apply onboarding patch
    v2_memo, _ = apply_patch(account_id, transcript_path, v1_dir, v2_dir)

    # Step 2 — Generate v2 agent spec
    generate_agent_spec(v2_memo, v2_dir)

    # Step 3 — Create v2 Complete card in Done list
    company = v2_memo.get("company_name") or account_id
    create_trello_card(account_id, company, "v2", [])

    print(f"=== DONE: {account_id} v2 ===")


# ─── BATCH RUNNER ─────────────────────────────────────────

def run_all():
    """Process all transcript files in data/transcripts/"""
    files = sorted(os.listdir(TRANSCRIPTS_DIR))

    demo_files       = [f for f in files if f.startswith("demo_")       and f.endswith(".txt")]
    onboarding_files = [f for f in files if f.startswith("onboarding_") and f.endswith(".txt")]

    print(f"\n[Batch] Found {len(demo_files)} demo files, {len(onboarding_files)} onboarding files")

    # Clear Trello board for fresh idempotent run
    clear_trello_board()

    # Pipeline A — all demo calls
    for f in demo_files:
        account_id = get_account_id(f)
        if account_id:
            run_pipeline_a(f, account_id)
        else:
            print(f"[WARNING] Could not extract account_id from: {f}")

    # Pipeline B — all onboarding calls
    for f in onboarding_files:
        account_id = get_account_id(f)
        if account_id:
            run_pipeline_b(f, account_id)
        else:
            print(f"[WARNING] Could not extract account_id from: {f}")

    print("\n[Batch] ALL DONE. Check outputs/accounts/ and Trello board for results.")
    print(f"[Batch] Trello board: https://trello.com/b/EM7q87T4/clara-pipeline-account-tracker")


if __name__ == "__main__":
    run_all()