# Sharykhin Preparation

# Siarhey Sharykhin

## What is your**experience with stakeholders **— tell me about a **problem you fixed****?**

- **Conflicting priorities between the business team and the client's IT team** (tenant integrations, Marketing SaaS)
    - Problem: the **business development team** had **promised** the client a **fast go-live**,   
but the **client's IT and security teams** would not approve the integration without **a security review**.
    - **What I did**:  
        - **presented** options **in one decision table**, with the same criteria for everyone: **scope**, **risk** and **timeline**
        - **proposed** going live in **phases**: (1) a minimal, compliant integration first, with the remaining improvements **recorded as a technical debt** that had owners and **dates**.
    - **Result**: both sides approved the plan. The client **went live** on time and **security was not bypassed**.

1. Architecture **decisions were lost** and argued again (governance)
    - **Problem**: decisions were made **in calls and emails**. **Months later**, new stakeholders questioned them and **nobody remembered** why they were taken
    - **What *I* did**: you **introduced** lightweight (**ADR**)architecture decision records and a regular review with the key stakeholders.
    - **Result**: **decisions could be traced**, and new people could be brought up to speed faster. This links naturally to what the interviewers said about LeanIX and the  
       architecture review board.
2. Stakeholders **understood "done" differently** (requirements alignment)
    - **Problem**: **marketing**, the **client's IT team** and your **engineering team** each meant something different by the integration requirements, so **work was redone and deadlines**  
**slipped**.
    - **What *you* did**: you introduced one **architecture document **per integration, with context, scope, the agreed **data flows**, **non-functional requirements** and **open decisions**. You  
made sign-off by all parties a required step before implementation.
    - Result: **less rework**, **predictable delivery**, and one document everyone relied on as the correct version.

## Practical example: where did you reduce the risk exposure of an application, and through which decisions

- Context (AI content platform, multi-tenant, on AWS)
    - onboarding a large enterprise tenant, environment review before go-live
- Risks found
    - public API exposed directly, no WAF, no rate limiting
    - tenant integrations using long-lived API keys stored in config / environment variables
    - shared database access across tenants: one bug could expose another tenant's data
    - no central audit log: we could not prove who accessed what
- Decisions I made
    - 
        1. Reduce the attack surface: API behind ALB + AWS WAF (managed rules + rate-based rules), services moved to private subnets
    - 
        1. Replace static secrets: IAM roles for AWS access, Secrets Manager with rotation for the rest, OAuth 2.0 / OIDC via Keycloak for tenants instead of API keys
    - 
        1. Tenant isolation: tenant ID enforced in the authorization layer and in the data access layer, plus automated tests for cross-tenant access
    - 
        1. Visibility: CloudTrail + CloudWatch centralized, alerts on unusual access
    - 
        1. Prioritisation: exposure and identity fixed before go-live, the rest recorded as security debt with owners and dates
- How I got it approved
    - options presented to the CTO / tenant security team in one table: risk, effort, impact on go-live
    - agreed a phased plan: critical fixes first, go-live one week later instead of an unmanaged risk
- Result
    - tenant's security review passed on the first attempt
    - no critical findings open at go-live, secrets rotated automatically
    - the same pattern became the standard for every new tenant



## **How would you secure applications running on **AWS EKS**?**

- 
    - 
        - security alwasy should be considered on all layers 
        - **Identity and access layer**
            1. **IAM roles** - should **not** be **overly permissve**
            2. Use **EKS** **Cluster Access Manager** for managing access to clusters (EKS Access Entries + Polices)
            3. Use **EKS Pod Identity on lower level for **Pods reach AWS services with their own identity.  . Each workload gets its own IAM role with only the permissions it needs, and nothing inherits the node's IAM role.
        - **Network layer**
            - **API endpoints**: Make the cluster **API endpoint** **private**, or **public** but **restricted to IP allow-list**.
            - **Plan proper VPC\\subnets boundaries**.   
Put worker nodes in private subnets.   
Outbound traffic goes through a **NAT gateway**, and VPC endpoints   
give private access to ECR (the container registry), S3, Secrets Manager and STS.
            - **Incoming traffic**:   
