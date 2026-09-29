# Fincons Architect (PMI) phase 1 — questions asked

Questions extracted from `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md`, the transcript of the phase 1 interview recorded 2026-09-25, source `https://app.bluedothq.com/preview/6ab64ec38b7f2b9d935d5412`, duration 1 hour 8 minutes 50 seconds.

Speakers in that transcript: **Speaker A** is the candidate, Yaraslau Dzmitryieu (who asks to be called Jarek at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:62`); **Speaker B** is Antonio, who describes the customer request and asks the methodological questions; **Speaker C** is Donato, who introduces himself as a solution architect at Fincons at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:52` and asks the hands-on AWS security questions. A fourth participant, Katerina, is greeted at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:36` but asks no question in the transcript.

Each entry gives the general idea of the question in full form, then the exact wording from the transcript with its timestamp, then an outline of the answer Yaraslau gave, with the transcript line of that answer; in Part 5, where Yaraslau asks the questions, the outline is of the interviewer's reply. Where the candidate left part of a question unanswered, the outline says so. The transcript is auto-transcribed, so the quoted wording is kept exactly as the transcriber produced it, and the correct term is added in square brackets immediately after each garbled one — the convention for correcting a quotation without destroying it. What the garbled terms mean:

| As transcribed | What was actually said |
| --- | --- |
| "entry D", "entry ID", "in 3D" | Microsoft Entra ID, the cloud identity provider formerly called Azure Active Directory and the identity provider behind every Microsoft 365 tenant |
| "entity providers" | identity providers |
| "SSAO MFA" | SSO and MFA, that is single sign-on and multi-factor authentication |
| "FDS RDS database" | an Amazon RDS database; "FDS" is not an AWS service and is a false start immediately corrected to RDS |
| "AWS JS" | AWS; the service name after "AWS" is not intelligible in the transcript, see the note at the end of this file |
| "in Kubernetes application" | in front of the application |
| "directory gene access" | direct origin access — traffic that bypasses CloudFront and reaches the origin directly; see the note at the end of this file |
| "cross account login" | cross-account logging |
| "GWT token" | JWT, a JSON Web Token |
| "GSON web security" | JSON Web Encryption, part of the JOSE family (JWS signs a payload, JWE encrypts it), which is the REST counterpart of SOAP's WS-Security |
| "SOAP with versus security" | SOAP with WS-Security |
| "OVASP" | OWASP, the Open Worldwide Application Security Project, whose Top 10 list the candidate refers to |
| "Kickloak" | Keycloak |
| "Linux" as the name of a catalogue tool | SAP LeanIX, the enterprise architecture management product |
| "the world" | Vault, meaning HashiCorp Vault for secrets management |

The role being interviewed for: an architect who improves the security posture of a customer's applications deployed on AWS, by designing the remediation of security findings that another team then implements. Antonio states that scope at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:96` and `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:104`, and narrows it at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:140` — "the architect should only design the most secure solution. Then another team will implement and develop deploy it."

## Part 1 — opening and framing, asked by Donato and Antonio

1. **Introduce yourself briefly.**
   - "So give me just a brief introduction." (00:04:39, Donato)
   - **Yaraslau's answer** (00:04:45–00:08:02, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:62-74`):
     - software engineer, team lead and architect with 11 years of experience, 16 projects: healthcare, finance, banking, logistics, license management, loyalty systems
     - started as a front-end ActionScript (Flash) developer, then Python and Java
     - as an architect not tied to one technology: the choice depends on business requirements and quality attributes
     - aims to be able to replace any developer in his team
     - strong soft skills with stakeholders and product owners, helped by a history degree; explains the system both to developers and to owners
     - then, at 00:08:51 (`/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:94`), five legacy-migration projects, two highlighted: a loyalty-system migration at Bank of Georgia, and a loyalty system plus a new integration layer for the old infrastructure at Pasha Holding in Azerbaijan
2. **Give a practical example: in which case did you contribute to reducing the risk exposure of an application, and through which decisions?**
   - "maybe it's better to have some practical example in which case you let's say contribute to the to reduce the risk exposure of an application with which decisions." (00:20:03, Antonio)
   - **Yaraslau's answer** (00:20:25, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:158`):
     - bank loyalty system: promo codes and QR codes arrive as a **file from a third-party provider**
     - decision: never load the file straight into the system or database; put it first into a **separate "DMZ" S3 bucket** for unverified content
     - a dedicated service **scans the file** for viruses and violations, and only then are the codes imported
     - principle: third parties are not trusted, every uploaded file is verified; he used the same pattern at Takamul in Saudi Arabia for files uploaded by users
     - sensitive data also has to be protected **in transit and at rest**
     - not covered: alternatives considered, how the decision was approved, measurable result

