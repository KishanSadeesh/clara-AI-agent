
import json
import os
from datetime import datetime


def format_business_hours(bh: dict) -> str:
    if not bh or not bh.get("days"):
        return "Business hours not yet confirmed."
    days  = bh.get("days")
    start = bh.get("start")
    end   = bh.get("end")
    tz    = bh.get("timezone") or ""
    return f"{days} from {start} to {end} {tz}".strip()


def generate_prompt(memo: dict) -> str:
    company   = memo.get("company_name") or "our company"
    services  = ", ".join(memo.get("services_supported", [])) or "service trade"
    bh_text   = format_business_hours(memo.get("business_hours"))

    emergency_triggers = memo.get("emergency_definition", [])
    emergency_text = "\n".join([f"  - {e}" for e in emergency_triggers]) if emergency_triggers else "  - Emergency criteria not fully defined."

    emergency_contact = memo.get("emergency_routing_rules", {}).get("contact_number")
    routing_text = f"If emergency → transfer to on-call technician at {emergency_contact}." if emergency_contact else "If emergency → follow defined escalation protocol."

    transfer = memo.get("call_transfer_rules") or {}
    timeout  = transfer.get("timeout_seconds") or 30

    return f"""You are Clara, a professional AI voice assistant for {company}.
You handle inbound calls for: {services}.
Business hours: {bh_text}

== BUSINESS HOURS CALL FLOW ==

Step 1 - GREETING:
Say: "Thank you for calling {company}, this is Clara. How can I help you today?"

Step 2 - ASK PURPOSE:
Listen carefully. Identify if emergency, non-emergency, scheduling, or inquiry.

Step 3 - COLLECT CALLER INFO:
Ask: "May I get your name and best callback number?"
Repeat the number back to confirm accuracy.

Step 4 - ROUTE OR TRANSFER:
- {routing_text} Transfer timeout: {timeout} seconds.
- If non-emergency → transfer to office line or take message.

Step 5 - IF TRANSFER FAILS:
Say: "I'm sorry, I wasn't able to connect you right now. Someone from {company} will call you back as soon as possible."

Step 6 - CONFIRM NEXT STEPS:
Tell the caller what will happen next.

Step 7 - ASK IF ANYTHING ELSE:
Say: "Is there anything else I can help you with today?"

Step 8 - CLOSE:
Say: "Thank you for calling {company}. Have a great day!"

== AFTER-HOURS CALL FLOW ==

Step 1 - GREETING:
Say: "Thank you for calling {company}. Our office is currently closed. I'm Clara and I can help you right now."

Step 2 - ASK PURPOSE:
"Can you briefly describe the reason for your call?"

Step 3 - DETERMINE EMERGENCY:
Emergency triggers:
{emergency_text}
If unclear ask: "Is this an active emergency requiring immediate attention?"

Step 4a - IF EMERGENCY:
Say: "I understand this is an emergency. Let me get your information right away."
Collect in order:
  1. Full name
  2. Callback number (read back to confirm)
  3. Service address
Say: "I am connecting you to our on-call team now. Please hold."
Attempt transfer. Timeout: {timeout} seconds.
If transfer fails: "I was unable to reach our on-call team. Your information has been recorded and someone will contact you immediately. Call 911 if there is immediate danger."

Step 4b - IF NON-EMERGENCY:
Collect: full name, callback number (confirm), brief description.
Say: "Someone from {company} will contact you next business day."

Step 5 - ASK IF ANYTHING ELSE:
"Is there anything else I can help you with?"

Step 6 - CLOSE:
"Thank you for calling {company}. We will be in touch soon."

== RULES - ALWAYS FOLLOW ==
- NEVER mention function calls, tools, APIs, or internal systems to the caller
- NEVER ask for information you already have
- Ask only ONE question at a time
- Always confirm callback numbers by reading them back
- Keep tone professional, calm, and empathetic"""


def generate_agent_spec(memo: dict, output_dir: str) -> dict:
    """memo is already a dict - use directly, no file reading needed."""
    bh       = memo.get("business_hours") or {}
    routing  = memo.get("emergency_routing_rules") or {}
    transfer = memo.get("call_transfer_rules") or {}

    spec = {
        "agent_name": f"Clara - {memo.get('company_name', 'Unknown')}",
        "version": memo.get("version", "v1"),
        "voice_style": "professional, calm, empathetic",
        "language": "en-US",
        "system_prompt": generate_prompt(memo),
        "key_variables": {
            "timezone": bh.get("timezone"),
            "business_hours": {
                "days":  bh.get("days"),
                "start": bh.get("start"),
                "end":   bh.get("end")
            },
            "office_address":    memo.get("office_address"),
            "emergency_routing": routing
        },
        "tool_invocation_placeholders": [
            "transfer_call(destination_number)",
            "log_call_details(name, number, address, call_type)",
            "check_business_hours(timezone)"
        ],
        "call_transfer_protocol": {
            "timeout_seconds": transfer.get("timeout_seconds", 30),
            "retries":         transfer.get("retries", 1),
            "on_success":      "Stay silent and allow connection",
            "on_failure":      transfer.get("fail_message") or "Apologize and assure callback"
        },
        "fallback_protocol": {
            "action":  "collect_and_assure",
            "message": "I was unable to connect you. Your information has been recorded and someone will follow up shortly."
        },
        "integration_constraints": memo.get("integration_constraints", []),
        "generated_at":        datetime.utcnow().isoformat() + "Z",
        "source_memo_version": memo.get("version", "v1")
    }

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "agent_spec.json")
    with open(path, "w") as f:
        json.dump(spec, f, indent=2)
    print(f"[Pipeline A] Agent spec saved -> {path}")
    return spec


if __name__ == "__main__":
    with open("outputs/accounts/ACC001/v1/account_memo.json") as f:
        memo = json.load(f)
    generate_agent_spec(memo, "outputs/accounts/ACC001/v1")