put **AWS WAF** in front of the **ALB**,   
add **AWS Shield **against **DDoS attacks**, and terminate TLS with certificates from ACM (AWS Certificate Manager).
            - **Rate limiting**
        - **Secrets and data protection layer**
            - Secret storage: keep secrets in **AWS Secrets Manager**. Deliver them to pods with the Secrets Store CSI Driver or External Secrets Operator instead of plain Kubernetes Secrets  
    in Git.
        - **Dependancies layer**
            - Scanning: scan images in ECR with** Amazon Inspector** enhanced scanning, and 
            - also in the CI/CD pipeline with **Trivy** or a similar scanner, failing the build on critical  
    vulnerabilities.
            - Base images: use **minimal base images** (distroless or **Alpine**) and scan the code for secrets and dependency vulnerabilities (**Gitleaks**, SAST and SCA tools, meaning static code  
  analysis and third-party dependency analysis)
        - **Detection, logging and audit**
            - Control plane logs: **enable EKS control plane logging**, especially the audit and authenticator logs, into **CloudWatch Logs**.
            - Amazon **GuardDuty EKS Protection** is a managed threat detection feature that continuously monitors your Amazon Elastic Kubernetes Service (EKS) clusters for potential security risks
            - **Central view**: use **AWS Security Hub** for the overall security posture, **AWS Config** rules for configuration drift, and **CloudTrail** for AWS API activity. Send all logs to a  
central logging account under **AWS Organizations**.
        - **Nodes and cluster lifecycle**
            - Node type: prefer managed node groups or AWS Fargate, and use Bottlerocket, AWS's minimal container OS, for a smaller attack surface.
            - **Access to nodes**: **no SSH**. Use AWS Systems Manager Session Manager when node access is really needed.
            - **Updates**: keep the Kubernetes version and add-ons current, because EKS versions have an end of standard support, and patch nodes regularly by rolling node replacement.
            - **Benchmarks**: check against the CIS Amazon EKS Benchmark, for example with kube-bench.
        - **Workload hardening**
            - **Pod Security Standards**: apply the **restricted level** through Pod Security Admission. Containers run as non-root, with no privileged mode, no host network or host path mounts,  
all Linux capabilities dropped, and a read-only root filesystem.
            - **Policy as code**: use **Kyverno** or **OPA Gatekeeper** admission policies. An admission policy rejects non-compliant manifests at deploy time: missing resource limits, the latest  
image tag, images from registries that are not allowed.
            - **Resource limits and quotas** per namespace, so one workload cannot starve the others.


## How to improve security web application on AWS with a REST API and an RDS database. How would you proceed?

- **0. Assess before changing anything**
    - turn on **Security Hub** (CIS / AWS Foundational standards), **GuardDuty**, **Config**, **CloudTrail**
    - map the app: diagram, data flows, what is **Internet-facing**, what data is **sensitive**
    - **prioritised findings list**: exposure first, then identity, then data
- **1. Edge** (what the Internet can reach)
    - only **CloudFront / ALB / API Gateway** public
    - **AWS WAF**: managed rules (OWASP Top 10), **rate-based rules**; **Shield**
    - **TLS 1.2+** with an **ACM** certificate, HTTP → HTTPS redirect
- **2. Network**
    - compute in **private subnets**, **RDS in isolated subnets**, **no public IP**
    - **security groups chained**: ALB SG → App SG → DB SG (5432 / 3306 only from the App SG)
    - **VPC endpoints** for S3, Secrets Manager, KMS; **no SSH**, use **Session Manager**
- **3. API layer**
    - **authentication**: OAuth 2.0 / OIDC with the organization's identity provider (**Entra ID**), JWT validated on every call
    - **authorization**: scopes / roles, **object-level checks** (a user sees only their own data)
    - **input validation**, request size limits, **throttling** per client, no internal details in errors
- **4. Compute identity**
    - **IAM role per service**, least privilege, **no access keys**, no admin policies on instance roles
    - patched images / AMIs, **minimal base images**
- **5. Database (RDS)**
    - **encryption at rest** with a **customer-managed KMS key**, **TLS enforced** in transit
    - **IAM database authentication** or credentials in **Secrets Manager with automatic rotation**
    - separate DB users per application (least privilege), **no master user** in the app
    - **automated backups + snapshots encrypted**, **deletion protection**, Multi-AZ for critical data
- **6. Detection and audit**
    - **CloudTrail** and **RDS / ALB / WAF logs** into a **central log account**
    - **GuardDuty** (including **RDS Protection** for suspicious logins), alarms on critical events
