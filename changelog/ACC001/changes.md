# Changelog: ACC001 — v1 to v2

**Updated:** 2026-03-04  
**Source:** Onboarding Call

## Fields Changed

| Field | v1 Value | v2 Value | Reason |
|-------|----------|----------|--------|
| `business_hours.timezone` | Central time | America/Chicago | onboarding_call |
| `call_transfer_rules.timeout_seconds` | None | 45 | onboarding_call |
| `call_transfer_rules.fail_message` | None | We were unable to reach our on-call technician. Your information has been logged and someone will call you within 15 minutes. | onboarding_call |
| `emergency_routing_rules.fallback` | None | 214-555-0288 | onboarding_call |
| `integration_constraints` | ['do not auto-create sprinkler jobs in ServiceTrade'] | ['no sprinkler jobs', 'no alarm inspection jobs', 'only extinguisher recharge jobs can be auto-created'] | onboarding_call |