## Part 2 — application security, asked by Antonio

3. **In which way do you ensure security in transit?**
   - "in which way. So for example, to assure that there is security at transit." (00:23:11, Antonio)
   - **Yaraslau's answer** (00:23:27, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:162`):
     - most developers think of **HTTPS / TLS**, but TLS ends at each network hop, so the payload is unencrypted at the hops
     - two ways to get end-to-end protection: **SOAP with WS-Security** in older banking systems, and for REST **JWT with JSON Web Encryption (JOSE)**
4. **In HTTPS, what is the role of the certificate?**
   - "Yeah. So for the HTTPs, what is the role of certificate?" (00:24:30, Antonio)
   - **Yaraslau's answer** (00:24:38, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:166`):
     - the certificate lets the **client verify it is talking to the expected server**
     - **mutual TLS**: both client and server check each other's certificates; he used mTLS in mature systems and plain HTTPS in simple environments
5. **In mutual TLS, does the client hold the same certificate as the server, and what gets verified?**
   - "Okay, so the server. The server. The server as a certificate, the client has the same certificate that will be" (00:25:17, Antonio)
   - **Yaraslau's answer** (00:25:29, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:170`):
     - not the same certificate: the client has **its own certificate**, possibly issued by a **different certificate authority**
     - the server checks the client certificate and the client checks the server certificate
6. **You have a SaaS application and you want to authenticate against the identity provider of your Microsoft 365 tenant. What should you do?**
   - "Okay. And. And for authorization authentication of one application. So for example, I have imagine that I have a sas. Okay." (00:25:44, Antonio)
   - "And. I want to use my identity provider of my Microsoft 365 tenant. What I should do?" (00:26:05, Antonio)
   - **Yaraslau's answer** (00:26:23, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:178`):
     - set up an SSO broker such as **Keycloak** with the organization's directory (Active Directory) as the identity source
     - Keycloak verifies the identity there and **issues the token** the application uses
     - not mentioned: federating the SaaS directly with Microsoft Entra ID over SAML or OpenID Connect, which Antonio then told him is the customer's standard (question 8)
7. **And how do you handle API authentication and authorization?**
   - "Okay, good. And the API authentication or the API authentication way" (00:26:57, Antonio)
   - **Yaraslau's answer** (00:27:08, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:182`):
     - authentication works the same way: Keycloak issues a **JWT**
     - for authorization, three options for where roles and permissions live: as **claims in the JWT**, **in the service itself**, or **in Keycloak**
8. **In this customer's landscape there is no Keycloak — the application integrates directly with Microsoft Entra ID, which is the only identity provider allowed, so that accounts are not replicated and the organization's SSO and MFA apply. Do you have experience with that?**
   - "In this specific case, let's say for this specific case, I mean that customer landscape keycloak is not used is used direct direct integration with entry D [Entra ID]. Because yeah, this is the only identity provided provider allowed. So you don't have to connect other entity [identity] providers. So you don't have. You don't need to have a middleware let's say in the middle you design let's say this part of authentication authorization between an application that wants to be authorized authenticated to entry D [Entra ID]. Did you have some experience with that? So typically now in our case for example should be implement should be integrated with the entry ID [Entra ID] of the customer so that you don't have to replicate accounts. You have the SSAO [SSO and] MFA as defined by the organization, not by the SaaS. But also can happen that internal application should be connected to assure the SSO and MFA with the entra ID identity provider." (00:28:01, Antonio)
   - **Yaraslau's answer** (00:29:38 and 00:30:37, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:186` and `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:198`):
     - **no direct experience with Entra ID**, but experience with **Cognito and Keycloak**; SSO providers follow the same patterns, so Entra ID "will not be a problem"
     - agreed that the architect's job is to go with the organization's identity provider
     - added that providers differ in maturity (Keycloak more mature than Cognito), and the architect has to weigh such choices
     - Antonio's reply: the architect must follow the **approved design patterns**; a justified exception becomes a **technical debt** for the vendor (`/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:200-204`)
     - Yaraslau's view on business versus standards (`/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:222`): **business comes first**; if a pattern blocks a business requirement he would look for a workaround, another vendor or technology, and would even deviate from the pattern
     - his example of stakeholder work at Pasha Holding (`/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:232`): accounting, marketing, SRE and product owners, each needing "its own language"