- **7. Prevent regressions**
    - **infrastructure as code** (Terraform); **CI/CD**: SAST, dependency, image and secret scanning
    - **Config rules** / **SCPs** as guardrails
- **8. Governance**
    - design reviewed by the **architecture review board**, fixes implemented by the owning teams
    - what can't be fixed now becomes **security debt** with an owner and a date; **penetration test** at the end

## How will you**manage the secrets, the API keys and the certificates** — you mentioned a secret manager, can you go deeper?

- 
    - 
        - **Use IAM roles wherever possible**, instead of stored secrets and keys.
        - **AWS Secrets Manager**: one place for everything that remains
            - What goes there: database passwords, third-party API keys, OAuth client secrets.
            - Secrets Manager keeps versions of a secret: current, pending and previous. During rotation the new password is created and tested while the old one still works, and applications re-read the secret from a short cache, so rotation causes no outage and needs no redeploy.
        - **KMS**: our own keys behind the secrets
            - secrets are encrypted with a customer-managed key, not the default AWS key
            - Reading a secret then needs two separate permissions: IAM permission on the secret and permission in the KMS key policy. A misconfigured IAM policy alone cannot expose the secret, and every decryption is logged.

## **Describe a secure ****VPC architecture**** for critical workloads: what are the main components of a VPC and how do you secure them?**

- 
    - "Yeah, it's clear, it's clear. Now let's go on the networking part. So please describe a secure VPC architecture for critical workloads, what are the main components of VPC, how to secure, etc. Etc." (00:19:25, Donato)
        - security is designed in **layers**, and **isolation** comes first: nothing is reachable unless it is explicitly allowed
        - **Account and VPC boundaries**
            - **separate AWS accounts** (and VPCs) per environment and per critical workload, under **AWS Organizations**
            - **hub-and-spoke** network: workload VPCs connect through a **Transit Gateway** to a central shared-services / inspection VPC, **no ad-hoc VPC peering mesh**
            - **non-overlapping CIDR ranges** planned up front (needed for connecting to on-premises and to other VPCs)
        - **Subnet tiers across multiple Availability Zones** (at least 2, better 3, for high availability)
            - **public subnets**: only the **ALB / NAT gateway**, nothing else
            - **private application subnets**: EKS nodes, ECS tasks, EC2 instances, **no public IPs**
            - **isolated data subnets**: RDS, ElastiCache, **no route to the Internet at all**
            - **route tables per tier**: only the public tier routes to the **Internet Gateway**, the application tier goes out through the **NAT gateway**, the data tier has only local routes
        - **Private access to AWS services**
            - **VPC endpoints**: **gateway endpoints** for S3 and DynamoDB, **interface endpoints (PrivateLink)** for ECR, Secrets Manager, KMS, STS, CloudWatch
            - traffic to AWS services **never goes over the Internet**
            - **endpoint policies** restrict which buckets and resources can be reached (protects against data exfiltration)
        - **Traffic filtering** (two levels)
            - **Security groups**: stateful firewall on each resource, the **main control**, **least privilege**, one security group can reference another (for example "database accepts port 5432 only from the app security group"), no `0.0.0.0/0` inbound except on the ALB
            - **Network ACLs**: stateless rules at the subnet level, a **coarse second line of defence** (for example the data tier blocks everything except the app tier ranges)
            - **AWS Network Firewall** in the inspection VPC for **egress filtering** by domain name and intrusion prevention
            - **Route 53 Resolver DNS Firewall**: blocks DNS lookups of malicious or unapproved domains
        - **Edge protection (incoming traffic)**
            - **CloudFront** and / or the **ALB** as the only entry point
            - **AWS WAF** against layer 7 attacks, **AWS Shield** (Advanced for critical workloads) against **DDoS attacks**
            - **TLS terminated at the ALB** with an **ACM** certificate, re-encrypted to the targets for sensitive data
        - **Admin and hybrid access**
            - **no SSH or RDP open, no bastion hosts**: use **AWS Systems Manager Session Manager**
            - connection to on-premises through **Site-to-Site VPN** or **Direct Connect**, attached to the Transit Gateway
        - **Monitoring and audit**
            - **VPC Flow Logs** (who talked to whom, accepted and rejected) sent to a **central logging account**
            - **GuardDuty** analyses the flow logs and DNS logs for threats (for example crypto-mining or command-and-control traffic)
            - **AWS Config** rules and **Security Hub** catch drift, for example a security group opened to the world or a resource given a public IP
        - **Governance** (for existing applications)
            - **baseline VPC as code** (Terraform or CloudFormation) so every new VPC is compliant by default
            - **Service Control Policies** as guardrails, for example deny creating an Internet Gateway in workload accounts
            - review existing VPCs against the baseline, fix **internet exposure first**, and **record the rest as security debt** with owners and dates

