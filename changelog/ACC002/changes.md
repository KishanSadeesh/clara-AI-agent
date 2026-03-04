# Changelog: ACC002 — v1 to v2

**Updated:** 2026-03-04  
**Source:** Onboarding Call

## Fields Changed

| Field | v1 Value | v2 Value | Reason |
|-------|----------|----------|--------|
| `business_hours.days` | None | Monday to Friday | onboarding_call |
| `business_hours.start` | None | 8:30 | onboarding_call |
| `business_hours.end` | None | 5:00 | onboarding_call |
| `emergency_definition` | [] | ['calls related to properties managed by G&M Pressure Washing'] | onboarding_call |
| `emergency_routing_rules.order` | [] | ['Shelley from G&M Pressure Washing'] | onboarding_call |
| `non_emergency_routing_rules.destination` | None | follow up the next business day | onboarding_call |
| `non_emergency_routing_rules.method` | None | inform caller | onboarding_call |
| `office_hours_flow_summary` | None | Clara will answer calls and can transfer to Ben if needed | onboarding_call |
| `after_hours_flow_summary` | None | Clara will inform callers that someone will follow up the next business day, except for emergency calls from G&M Pressure Washing which will be transferred to Ben | onboarding_call |
| `notes` | None | Ben has a second phone number that will be used for personal calls once activated, Clara can be turned on and off as needed | onboarding_call |