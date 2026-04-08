# Lab 06 — Container as Firewall / NAT Gateway

(No written questions in this lab, but here is the explanation for the DNAT challenge)

## DNAT Challenge Explanation
To make the web server accessible from the outside:
1. `PREROUTING`: We use the `nat` table in the `PREROUTING` chain. Port 80 traffic arriving on the external interface (`eth0`) is rewritten so its destination IP is `172.40.1.10`.
2. `FORWARD`: Because the destination IP is rewritten before the routing decision, the traffic goes to the `FORWARD` chain. We must add a rule explicitly `ACCEPT`ing `NEW` traffic destined for `172.40.1.10` on port 80, because our default policy is `DROP`.