## **Tell me about ****security groups****.**

- 
    - "Okay, and tell me something about the security groups." (00:20:54, Donato)
        - **One security group per tier**, and each tier accepts traffic only from the tier in front of it
            - **ALB SG**: inbound **443** only, from the Internet or only from **CloudFront**
            - **App SG**: inbound only **from the ALB SG**, on the application port
            - **DB SG**: inbound **5432 only from the App SG**
            - rules reference **other security groups, not IP addresses**, so they keep working when instances scale
        - **Least privilege**
            - no `0.0.0.0/0` inbound except on the ALB
            - **no SSH / RDP open**: use **Session Manager** instead
            - **restrict outbound** too, only to what the service really calls
        - **Managed only as code** (Terraform or CloudFormation), no manual changes in the console
        - **Continuous control**
            - **AWS Config** rules and **Security Hub** flag open ports and over-permissive rules
            - **Firewall Manager** enforces baseline rules across all accounts
            - **VPC Flow Logs** show which rules are unused, so they can be removed safely

## **How will you design ****enterprise logging and auditing****?**

- 
    - "Okay. Okay, good. Now, okay, we talking about the network. Let's go to the audit topic. So how will you design enterprise logging and auditing?" (00:21:28, Donato)
        - **Central log archive account** (under **AWS Organizations**)
            - all accounts and regions send logs to **one dedicated log archive account**
            - nobody in the workload accounts can delete or change the logs there
        - **What is collected**
            - **CloudTrail organization trail**: every AWS API call, all accounts, all regions
            - **AWS Config**: configuration history of every resource (who changed what, when)
            - **VPC Flow Logs**, **ALB / CloudFront / WAF logs**, **EKS control plane audit logs**
            - **application logs** into **CloudWatch Logs**, structured (JSON) with a **correlation ID**
        - **Protected storage**
            - **S3** in the log archive account with **Object Lock** (logs cannot be deleted or changed) and **CloudTrail log file validation**
            - encrypted with a **customer-managed KMS key**
            - **retention** set by the compliance requirement, with older logs moved to cheaper **Glacier** storage
        - **Detection and alerting**
            - **GuardDuty** for threats, **Security Hub** as the single view of findings
            - **CloudWatch alarms / EventBridge** on critical events: root login, CloudTrail stopped, security group opened to the world, IAM policy changes
        - **Analysis**
            - **CloudWatch Logs Insights** or **Athena** for queries, **CloudTrail Lake** for audit investigations
            - optionally a **SIEM** (Security Lake, OpenSearch, Splunk) if the organization already uses one
        - **Guardrails**
            - **Service Control Policies**: nobody can stop CloudTrail or delete the log buckets
            - **no personal data or secrets in logs**: masked before they are written

## **How will you protect applications from ****DDoS attacks**** and ****layer 7 attacks****, and which AWS services give you that protection?**

- 
    - 
        - **Layers 3–4** (network floods: SYN / UDP floods)
            - **AWS Shield Standard**: automatic and free on every account
            - **Shield Advanced** for critical apps: 24/7 **Shield Response Team**, automatic layer 7 mitigation, **cost protection** against scaling bills
            - only **CloudFront / ALB / Route 53** exposed, the rest in private subnets
        - **Layer 7** (HTTP floods, injection, bots)
            - **AWS WAF** on CloudFront / ALB / API Gateway
            - **rate-based rules**: block an IP that sends too many requests
            - **AWS managed rule groups**: OWASP Top 10 (SQL injection, XSS), known bad IPs
            - **Bot Control**, geo-blocking if needed
        - **Absorb and scale**
            - **CloudFront** caching absorbs traffic at the edge
            - **Auto Scaling** behind the ALB, **API Gateway throttling** per client
        - **Detect and respond**
            - **CloudWatch** alarms on request spikes, **WAF logs**, a DDoS runbook

## **You inherit ****10 AWS applications**** with a poor security posture. Describe your ****90-day remediation plan****.**