## Part 3 — AWS security, asked by Donato

9. **You are responsible for improving the security posture of a web application hosted on AWS with a REST API and an RDS database. How would you proceed?**
   - "we can go more in detail. So let me think about this. Okay, so if you are responsible for improving the security posture of our web application, in this case hosted on AWS JS [AWS; the service name is not intelligible, see the note at the end of this file] with a REST API and an FDS RDS [RDS] database, how would you proceed?" (00:38:43, Donato)
   - **Yaraslau's answer** (00:39:08–00:44:28, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:242-246`):
     - Internet-facing API: add a **web application firewall**
     - check the **VPC and security group** configuration; **RDS in a private subnet**, sometimes behind a bastion host
     - **encrypt data with KMS**, with a customer-created key or a KMS-managed key
     - with more services: **zero trust** and **mutual TLS** between services in banking or finance
     - encryption in flight with **JSON Web Encryption** for REST, if high security is needed
     - check the API against the **OWASP Top 10**: authentication and authorization, JWT, role management, two-factor authentication, how OAuth 2 is implemented, credentials stored in Cognito or Keycloak
     - **least privilege**: users see only their own data (tenant protection) and no admin endpoints
     - **IAM least privilege** too: he often sees admin permissions on EC2 instance roles, which let anyone on the instance read data or delete other instances
     - then an off-topic story about a wrong AWS bill, which he himself called "a bit overloaded"
10. **You mentioned KMS. How do you manage KMS keys — do you have a suggestion?**
    - "So you mentioned also the kms. How to manage KMS keys. Do you have an idea suggestion?" (00:44:28, Donato)
    - **Yaraslau's answer** (00:44:44, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:250`):
      - KMS **costs money per call**
      - option 1: create **your own keys** and encrypt data yourself without calling KMS each time (cheaper)
      - option 2, the most secure: **call KMS every time**, at a higher monthly bill
      - not mentioned: customer-managed versus AWS-managed keys, key policies, envelope encryption with data keys, separation of duties
11. **And what about the rotation of the keys?**
    - "And what about the rotation of the keys?" (00:45:42, Donato)
    - **Yaraslau's answer** (00:45:46, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:254`):
      - asked back in which situation rotation is meant
      - rotating a key that encrypts RDS data means tracking which key encrypted which row, so he would **avoid key rotation and rotate credentials instead**
      - not mentioned: KMS **automatic key rotation**, which keeps the old key material so existing data still decrypts, without tracking keys per row
12. **What do you know about the web application firewall: which controls would you deploy for an Internet-facing application, and how would you operate those controls?**
    - "Okay, okay. Now let's go back to the security topic. I want to understand what you know about the WAF" (00:46:34, Donato)
    - "Yeah. Which controls would you deploy for Internet facing application and how would you operate them?" (00:46:48, Donato)
    - **Yaraslau's answer** (00:47:12 and 00:47:52, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:266` and `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:270`):
      - asked first whether there is a CDN in front of the application (questions 25 and 26)
      - functions on the CDN can do first-line checks, but cannot handle **SQL injection or XSS**
      - so a **WAF with signature-based rule sets** against the OWASP classics
      - not covered: how he would operate the controls (count mode first, tuning false positives, WAF logging, rate-based rules, managed rule groups)
13. **So you would add the managed rule groups plus application-specific rules?**
    - "Okay, so you will add the rule groups and other application specific rules." (00:48:54, Donato)
    - **Yaraslau's answer** (00:49:02, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:274`):
      - one line only: "I would use the rule set"
14. **You mentioned a CDN, so let us talk about CloudFront: why would you place CloudFront in front of the application, and how would you prevent traffic from reaching the origin directly, bypassing CloudFront?**
    - "but the rule set. So you mentioned the cdn so probably we can talk about Cloudfront. So why would you place cloud front in Kubernetes [in front of the] application? And how would you prevent directory gene [direct origin] access for example?" (00:49:06, Donato)
    - **Yaraslau's answer** (00:49:24, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:278`):
      - CloudFront for **static content** and users worldwide: caching at edge locations means **lower latency**
      - **Lambda@Edge** for light changes to headers and payloads
      - not answered: the second half, how to stop direct origin access (see the note at the end of this file)
