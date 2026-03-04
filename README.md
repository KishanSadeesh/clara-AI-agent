# Clara Answers — AI Voice Agent Pipeline

> Automated pipeline that converts real-world call transcripts into 
> production-ready Retell AI voice agent configurations.

## 🎥 Demo
- **Loom Video:** [Add your Loom link here]
- **Dashboard:** [(https://github.com/KishanSadeesh/clara-ai.git)]
- **Trello Board:** https://trello.com/b/EM7q87T4/clara-pipeline-account-tracker

---

## 🧠 What This Does

Clara Answers is an AI-powered voice agent for service trade businesses
(fire protection, electrical, HVAC, alarm systems).

This pipeline automates the full onboarding journey:
```
Demo Call Transcript
        ↓
[Groq LLM Extraction]
        ↓
Account Memo JSON (v1)  +  Retell Agent Spec (v1)
        ↓
Onboarding Call Transcript
        ↓
[Groq LLM Patch Extraction]
        ↓
Account Memo JSON (v2)  +  Retell Agent Spec (v2)  +  Changelog
        ↓
Trello Card Created → Ready for Retell Deployment
```

---

## 🏗️ Architecture
```
clara-pipeline/
├── scripts/
│   ├── s1_extract_memo.py         # Pipeline A Step 1: transcript → memo JSON
│   ├── s2_generate_agent_spec.py  # Pipeline A Step 2: memo → agent spec JSON
│   ├── s3_apply_patch.py          # Pipeline B: onboarding → v2 patch + changelog
│   └── s4_batch_run.py            # Batch runner: all 10 files + Trello integration
├── data/
│   └── transcripts/               # Input transcripts (demo + onboarding)
│       ├── demo_ACC001.txt
│       ├── demo_ACC002.txt
│       ├── demo_ACC003.txt
│       ├── demo_ACC004.txt
│       ├── demo_ACC005.txt
│       ├── onboarding_ACC001.txt
│       ├── onboarding_ACC002.txt
│       ├── onboarding_ACC003.txt
│       ├── onboarding_ACC004.txt
│       └── onboarding_ACC005.txt
├── outputs/
│   └── accounts/
│       └── ACCXXX/
│           ├── v1/
│           │   ├── account_memo.json   # Extracted from demo call
│           │   └── agent_spec.json     # Generated Retell config
│           └── v2/
│               ├── account_memo.json   # Updated from onboarding call
│               └── agent_spec.json     # Updated Retell config
├── changelog/
│   └── ACCXXX/
│       └── changes.md              # Human-readable v1 → v2 diff
├── workflows/
│   ├── pipeline_a_demo_to_agent.json
│   ├── pipeline_b_onboarding_patch.json
│   └── pipeline_batch_run.json
├── docker-compose.yml
├── retell_setup.md
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack (100% Free, Zero Cost)

| Tool | Purpose | Cost |
|------|---------|------|
| Groq API (llama-3.3-70b) | LLM extraction and generation | Free |
| Python 3.10 | Pipeline scripts | Free |
| n8n (Docker) | Visual workflow orchestration | Free (self-hosted) |
| Trello API | Task tracking per account | Free |
| GitHub | Version controlled storage | Free |
| Retell AI | Target voice agent platform | Free tier |

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOURUSERNAME/clara-pipeline
cd clara-pipeline
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your API keys:
```
update all GROQ_API_KEY,TRELLO_API_KEY,TRELLO_TOKEN,RETELL_API_KEY
```

### 4. Add transcript files
Place your transcripts in `data/transcripts/`:
- Demo calls named: `demo_ACCXXX.txt`
- Onboarding calls named: `onboarding_ACCXXX.txt`

### 5. Run the full batch pipeline
```bash
python scripts/s4_batch_run.py
```

This will:
- Process all 5 demo transcripts → generate v1 outputs
- Process all 5 onboarding transcripts → generate v2 outputs
- Create Trello cards for every account automatically
- Save changelogs to `changelog/` folder

---

## 🔄 Pipeline A — Demo Call to v1 Agent

**Input:** `data/transcripts/demo_ACCXXX.txt`

**Steps:**
1. Create `📥 Demo Received` card in Trello To Do list
2. Read transcript file
3. Send to Groq LLM with strict extraction prompt
4. Extract structured Account Memo JSON
5. Validate — flag all missing fields in `questions_or_unknowns`
6. Generate full Retell Agent Spec with:
   - Business hours call flow
   - After-hours call flow
   - Emergency routing
   - Transfer protocol
   - Fallback protocol
7. Save outputs to `outputs/accounts/ACCXXX/v1/`
8. Create `⚙️ v1 Generated` card in Trello Doing list

**Output:**
```
outputs/accounts/ACCXXX/v1/
├── account_memo.json
└── agent_spec.json
```

---

## 🔄 Pipeline B — Onboarding Call to v2 Agent

**Input:** `data/transcripts/onboarding_ACCXXX.txt`

**Steps:**
1. Load existing v1 memo
2. Send onboarding transcript to Groq LLM
3. Extract only new or updated fields
4. Deep merge updates into v1 memo
5. Track every changed field with old value, new value, and reason
6. Regenerate agent spec with confirmed configuration
7. Save changelog to `changelog/ACCXXX/changes.md`
8. Save outputs to `outputs/accounts/ACCXXX/v2/`
9. Create `✅ v2 Complete` card in Trello Done list

**Output:**
```
outputs/accounts/ACCXXX/v2/
├── account_memo.json
└── agent_spec.json

changelog/ACCXXX/
└── changes.md
```

---

## 📋 Account Memo JSON Schema

Every account memo contains these fields:
```json
{
  "account_id": "ACC001",
  "company_name": "ProShield Fire Protection",
  "version": "v1",
  "source": "demo_call",
  "business_hours": {
    "days": "Monday through Friday",
    "start": "7am",
    "end": "6pm",
    "timezone": "America/Chicago"
  },
  "office_address": null,
  "services_supported": ["sprinkler installation", "fire alarm systems"],
  "emergency_definition": ["active sprinkler discharge", "fire alarm going off"],
  "emergency_routing_rules": {
    "primary_contact": "on-call technician",
    "contact_number": "214-555-0199",
    "fallback": null
  },
  "non_emergency_routing_rules": {
    "method": "take message and call back next business day"
  },
  "call_transfer_rules": {
    "timeout_seconds": null,
    "retries": null,
    "fail_message": null
  },
  "integration_constraints": [
    "never auto-create sprinkler jobs in ServiceTrade"
  ],
  "questions_or_unknowns": [
    "Missing critical field 'call_transfer_rules' - confirm during onboarding."
  ],
  "notes": null,
  "generated_at": "2025-01-15T10:30:00Z"
}
```

> **Missing Data Policy:** All missing fields are set to `null`.
> Critical missing fields are flagged in `questions_or_unknowns`.
> The pipeline **never hallucninates or invents missing data.**

---

## 🤖 Retell Agent Spec Schema
```json
{
  "agent_name": "Clara - ProShield Fire Protection",
  "version": "v1",
  "voice_style": "professional, calm, empathetic",
  "language": "en-US",
  "system_prompt": "Full Clara voice agent prompt...",
  "key_variables": {
    "timezone": "America/Chicago",
    "business_hours": {...},
    "emergency_routing": {...}
  },
  "call_transfer_protocol": {
    "timeout_seconds": 45,
    "on_failure": "Apologize and assure callback"
  },
  "fallback_protocol": {
    "message": "I was unable to connect you. Someone will follow up shortly."
  },
  "integration_constraints": [
    "never auto-create sprinkler jobs in ServiceTrade"
  ]
}
```

---

## 📝 Changelog Format

Every `changelog/ACCXXX/changes.md` shows:
```markdown
# Changelog: ACC001 — v1 to v2

**Updated:** 2025-01-15
**Source:** Onboarding Call

## Fields Changed

| Field | v1 Value | v2 Value | Reason |
|-------|----------|----------|--------|
| call_transfer_rules.timeout_seconds | null | 45 | confirmed during onboarding |
| emergency_routing_rules.backup_number | null | 214-555-0288 | Mike - Operations Manager |
| business_hours.timezone | Central time | America/Chicago | timezone confirmed |
```

---

## 🔧 n8n Workflow Setup

### Prerequisites
- Docker Desktop installed from https://docker.com

### Start n8n
```bash
# Start n8n via Docker Compose
docker-compose up -d

# Open n8n in browser
# Go to http://localhost:5678
```

### Import Workflows
1. Open http://localhost:5678
2. Go to **Workflows** → **Import from File**
3. Import each file from `workflows/` folder:
   - `pipeline_a_demo_to_agent.json`
   - `pipeline_b_onboarding_patch.json`
   - `pipeline_batch_run.json`
4. Update Groq API key in each HTTP Request node

### Stop n8n
```bash
docker-compose down
```

---

## 📞 Retell Setup

See `retell_setup.md` for complete manual steps to deploy
any generated agent spec into the Retell UI.

**Summary:**
1. Create account at https://retell.ai
2. Create New Agent → Blank Agent
3. Copy `system_prompt` from `agent_spec.json`
4. Paste into Retell System Prompt field
5. Configure transfer number from `emergency_routing_rules`
6. Publish agent

---

## 🔑 Environment Variables

| Variable | Description | Where to Get |
|----------|-------------|-------------|
| `GROQ_API_KEY` | Free LLM API key | https://console.groq.com |
| `TRELLO_API_KEY` | Task tracker API | https://trello.com/power-ups/admin |
| `TRELLO_TOKEN` | Trello auth token | https://trello.com/power-ups/admin |
| `RETELL_API_KEY` | Voice agent platform | https://retell.ai |

---

## 🧪 Running Tests

### Test single account
```bash
# Test Pipeline A only
python scripts/s1_extract_memo.py
python scripts/s2_generate_agent_spec.py

# Test Pipeline B only
python scripts/s3_apply_patch.py
```

### Test full batch
```bash
python scripts/s4_batch_run.py
```

### Expected output
```
[Batch] Found 5 demo files, 5 onboarding files
[Trello] Cleared existing cards
=== PIPELINE A: ACC001 === ... DONE
=== PIPELINE A: ACC002 === ... DONE
=== PIPELINE A: ACC003 === ... DONE
=== PIPELINE A: ACC004 === ... DONE
=== PIPELINE A: ACC005 === ... DONE
=== PIPELINE B: ACC001 === ... DONE
=== PIPELINE B: ACC002 === ... DONE
=== PIPELINE B: ACC003 === ... DONE
=== PIPELINE B: ACC004 === ... DONE
=== PIPELINE B: ACC005 === ... DONE
[Batch] ALL DONE.
```

---

## ⚠️ Known Limitations

- Requires text transcripts as input — audio transcription not included
- n8n must be run locally via Docker — not cloud hosted
- Groq free tier has rate limits — large batches may need delays
- Retell API deployment is manual — requires UI copy-paste

---

## 🚀 What I Would Improve With Production Access

- **Retell API** — auto-deploy agent specs directly via API
- **Whisper** — add audio transcription for .mp3/.wav files
- **Supabase** — replace local JSON files with proper database
- **Webhooks** — trigger pipeline automatically when new transcript arrives
- **Slack notifications** — alert team when new account is ready
- **Diff viewer UI** — visual side-by-side v1 vs v2 comparison
- **Multi-language** — Spanish language support for Clara agent

---

## 📊 Evaluation Criteria Met

| Criteria | Implementation |
|----------|---------------|
| Runs end-to-end on all 10 files | `s4_batch_run.py` processes all automatically |
| No hallucination | `questions_or_unknowns` used for all missing data |
| Correct agent prompts | Both business hours + after-hours flows in every spec |
| Clean versioning | v1 and v2 separate with `changes.md` per account |
| Task tracker | Trello cards auto-created via API |
| Reproducible | docker-compose + .env.example + README |
| Zero cost | Groq free tier + all free tools |

---

## 👤 Submission

**GitHub:** https://github.com/KishanSadeesh/clara-ai.git
**Loom:** [Add your Loom link]
**Trello:** https://trello.com/b/EM7q87T4/clara-pipeline-account-tracker