- 
    - **Option C — by architecture-governance process** (closest to the Fincons role)
        - **1. Assess** (weeks 1–3)
            - automated scan (**Security Hub** against the **CIS / AWS Foundational** standards) plus an **architecture review** of each application
            - one **findings list** per application, with severity and owner
        - **2. Plan and agree** (weeks 3–4)
            - remediation plan per application: **harden** (config fixes) or **redesign** (legacy, lift-and-shift applications)
            - approved by the **architecture review board** and security team
        - **3. Delegate and track** (weeks 4–12)
            - the architect designs the fix, **the owning teams implement it**: networking fixes by the networking team, IAM by platform, code by development
            - weekly tracking, risks escalated early
        - **4. Accept or record** (ongoing)
            - what can't be fixed in 90 days becomes **security debt** with a mitigation, owner and date
        - **5. Prevent** (weeks 8–12)
            - reusable **secure patterns** and guardrails (SCPs, Config rules, baseline as code), so the next applications start compliant
        - **Outcome after 90 days:** no critical findings open, every high finding either fixed or recorded as debt, and a repeatable process for the rest of the list
    - **Option A — by time: 30 / 60 / 90 days**
        - **Days 1–30: visibility and quick wins**
            - enable **Security Hub, GuardDuty, Config, CloudTrail** across all 10 applications' accounts
            - build an **inventory**: owners, internet exposure, data sensitivity
            - quick wins: close **public S3 buckets**, `0.0.0.0/0`** security groups**, open SSH / RDP; enforce **MFA**, remove **root access keys**
        - **Days 31–60: fix the high risks**
            - **IAM**: replace access keys with roles, least privilege
            - **edge**: WAF and Shield in front of public endpoints, TLS with ACM
            - **secrets**: move hard-coded secrets to Secrets Manager
            - **encryption at rest** with KMS
        - **Days 61–90: make it stick**
            - **guardrails**: SCPs, Config rules, baseline as code (Terraform)
            - **CI/CD scanning**: image, dependency and secret scanning
            - remaining items recorded as **security debt** with owners and dates; progress reported to stakeholders

## **What is your way of working when you have to ****design a new solution****?**

- 
    - 
        - **1. Understand the need**
            - business goal, scope and **stakeholders** (business, security, networking, operations)
            - **functional and non-functional requirements**: availability, performance, security, compliance (GDPR), cost
        - **2. Check the context and constraints first**
            - the organization's **architecture guidelines and approved patterns**, security standards
            - what already exists in the **application catalogue (LeanIX)**: reuse before building new
        - **3. Design options and trade-offs**
            - 2–3 options compared with the **same criteria**: risk, cost, time, fit with the standards
            - the chosen option recorded as an **architecture decision (ADR)**
        - **4. Document the solution**
            - **technical design document**: context, C4 diagrams (context, container), data flows, deployment, security, NFRs
            - **deviations from the standards** listed explicitly, each with a justification
        - **5. Early reviews, then formal approval**
            - informal early review with **security and networking**, so there are no surprises at the board
            - formal approval by the **architecture review board** and the enterprise architect
        - **6. Non-compliant parts**
            - either a **compliant alternative**, or an approved exception recorded as **technical / security debt** with a mitigation plan, owner and date
        - **7. Hand over and oversee**
            - hand the design to the **implementation teams**, answer their questions, review that the build matches the design
            - update the documentation and the catalogue after go-live

## **You designed a solution following the organization's IT and ****architecture guidelines**** as far as possible, but part of the solution turns out not to be**** compliant with those guidelines****. What do you do to address that?**

- 
    - 
        - **1. Understand the gap**
            - which guideline exactly, and **why** the design can't meet it: technical limit, legacy system, time, cost
            - what is the **risk** of the gap: security, operations, compliance
        - **2. Try to make it compliant first**
            - look for an **alternative design** or an **approved pattern** that meets the same need
            - talk early with the **guideline owner** (security, networking, architecture team), because they often know an approved way
        - **3. If it can't be compliant now: make the deviation visible**
            - document it in the design: **what, why, risk, options considered**
            - never hide it or silently accept it
        - **4. Get a formal decision**
            - present it to the **architecture review board** as an exception request
            - propose a **mitigation** for the meantime: extra monitoring, network isolation, restricted access
        - **5. Record it as technical / security debt**
            - with an **owner**, a **remediation plan** and a **target date** (weeks or months)
            - tracked until closed, reviewed again if the date slips
        - **6. Feed it back**
            - if the same deviation keeps coming up, propose an **update to the guideline** or a new approved pattern