15. **On CI/CD pipelines: how would you establish continuous vulnerability management for the application, the container hosts and the dependencies?**
    - "Okay, clear, Clear. Now let's go to another topic which is related to CI CD pipelines. How would you establish continuous vulnerability management for application container hosts and dependencies?" (00:50:18, Donato)
    - **Yaraslau's answer** (00:50:40, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:286`):
      - start with **SAST** in the pipeline
      - **dependency vulnerability checks** and code checks for **leaked passwords and secrets**
      - tools: **SonarQube**, Checkstyle and similar plugins
      - **block the merge** when the security checks find vulnerabilities
      - not covered: container image scanning, scanning of the hosts, continuous re-scanning after deployment
16. **Pushback on blocking every merge: for a minor version, could the control be skipped?**
    - "Yeah, this is a strictly thing to say. Probably for minor version we can skip the control" (00:51:58, Donato)
    - **Yaraslau's answer** (00:52:07, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:290`):
      - skipping it for minor versions means that at the next **major version** you face "a big bunch of outdated dependencies", so he kept the control
17. **How would you design centralized security logging and auditing across several AWS accounts and regions?**
    - "Okay, now let's see. We were discussing before about the audit. So how will you design a centralized security logging and audit across AWS accounts and regions? So we have a big application across multiple accounts and regions. We want to retrieve centralized to a decentralized log [that is, collect the logs of the separate accounts into one place]." (00:52:20, Donato)
    - **Yaraslau's answer** (00:52:58, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:294`):
      - **CloudWatch Logs** as the primary option, **X-Ray** for tracing
      - not mentioned: CloudTrail organization trail, a central log archive account, AWS Config, Security Hub, GuardDuty
18. **And how do you manage that cross-account logging?**
    - "Okay, and now you manage this cross account login [logging]." (00:53:21, Donato)
    - **Yaraslau's answer** (00:53:28, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:298`):
      - a clarifying question instead of an answer: does "multiple accounts" mean test and production accounts under one organization? (question 27)
19. **Clarification of question 18: the accounts are separated per application, not per environment — application A in account A, application B in account B.**
    - "Let me say different accounts not by environment by, but by application. So you have application A hosted on account A and application B hosted on" (00:53:43, Donato)
    - **Yaraslau's answer** (00:53:57 and 00:55:03, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:302` and `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:306`):
      - "Pretty tough question"; separate CloudWatch set-ups would mean checking two consoles
      - "I don't remember exactly", but with **AWS Organizations** a **single dashboard** could give access to the logs of each application
      - the accounts have to be united in one organization
      - Donato's correction (`/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:314`): start from the organization, then add **GuardDuty** and other services; Yaraslau: "I forgot about guardduty"

## Part 4 — methodology, asked by Antonio

20. **When you are asked to design a solution, what are the macro steps you follow, from collecting the requirements to the final technical design document approved by an external architecture review board?**
    - "Some other, let's say, more methodological questions. So when you are asked to design a solution. Okay. What are the steps that you follow? The macro steps during your journey. Okay. From the collection, the requirements to the final technical design document to be approved, for example, by an external architecture review board." (00:56:06, Antonio)
    - **Yaraslau's answer** (00:56:57–01:02:45, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:328-332`):
      - **1. Observation (day one)**: five questions: the business problem, how stakeholders see the result, why they think it is a problem, who the end users are (services or people), when the result is needed
      - the **business analyst** collects business requirements and use cases in parallel, in **workshops** and sometimes **questionnaires**; everything goes into **Confluence** from day one
      - he picks up the **non-functional requirements** and builds a **glossary**, so business and developers use the same words
      - **2. Scope of the document**: a full **architecture vision document** or a lighter version
      - collect **architectural drivers and concerns**: risks, assumptions, use cases, constraints (legal, business), **quality attributes**
      - **3. Diagrams**: **C4** (mostly context and container levels), plus flow, data and **deployment diagrams**, which are especially valuable in the cloud
      - **4. One document**: the architecture vision document, called a "solution defense document" in some banks
      - **5. Solution defense**: assessment by the company's other architects and final approval by the **enterprise architect**
      - **6. Implementation**: teams build it while he guides them and keeps the documents and diagrams up to date as the business changes requirements
      - **7. End**: helps the teams doing **security and penetration testing**, and prepares the final documentation
      - Antonio: "More or less aligned with our process"; Yaraslau: "a little bit with TOGAF"; Antonio then described the customer's TOGAF-based Enterprise Architecture Team, the LeanIX catalogue and the gates G0, G3 and G5 (`/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:338` and `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:346`)
