import json
from dotenv import load_dotenv
import os
import re
import requests
from datetime import datetime

load_dotenv()

# 🔐 Use environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

if not GROQ_API_KEY:
    raise ValueError("Set GROQ_API_KEY as environment variable before running.")

EXTRACTION_PROMPT = """You are a strict data extraction assistant for Clara Answers.

Extract ONLY explicitly stated information from the transcript into the JSON schema.

STRICT RULES:
- NEVER invent or assume missing data
- If a field is not explicitly mentioned, set it to null
- If operational detail is unclear or missing, add it to questions_or_unknowns
- DO NOT infer transfer timeouts, retry logic, or escalation order unless explicitly stated
- Output ONLY valid JSON

JSON Schema:
{
  "account_id": null,
  "company_name": null,
  "business_hours": {
    "days": null,
    "start": null,
    "end": null,
    "timezone": null
  },
  "office_address": null,
  "services_supported": [],
  "emergency_definition": [],
  "emergency_routing_rules": {
    "primary_contact": null,
    "contact_number": null,
    "order": [],
    "fallback": null
  },
  "non_emergency_routing_rules": {
    "destination": null,
    "method": null
  },
  "call_transfer_rules": {
    "timeout_seconds": null,
    "retries": null,
    "fail_message": null
  },
  "integration_constraints": [],
  "after_hours_flow_summary": null,
  "office_hours_flow_summary": null,
  "questions_or_unknowns": [],
  "notes": null
}

Transcript:
{transcript}
"""

def call_groq(transcript: str) -> dict:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": EXTRACTION_PROMPT.replace("{transcript}", transcript)}
        ],
        "temperature": 0.0
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    response.raise_for_status()

    raw = response.json()["choices"][0]["message"]["content"]
    clean = re.sub(r"```json|```", "", raw).strip()

    return json.loads(clean)


def validate_and_flag(memo: dict, account_id: str) -> dict:
    unknowns = memo.get("questions_or_unknowns", []) or []

    # Flag missing operational details
    if memo.get("call_transfer_rules", {}).get("timeout_seconds") is None:
        unknowns.append("Transfer timeout not specified in demo.")

    if memo.get("call_transfer_rules", {}).get("retries") is None:
        unknowns.append("Transfer retry logic not specified in demo.")

    if memo.get("emergency_routing_rules", {}).get("order") == []:
        unknowns.append("Emergency escalation order not specified.")

    # Ensure critical fields flagged
    critical_fields = ["company_name", "business_hours", "emergency_definition"]
    for field in critical_fields:
        if memo.get(field) in [None, {}, []]:
            unknowns.append(f"Missing critical field '{field}' – confirm during onboarding.")

    memo["questions_or_unknowns"] = list(set(unknowns))
    memo["account_id"] = account_id
    memo["version"] = "v1"
    memo["source"] = "demo_call"
    memo["generated_at"] = datetime.utcnow().isoformat() + "Z"

    return memo


def extract_memo(transcript_path: str, account_id: str, output_dir: str):
    print(f"[Pipeline A] Processing: {transcript_path}")

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    raw_memo = call_groq(transcript)
    memo = validate_and_flag(raw_memo, account_id)

    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "account_memo.json"), "w") as f:
        json.dump(memo, f, indent=2)

    print(f"[Pipeline A] Memo saved → {output_dir}/account_memo.json")

    return memo


if __name__ == "__main__":
    extract_memo(
        transcript_path="data/transcripts/demo_ACC001.txt",
        account_id="ACC001",
        output_dir="outputs/accounts/ACC001/v1"
    )