## **In which way do you ****scan Docker images**** to be sure there are no security issues in the code or in the base image? Do you know the names of the ****scanning tools**** you just referred to?**

- 
    - 
        - **Scan at every stage**, not only once
            - **1. Code (before the build)**
                - **SAST** (static code analysis): **SonarQube**, **Semgrep**
                - **secret scanning**: **Gitleaks**, or GitLab / GitHub secret detection
            - **2. Dependencies**
                - **SCA** (third-party libraries with known CVEs): **Snyk**, **OWASP Dependency-Check**, **Trivy**
            - **3. Image (in the CI pipeline, after the build)**
                - **Trivy** or **Grype** scan the base image and OS packages
                - **Dockerfile lint**: **Hadolint**, plus **Checkov** for misconfigurations
                - **build fails** on critical / high findings
            - **4. Registry**
                - **Amazon ECR + Amazon Inspector** enhanced scanning: **continuous re-scan** when new CVEs appear, not only on push
            - **5. Runtime**
                - **GuardDuty Runtime Monitoring** or **Falco** for suspicious behaviour in running containers
        - **Reduce what there is to scan**
            - **minimal base images**: distroless or Alpine, pinned by **digest**
            - rebuild images regularly to pick up **patched base images**
        - **Trust what is deployed**
            - **SBOM** (list of components) generated with **Syft**
            - images **signed** (cosign / AWS Signer), only signed images from **approved registries** can deploy (admission policy)
        - **Governance**
            - findings go to **Security Hub**; what can't be fixed immediately becomes **security debt** with an owner and a date

## **When you design a solution, which tools do you use to ****document the solution****?**

- 
    - 
        - **I use the organization's standard first**, whatever the architecture team and the review board expect
        - **Documents**
            - **Confluence**: technical design document from a template (context, scope, NFRs, security, deviations)
            - **ADRs** (architecture decision records), in Confluence or in Git next to the code
        - **Diagrams**
            - **draw.io / diagrams.net** (inside Confluence) with the **AWS icon set**, the most common choice
            - **Miro** for early workshops with stakeholders
            - **diagrams as code** when diagrams must stay in sync with the system: **Structurizr** (C4), **PlantUML**, **Mermaid**
        - **Notation**
            - **C4 model**: context, container, component levels
            - **UML sequence diagrams** for integration flows
            - **ArchiMate** if the enterprise architecture team works with TOGAF
        - **Enterprise catalogue**
            - **LeanIX**: register the application, its interfaces and technologies, and link the design and decisions to it
        - **API and infrastructure**
            - **OpenAPI / Swagger** for API contracts
            - **Terraform** code as the documentation of what is actually deployed


# Yaraslau Dzmitryieu


## **In which way do you ensure ****security in transit****?**

- HTTPS
- mutial TLS
- Redirect HTTP to HTTP wherever possible. Or forbid HTTPS.
- **Principle**: every hop is encrypted, not only the edge; **TLS 1.2+ (prefer 1.3)**, no plain HTTP anywhere
- **1. Client → edge**
    - **CloudFront / ALB** with an **ACM** certificate and a strict **TLS security policy** (old protocols and weak ciphers off)
    - **HTTP → HTTPS redirect**, **HSTS** header
- **2. Edge → application** (the "hop" gap)
    - **re-encrypt**: ALB → targets over HTTPS, CloudFront → origin HTTPS only
    - between services: **mTLS**, through a **service mesh** (Istio / App Mesh) or **VPC Lattice**, with certificates from **AWS Private CA**
- **3. Application → data and AWS services**
    - **RDS**: force SSL (`rds.force_ssl` / `require_secure_transport`), clients verify the RDS certificate
    - **S3**: bucket policy denies requests without TLS (`aws:SecureTransport = false`)
    - **ElastiCache, MSK, OpenSearch**: in-transit encryption enabled
    - **VPC endpoints / PrivateLink**: traffic to AWS services stays off the Internet
- **4. Hybrid and partner links**
    - **Site-to-Site VPN** (IPsec) or **Direct Connect with MACsec**
    - partners: mTLS or a signed payload
- **5. ****Message-level protection** (data passing through intermediaries: queues, gateways, third parties)
    - **JWS** to sign, **JWE** to encrypt the payload
    - adds to TLS, does not replace it
