# CLAUDE.md

## SOC 2 impact (INF-352)

Every PR answers the "SOC 2 impact" checklist in `.github/pull_request_template.md`: new public endpoint/port, new site or vendor, new system with logins, new/widened admin access, logging/alerting change, secret handling change. Any ticked box needs a linked ticket in the Linear project "SOC 2 compliance". Agents fill this section in their PR bodies too.

## Secrets

Never commit secrets. `.github/workflows/gitleaks.yml` scans every PR's new commits and fails on a hit. Test fixtures and build output are allowlisted in `.gitleaks.toml`; reviewed historical false positives are in `.gitleaksignore`. Never add a real secret to either: rotate it.