21. **Do you have any questions or clarifications for us?**
    - "For me is enough. I don't know if you have some other. Also if you want to ask us some other questions or that clarification. I don't know." (01:07:06, Antonio)
    - **Yaraslau's answer** (01:07:22, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:352-366`):
      - no question about the role
      - went back to the CI/CD question: he had forgotten to mention **HashiCorp Vault** for secrets management; Antonio confirmed Vault is another component of the customer's catalogue

## Part 5 — clarifying questions the candidate asked back

These are the questions Speaker A, the candidate Yaraslau Dzmitryieu, put to Antonio and Donato. They are worth keeping separately, because in an architecture interview the clarifying question is itself part of the assessed answer.

22. **Would that migration experience fit the position you are looking to fill?**
    - "So I suppose that experience would satisfy you and position which you are looking, which we are looking at right now. What do you think?" (00:08:51, candidate)
    - **Antonio's reply** (00:10:32–00:13:23, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:96-104`):
      - not a yes or no; he described the role instead: an architect to improve the **security hardness** of the customer's AWS applications
      - two kinds of applications: **legacy** ones built before any security guidelines existed, and **recent** ones blocked by **technical or security debt** against the organization's standards
      - the architect suggests the best way to remove that debt, using AWS services and their configuration
      - Yaraslau's follow-up (`/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:106-110`): AWS Developer and Solutions Architect Associate certifications, aiming for Professional; first step would be to **gather everything about the system**: documentation, service maps, API contracts, security map, deployment map
23. **Is the system currently running in production?**
    - "Also I need to ask an additional question. This system, it's currently working in production, right?" (00:14:05, candidate)
    - **Antonio's reply** (00:14:30, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:112-140`):
      - "Yes, yes, absolutely"
      - the **security team has already assessed** a set of solutions and produced a **prioritized list** of findings, for example a missing WAF, Internet exposure, no VPC configured (Yaraslau: this is close to the **OWASP Top 10**, and any AI-produced findings should be verified by a human)
      - the list is **not the architect's job**: the architect designs how to remove or reduce each issue, and **another team implements it**
24. **Confirm that the primary goal is to deal with the security audit, so that security is the primary quality attribute — because prioritising security means maintainability and performance may be sacrificed.**
    - "I need Antonio, I need to double confirm that. So the primary goal is to deal with the security audit. So security is the primary quality attribute." (00:18:43, candidate)
    - "Of this system. Okay. You know, I'm asking that because in my career, every single time we have some trade offs and if we put the security in the first place, it means that maybe maintainability, performance, etc. Can be sacrificed in the owner of security." (00:18:59, candidate)
    - **Antonio's reply** (00:18:59 and 00:19:25, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:144` and `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:148`):
      - security as the primary quality attribute: "Absolutely"
      - whether maintainability or performance may be sacrificed: "This depends. Depends on the specific application."
25. **Confirm the scope of the WAF scenario: are we still talking about the small REST application deployed on EC2 or Fargate?**
    - "So we are still talking about our small rest deployed application on some EC2 or Fargate, right?" (00:47:00, candidate)
    - **Donato's reply** (00:47:10, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:264`):
      - "Okay. Yeah, yeah." — the same application
26. **Is there a CDN in front of the application or not?**
    - "So with web application firewall, Let me think. So with this simple application. We can utilize basically two different approaches here. First of all, do we have some CDN there or not?" (00:47:12, candidate)
    - **Donato's reply** (00:47:44, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:268`):
      - "We can add the CDN, it's not a problem"; he later built question 14 on that CDN
27. **Confirm the meaning of "multiple accounts": separate AWS accounts for test and production, united under one organization?**
    - "You mean that we have multiple accounts like test account, prod account, all within different AWS accounts, utilized or unified under the simple organization." (00:53:28, candidate)
    - **Donato's reply** (00:53:43, `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:300`):
      - no: the accounts are split **by application**, not by environment (question 19)

