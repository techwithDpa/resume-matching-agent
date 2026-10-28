# Interview questions: Diego Silva (#1, final 80, hire)

Role: DevOps / SRE Engineer (must: Kubernetes, Terraform, AWS; nice: CI/CD, Prometheus, Incident Response; 4+ yrs)

| # | Question | What it checks |
|---|---|---|
| 1 | At DataWorks you cut infrastructure cost by 36%. What was the baseline spend, what were the top three changes, and how did you confirm reliability and performance held up? | Verifies the cost claim: AWS specifics, trade-offs, personal ownership |
| 2 | How is your Terraform organized today? Cover modules, remote state and locking, number of accounts or environments, and how changes are reviewed and applied. | Terraform depth. This is a must-have, and the resume gives no detail on it. |
| 3 | When did you last run Kubernetes in production? Describe the cluster (EKS or self-managed, node count, workloads) and the last significant problem you debugged. | Recency gap. Kubernetes is tied only to the 2014–2020 BrightUI role, and the current role lists Docker. |
| 4 | Tell me about the BrightUI migration serving 51M users. What moved from and to where, what was your role, how did you handle cutover and rollback, and what went wrong? | Verifies the scale claim and separates his contribution from the team's |
| 5 | Describe the worst production incident you handled. How were you alerted, how did you triage and communicate, what was the root cause, and what changed afterward? | Incident response and on-call gap. The resume doesn't mention either. |
| 6 | Have you defined SLOs or error budgets? Give an example of an SLI you chose and how it influenced a release or prioritization decision. | SRE practice, as opposed to DevOps tooling alone |
| 7 | What have you built in Prometheus? Give an example alert rule, how you set its thresholds, and one noisy alert you removed. | Prometheus is listed only under skills. This checks for hands-on use. |
| 8 | Describe a CI/CD pipeline you own: stages, deployment strategy (rolling, canary, blue-green), and how you roll back a bad release on AWS. | CI/CD detail and how it connects to the AWS and Kubernetes work |

**Focus areas:** Kubernetes recency (Q3), Terraform depth (Q2), and incident response (Q5) are the biggest risks. Terraform and Kubernetes are must-haves, and the resume doesn't show recent hands-on evidence for them.
