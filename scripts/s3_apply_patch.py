import json, os, re, requests,time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

ONBOARDING_PROMPT = """You are a data extraction assistant for Clara Answers.

This is an ONBOARDING call transcript. Extract ONLY the new or updated information confirmed during this call.

RULES:
- Only include fields that were EXPLICITLY confirmed or updated in this call
- If a field was not discussed, do NOT include it
- Do not repeat info from a previous version - only what's new or changed
- Output ONLY valid JSON using the same schema. No markdown. No explanation.

Schema (only include fields that changed or were confirmed):
{
  "company_name": null,
  "business_hours": {"days": null, "start": null, "end": null, "timezone": null},
  "office_address": null,
  "services_supported": [],
  "emergency_definition": [],
  "emergency_routing_rules": {"primary_contact": null, "contact_number": null, "order": [], "fallback": null},
  "non_emergency_routing_rules": {"destination": null, "method": null},
  "call_transfer_rules": {"timeout_seconds": null, "retries": null, "fail_message": null},
  "integration_constraints": [],
  "after_hours_flow_summary": null,
  "office_hours_flow_summary": null,
  "questions_or_unknowns": [],
  "notes": null
}

Transcript:
{transcript}"""


def call_groq(transcript: str) -> dict:
    """Send transcript to Groq with retry logic for rate limits."""
    max_retries = 5
    wait_seconds = 15

    for attempt in range(max_retries):
        time.sleep(5)  # always wait 5 seconds before every call
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": [{"role": "user", "content": ONBOARDING_PROMPT.replace("{transcript}", transcript)}],
                    "temperature": 0.0,
                    "max_tokens": 2000
                }
            )

            # If rate limited wait and retry
            if response.status_code == 429:
                print(f"[Groq] Rate limited. Waiting {wait_seconds}s before retry {attempt+1}/{max_retries}...")
                time.sleep(wait_seconds)
                wait_seconds += 10  # increase wait each retry
                continue

            response.raise_for_status()
            raw = response.json()["choices"][0]["message"]["content"]
            clean = re.sub(r"```json|```", "", raw).strip()
            return json.loads(clean)

        except Exception as e:
            if attempt < max_retries - 1:
                print(f"[Groq] Error: {e}. Retrying in {wait_seconds}s...")
                time.sleep(wait_seconds)
            else:
                raise

    raise Exception("Groq API failed after maximum retries")

def deep_merge(v1: dict, updates: dict, path="") -> tuple[dict, list]:
    """Recursively merge updates into v1. Returns (merged_dict, changelog_entries)."""
    result = v1.copy()
    changelog = []
    for key, new_val in updates.items():
        if new_val is None:
            continue
        old_val = v1.get(key)
        full_key = f"{path}.{key}" if path else key
        if isinstance(new_val, dict) and isinstance(old_val, dict):
            merged_sub, sub_log = deep_merge(old_val, new_val, full_key)
            result[key] = merged_sub
            changelog.extend(sub_log)
        elif new_val != old_val and new_val not in ([], {}, None):
            changelog.append({
                "field": full_key,
                "old_value": old_val,
                "new_value": new_val,
                "source": "onboarding_call",
                "updated_at": datetime.utcnow().isoformat() + "Z"
            })
            result[key] = new_val
    return result, changelog


def save_changelog(changelog: list, account_id: str, output_dir: str):
    """Save changelog as markdown to changelog/<account_id>/ folder."""

    changelog_dir = os.path.join("changelog", account_id)
    os.makedirs(changelog_dir, exist_ok=True)

    md_lines = [
        f"# Changelog: {account_id} — v1 to v2\n",
        f"**Updated:** {datetime.utcnow().strftime('%Y-%m-%d')}  ",
        "**Source:** Onboarding Call\n",
        "## Fields Changed\n",
        "| Field | v1 Value | v2 Value | Reason |",
        "|-------|----------|----------|--------|"
    ]
    for c in changelog:
        md_lines.append(
            f"| `{c['field']}` | {c['old_value']} | {c['new_value']} | {c.get('source', 'confirmed during onboarding')} |"
        )
    if not changelog:
        md_lines.append("| — | No changes detected | — | — |")

    cl_md_path = os.path.join(changelog_dir, "changes.md")
    with open(cl_md_path, "w") as f:
        f.write("\n".join(md_lines))

    print(f"[Pipeline B] Changelog saved -> changelog/{account_id}/changes.md")

def apply_patch(account_id: str, onboarding_transcript_path: str, v1_dir: str, v2_dir: str):
    """Full Pipeline B: load v1 -> extract onboarding updates -> merge -> save v2."""
    print(f"\n[Pipeline B] Patching {account_id}")
    
    # Load v1 memo
    v1_path = os.path.join(v1_dir, "account_memo.json")
    with open(v1_path) as f:
        v1_memo = json.load(f)
    
    # Extract onboarding updates
    with open(onboarding_transcript_path, encoding="utf-8") as f:
        transcript = f.read()
    updates = call_groq(transcript)
    
    # Merge and track changes
    v2_memo, changelog = deep_merge(v1_memo, updates)
    v2_memo["version"] = "v2"
    v2_memo["source"] = "onboarding_call"
    v2_memo["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    # Save v2 memo
    os.makedirs(v2_dir, exist_ok=True)
    memo_path = os.path.join(v2_dir, "account_memo.json")
    with open(memo_path, "w") as f:
        json.dump(v2_memo, f, indent=2)
    print(f"[Pipeline B] v2 memo saved -> {memo_path}")
    
    # Save changelog
    save_changelog(changelog, account_id, v2_dir)
    
    return v2_memo, changelog


if __name__ == "__main__":
    apply_patch(
        account_id="ACC001",
        onboarding_transcript_path="data/transcripts/onboarding_ACC001.txt",
        v1_dir="outputs/accounts/ACC001/v1",
        v2_dir="outputs/accounts/ACC001/v2"
    )