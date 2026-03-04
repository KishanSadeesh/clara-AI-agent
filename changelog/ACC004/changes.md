# Changelog: ACC004 — v1 to v2

**Updated:** 2026-03-04  
**Source:** Onboarding Call

## Fields Changed

| Field | v1 Value | v2 Value | Reason |
|-------|----------|----------|--------|
| `emergency_definition` | ['Complete power outage to a commercial building or facility', 'Live exposed wiring accessible to people', 'Electrical burning smell or sparks with unknown source', 'Main panel failure', 'Generator failure at a hospital or data center', 'Anything where there is immediate risk of fire, injury, or critical system failure'] | ['arc flash', 'electrical fire', 'hospital', 'data center', 'airport', 'semiconductor fabrication facility'] | onboarding_call |
| `emergency_routing_rules.primary_contact` | dispatcher | 602-555-0187 | onboarding_call |
| `emergency_routing_rules.order` | ['dispatcher', 'on-call supervisor'] | ['602-555-0187', '602-555-0233'] | onboarding_call |
| `emergency_routing_rules.fallback` | collect caller information and send an alert | Collect name, callback number, location, and nature of the issue. Then send a text alert. | onboarding_call |
| `call_transfer_rules.fail_message` | None | Our emergency team has been notified and will contact you within 10 minutes. This is being escalated as a priority emergency. | onboarding_call |
| `integration_constraints` | ['no auto-creation of emergency jobs', 'no auto-creation of inspection scheduling requests'] | ['no auto job creation in ServiceTrade or FieldEdge'] | onboarding_call |
| `questions_or_unknowns` | ['how to handle non-emergency calls during office hours', 'Transfer retry logic not specified in demo.'] | ['Spanish language support'] | onboarding_call |