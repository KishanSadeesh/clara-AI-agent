# Changelog: ACC005 — v1 to v2

**Updated:** 2026-03-04  
**Source:** Onboarding Call

## Fields Changed

| Field | v1 Value | v2 Value | Reason |
|-------|----------|----------|--------|
| `business_hours.timezone` | Central | America/Chicago | onboarding_call |
| `office_address` | Nashville, Tennessee | Nashville Tennessee | onboarding_call |
| `emergency_definition` | ['HVAC failure in a hospital operating room or ICU', 'boiler failure in winter when building temperatures are dropping', 'complete chiller failure in summer causing building temperatures to rise above 85 degrees', 'any refrigerant leak', 'cooling tower failure at a data center', 'flooding from a burst pipe or mechanical failure', 'fire suppression system activation'] | ['compressor failure', 'refrigerant leak', 'temperature above 90 degrees', 'temperature below 55 degrees'] | onboarding_call |
| `emergency_routing_rules.primary_contact` | primary on-call | 615-555-0133 | onboarding_call |
| `emergency_routing_rules.order` | ['primary on-call', 'secondary on-call at 615-555-0144', 'operations manager at 615-555-0155'] | ['615-555-0133', '615-555-0144', '615-555-0166'] | onboarding_call |
| `non_emergency_routing_rules.destination` | service coordinator | guardianhvac.com/portal | onboarding_call |
| `call_transfer_rules.fail_message` | None | Our on-call engineering team has been notified. Someone will contact you within {10 minutes for hospital clients, 20 minutes for others}. | onboarding_call |
| `integration_constraints` | ['never create any job in ServiceTrade automatically without human review'] | ['no auto job creation in ServiceTrade'] | onboarding_call |
| `questions_or_unknowns` | ['specific handling for non-emergency calls during office hours', 'how to handle calls from non-premium accounts during office hours', 'Transfer retry logic not specified in demo.'] | ['ask callers if they are currently on a maintenance contract when preventive maintenance program launches'] | onboarding_call |
| `notes` | premium accounts include Vanderbilt University Medical Center, Saint Thomas Hospital, and any Marriott property; client portal available at guardianhvac.com/portal | VIP accounts: Vanderbilt University Medical Center, Saint Thomas Hospital, Marriott properties, Nashville Predators or Tennessee Titans facility, government building or federal facility. Special date range exception: week between Christmas and New Year treated as after hours. | onboarding_call |