- **6. ****Certificates**
    - **AWS Certificate Mmanager** (public) and **Private CA** (internal): automatic renewal, **no self-signed certificates**
- **7. ****Enforcement and audit**
    - **AWS Config** rules: `alb-http-to-https-redirection-check`, `s3-bucket-ssl-requests-only`, `elb-tls-https-listeners-only`
    - **Security Hub** for the view across accounts; any exception recorded as **security debt**


## **Microsoft 365 tenant authenticayion****. How to do?**

- **Principle**: the Microsoft 365 identity provider is **Microsoft Entra ID**; federate the SaaS **directly** with Entra ID: **one identity, SSO, MFA / Conditional Access set by the organization**, not by the SaaS
- **Option 1: third-party SaaS that supports federation** (the standard case)
    - add it in Entra ID as an **Enterprise Application** (from the gallery if listed)
    - protocol: **OpenID Connect** (modern) or **SAML 2.0** (most enterprise SaaS)
    - exchange metadata: Entra ID issuer and signing certificate one way, the SaaS redirect / ACS URL the other
    - **claims**: user ID, email, **groups or app roles** so the SaaS can authorise
    - **assign only the groups** that need the app
    - **Conditional Access**: MFA, compliant device, location rules
    - **user provisioning** with **SCIM**: accounts created and **removed automatically** when people leave
- **Option 2: SaaS or internal application you build yourself**
    - **app registration** in Entra ID (single-tenant for internal, **multi-tenant** if customers use their own Entra ID)
    - **OIDC authorization code flow with PKCE** through **MSAL**
    - validate the token: issuer, audience, signature, **tenant ID** (multi-tenant: allow only known tenants)
    - **app roles** mapped to Entra ID groups for authorization
    - **admin consent** only for the permissions really needed (least privilege)
- **Option 3: APIs and machine-to-machine access**
    - **OAuth 2.0 client credentials** for service-to-API, **on-behalf-of** flow when an API calls another API as the user
    - no client secrets where possible: **certificates**, **managed identities** or **workload identity federation** (for example an AWS workload trusted by Entra ID)
- **Option 4: SaaS without SAML or OIDC** (the exception)
    - a broker (Keycloak, Cognito) or **Entra Application Proxy** for header-based or on-premises apps
    - breaks the "no middleware" pattern: **architecture review board approval** and record it as **technical / security debt**, or choose another vendor
- **Always check**
    - token lifetime and session length, logout and **SSO session revocation**
    - **signing certificate rollover** on the SaaS side
    - sign-in logs sent to the central logging / SIEM


## **You mentioned KMS. ****How do you manage KMS keys**** — do you have a suggestion? And what about the rotation of the keys?**

- **Key types**
    - **customer-managed keys** for sensitive data (not the default AWS-managed key): own key policy, own rotation, own audit
    - one key per **application / data classification / environment**, never one key for everything
- **Envelope encryption** (answers the cost and performance concern)
    - KMS generates a **data key**; data is encrypted locally with it; only the data key is encrypted by KMS
    - RDS, S3, EBS do this automatically; in code use the **AWS Encryption SDK** with data key caching
- **Access control**
    - **key policy + IAM**, **separation of duties**: key administrators cannot use the key, applications can only encrypt / decrypt
    - **encryption context** to bind a ciphertext to its purpose; cross-account use only through the key policy
- **Rotation**
    - **automatic rotation** of customer-managed keys (yearly by default, configurable): new key material, **old material kept**, so old data still decrypts with **no re-encryption and no tracking of which key encrypted which row**
    - imported or external key material: rotate manually by switching the **alias** to a new key
    - immediate rotation / re-encryption only after a **suspected compromise**
- **Protection and audit**
    - **CloudTrail** logs every key use; alarms on `DisableKey` / `ScheduleKeyDeletion`
    - deletion waiting period (7–30 days), **SCP** that denies key deletion outside the security team


## **What do you know about the ****WAF****: which controls would you deploy for an Internet-facing application, and how would you operate those controls?**

(So you would add the managed rule groups plus application-specific rules?)

- **Where**
    - on the entry points: **CloudFront**, **ALB**, **API Gateway**
