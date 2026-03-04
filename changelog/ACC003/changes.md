# Changelog: ACC003 — v1 to v2

**Updated:** 2026-03-04  
**Source:** Onboarding Call

## Fields Changed

| Field | v1 Value | v2 Value | Reason |
|-------|----------|----------|--------|
| `business_hours.days` | Monday through Friday | ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'] | onboarding_call |
| `business_hours.start` | 7am | 7:00am | onboarding_call |
| `business_hours.end` | 6pm | 6:00pm | onboarding_call |
| `business_hours.timezone` | Central time | America/Chicago | onboarding_call |
| `services_supported` | ['sprinkler system installation', 'sprinkler system maintenance', 'fire alarm installation', 'kitchen hood suppression systems', 'annual fire safety inspections'] | ['sprinkler emergency jobs', 'inspection and maintenance jobs'] | onboarding_call |
| `emergency_definition` | ['Active sprinkler head discharge', 'Fire alarm system going off and not resetting', 'Kitchen hood suppression system discharge', 'Active water damage from our systems', 'Active fire risk'] | ['water damage', 'flooding'] | onboarding_call |
| `emergency_routing_rules.primary_contact` | None | 713-555-0142 | onboarding_call |
| `emergency_routing_rules.contact_number` | 713-555-0142 | 713-555-0199 | onboarding_call |
| `emergency_routing_rules.order` | ['on-call technician', 'senior technician Mike (713-555-0199)'] | ['primary', 'secondary'] | onboarding_call |
| `emergency_routing_rules.fallback` | None | Our on-call team has been notified and will contact you within 15 minutes. If this is a life safety emergency please call 911 immediately. | onboarding_call |
| `non_emergency_routing_rules.destination` | None | message taken | onboarding_call |
| `non_emergency_routing_rules.method` | collect info and assure callback | collect info and call back Monday | onboarding_call |
| `call_transfer_rules.timeout_seconds` | None | 40 | onboarding_call |
| `call_transfer_rules.retries` | None | 2 | onboarding_call |
| `call_transfer_rules.fail_message` | None | Our on-call team has been notified and will contact you within 15 minutes. If this is a life safety emergency please call 911 immediately. | onboarding_call |
| `integration_constraints` | ['no auto-creation of sprinkler emergency jobs in ServiceTrade'] | ['never auto-create sprinkler emergency jobs', 'never auto-create kitchen hood suppression jobs'] | onboarding_call |
| `after_hours_flow_summary` | None | collect info and call back Monday | onboarding_call |
| `office_hours_flow_summary` | None | transfer calls | onboarding_call |
| `notes` | hospitals are top priority clients, treat them differently | never put callers on hold, VIP routing rule for Memorial Hermann Hospital system, page 713-555-0300 | onboarding_call |