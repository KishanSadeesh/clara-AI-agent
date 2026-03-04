# Changelog: ACC004 — v1 to v2

**Updated:** 2026-03-04  
**Source:** Onboarding Call

## Fields Changed

| Field | v1 Value | v2 Value | Reason |
|-------|----------|----------|--------|
| `emergency_routing_rules.primary_contact` | Dispatcher | 602-555-0187 | onboarding_call |
| `emergency_routing_rules.order` | ['Dispatcher', 'On-call supervisor'] | ['602-555-0187', '602-555-0233'] | onboarding_call |
| `emergency_routing_rules.fallback` | Collect caller information and send an alert | Collect name, callback number, location, and nature of the issue. Then send a text alert. | onboarding_call |
| `emergency_definition` | ['Complete power outage to a commercial building or facility', 'Live exposed wiring accessible to people', 'Electrical burning smell or sparks with unknown source', 'Main panel failure', 'Generator failure at a hospital or data center', 'Anything where there is immediate risk of fire, injury, or critical system failure'] | ['arc flash', 'electrical fire', 'hospital', 'data center', 'airport', 'semiconductor fabrication facility'] | onboarding_call |
| `call_transfer_rules.fail_message` | None | Our emergency team has been notified and will contact you within 10 minutes. This is being escalated as a priority emergency. | onboarding_call |
| `after_hours_flow_summary` | Transfer to 24 hour emergency line | Ask if issue is preventing operation, escalate to emergency if yes | onboarding_call |
| `questions_or_unknowns` | ['Transfer retry logic not specified in demo.', 'How to prioritize non-emergency calls', 'How to handle non-emergency calls during office hours'] | ['Spanish language support'] | onboarding_call |
| `notes` | Hospitals, data centers, and airports have SLA agreements and are treated as priority emergencies | No auto job creation in ServiceTrade or FieldEdge, no daylight saving time changes | onboarding_call |