- **Controls**
    - **AWS managed rule groups**: Core rule set (OWASP Top 10), Known bad inputs, SQL database, IP reputation / anonymous IP lists
    - **rate-based rules** per IP or per API key, **size and geo restrictions**
    - **Bot Control**, **Account Takeover Prevention** on the login endpoint
    - **application-specific rules**: allowed methods and paths, admin paths blocked from the Internet — yes, managed groups **plus** custom rules, ordered by priority
- **How to operate them**
    - new rules in **Count mode** first, tune false positives from the logs, then **Block**
    - **WAF logs** to S3 / CloudWatch, dashboards and alarms on blocked-request spikes
    - rules managed **as code** (Terraform), **Firewall Manager** enforces the baseline in every account
    - regular review; pin managed rule group **versions** and test upgrades


## **You mentioned a CDN, so let us talk about ****CloudFront****: why would you place CloudFront in front of the application, and how would you prevent traffic from reaching the origin directly, bypassing CloudFront?**

- **Why CloudFront in front**
    - **caching at the edge**: lower latency, less load on the origin
    - **security at the edge**: Shield Standard absorbs DDoS, **WAF** at the edge, TLS with **ACM**, geo restriction, signed URLs / cookies
    - **one entry point**, the origin stays hidden
- **Prevent direct origin access**
    - **S3 origin**: **Origin Access Control (OAC)**, bucket policy allows only this distribution, **Block Public Access** on
    - **ALB origin**: best is **CloudFront VPC origins** (ALB stays private); otherwise ALB security group allows only the managed prefix list `com.amazonaws.global.cloudfront.origin-facing` **plus** a secret custom header checked by an ALB listener rule or WAF
    - origin protocol **HTTPS only**
- **Also**
    - default root object, no directory listing on the origin


## **On CI/CD pipelines: how would you ****establish continuous vulnerability management**** for the application, the container hosts and the dependencies?**

- **In the pipeline (shift left)**
    - pre-commit and PR: **secret scanning** (Gitleaks), **SAST** (SonarQube / Semgrep)
    - **dependencies**: SCA (Snyk, Dependabot / Renovate for automatic update PRs)
    - **infrastructure as code**: Checkov / tfsec
    - **container image**: Trivy, plus an **SBOM**
    - **quality gate**: build fails on critical / high
- **After deployment (continuous)**
    - **ECR + Amazon Inspector**: images re-scanned when new CVEs appear
    - **hosts**: Amazon Inspector for EC2 and Lambda, **SSM Patch Manager**, immutable golden AMIs from **EC2 Image Builder**
    - **runtime**: GuardDuty Runtime Monitoring
- **Process**
    - all findings in **Security Hub**, fix **SLA per severity** (for example critical in 7 days)
    - on "skip it for minor versions": **do not skip** the scan; use severity thresholds and **time-boxed exceptions** recorded as security debt, otherwise the debt piles up for the next major release


## **How would you design ****centralized security logging**** and auditing across several AWS accounts and regions?**

- **Foundation**
    - **AWS Organizations / Control Tower** landing zone with a **Log Archive** account and a **Security Tooling (Audit)** account
- **Collection**
    - **organization CloudTrail trail**, all accounts and all regions, into S3 in the Log Archive account
    - **AWS Config aggregator**, **Security Hub** and **GuardDuty** with a **delegated administrator** and **cross-region aggregation**
    - VPC Flow Logs, ALB / WAF logs and application logs forwarded (subscription filters / Firehose) or **Amazon Security Lake** (OCSF format)
- **Protection**
    - S3 **Object Lock**, **KMS** encryption, log file validation, **SCPs** so no account can stop CloudTrail or delete logs
- **Use**
    - Athena / CloudTrail Lake for investigations, optional **SIEM**, alarms on critical events


## **And how to manage ****cross-account logging****?**

(Let me say different accounts not by environment by, but by application. So you have application A hosted on account A and application B hosted on)

- **Same pattern** whether accounts are split by environment or by application
    - every application account sends its logs to the central **Log Archive** account
- **One view across application accounts**
    - **CloudWatch cross-account observability**: a **monitoring account** linked to the source accounts (application A, application B) shows their logs, metrics and traces in one console
    - or **CloudWatch Logs subscription filters** to a **cross-account destination** (Kinesis / Firehose) into the central account
- **Access**
    - application teams read **only their own logs**; the security team reads all
    - logs **tagged per application**, retention set per application
- **Security findings**
    - GuardDuty / Security Hub delegated administrator already covers all application accounts