## Topics the interviewers raised that were not phrased as questions, but are likely to return

- **The customer's architecture governance**, described by Antonio at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:338` and `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:346`: an Enterprise Architecture Team following TOGAF, a catalogue tool transcribed as "Linux" and almost certainly SAP LeanIX, holding solution outline documents, diagrams, reusable components and approved design patterns, and a gate approval process — gate G0 for the conceptual solution, gate G3 for the low-level design, gate G5 for go-live.
- **The expectation that an architect follows the design patterns already approved by the organization**, and only deviates with an acceptable justification, which then becomes a recorded technical debt for the vendor to solve — Antonio at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:200` and `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:204`.
- **The architect as the mediator between the business team and the IT functions** — security, identity and access management, networking — where a decision can take months in a large, bureaucratic organization: Antonio at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:220` and `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:230`.
- **Secrets management with Vault**, which the candidate raised himself at the very end as a missing part of his CI/CD answer, and which Antonio confirmed is another component of the customer's catalogue: `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:352` and `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:358`.
- **AWS GuardDuty**, named by Donato at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:314` as the piece the candidate missed in the centralized logging answer: the organization comes first, then GuardDuty and the other services on top.

## Note on three terms that the transcript does not resolve on its own

**"directory gene access"** in question 14. Two readings are possible, and the first is far more likely.

*Direct origin access* — the question being "how would you prevent direct origin access", meaning how do you stop a client from bypassing CloudFront and calling the origin (the S3 bucket, the load balancer or the EC2 instance) directly. This reading fits phonetically, because "direct origin" collapses into "directory gene" far more naturally than any alternative; it fits the sentence, because it is the standard second half of the CloudFront question whose first half Donato has just asked; and it fits the role, because bypassing the CDN also bypasses the web application firewall attached to it, which is precisely a security-posture finding. The expected answer: for an S3 origin, **Origin Access Control** (the modern replacement for the legacy Origin Access Identity), with a bucket policy that allows only the CloudFront distribution and blocks public access; for a load balancer or EC2 origin, a **secret custom header** injected by CloudFront and enforced by a WAF rule or a listener rule on the load balancer, combined with **security groups restricted to the AWS-managed prefix list `com.amazonaws.global.cloudfront.origin-facing`**, so the origin only accepts connections coming from CloudFront.

*Directory listing access* — the question being how you stop a web server or an S3 static website from returning an index of the files in a directory when no default document exists. The expected answer would be to disable directory listing on the origin, set a default root object on the CloudFront distribution, and keep the S3 bucket private behind Origin Access Control rather than serving it as a public website endpoint. This reading is grammatical but phonetically much weaker, and it is a less natural follow-up to "why would you place CloudFront in front of the application".

The candidate never answered the second half of the question — his reply at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:278` covers only caching, latency and Lambda@Edge — so the transcript gives no further clue. Settle it by listening to `https://app.bluedothq.com/preview/6ab64ec38b7f2b9d935d5412` at 00:49:06. Prepare the Origin Access Control answer first and mention the default root object second, and the question is covered under either reading.

**"AWS JS"** in question 9. No AWS service is named "JS". Donato is naming where the web application is hosted, so the word after "AWS" is a service name the transcriber failed on. The three readings that fit, in order of likelihood: **EKS**, the Elastic Kubernetes Service, because Donato asked the other candidate the same day how to secure applications running on EKS, per question 3 of `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/04-interview-questions-Siarhei-Sharykhin-phase1.md`, and because the transcriber also turned the word "front" into "Kubernetes" in question 14 of this file, which shows the model was primed on Kubernetes vocabulary in this passage; **ECS**, the Elastic Container Service, which the candidate's own follow-up hints at when he asks at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:262` whether the application sits "on some EC2 or Fargate" and Donato accepts that framing without correcting it; or simply **AWS** with no service named at all, the transcriber having produced "JS" from noise. The question works identically under all three readings, because what is asked is how to improve the security posture of a web application with a REST API and a relational database on AWS.

**"FDS"** in question 9. There is no AWS service abbreviated FDS. The phrase "an FDS RDS database" is a false start that the speaker corrects within the same breath, so the database is **Amazon RDS**, the Relational Database Service.
