## What and why

<!-- What changes, and the ticket it closes (INF-xxx). -->

## How verified

<!-- tests, lint, build, manual check... -->

## Before / after merge

<!-- There is no staging: merging deploys to production.
     List anything that must happen first (config, secrets, migrations)
     and anything to check afterwards. Rollback plan. -->

## SOC 2 impact

Does this change add or change any of the following? Tick every box that applies.

- [ ] New public endpoint or open port
- [ ] New site, datacenter or vendor (incl. a new SaaS or cloud service)
- [ ] New system that people log in to
- [ ] New or widened admin / privileged access (IAM roles, RBAC, SSH, tailnet ACLs)
- [ ] Logging, monitoring or alerting change (incl. log sinks, retention, alert receivers)
- [ ] Secret handling change (new secret, new place a secret lives, rotation, CI credentials)
- [ ] None of the above

**If you ticked any box other than "None":** link a ticket in the Linear project **SOC 2 compliance** that covers updating the controls/evidence:

SOC 2 ticket: <!-- INF-xxx -->
