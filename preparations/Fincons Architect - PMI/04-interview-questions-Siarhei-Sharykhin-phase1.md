# Fincons Architect (PMI) phase 1, second candidate — questions asked

Questions extracted from `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/03-interview-transcript-Siarhei-Sharykhin-phase1.md`, the transcript of the phase 1 interview recorded 2026-09-25, source `https://app.bluedothq.com/preview/6ab67aa0fa0a6b005d5ce6a2`, duration 50 minutes 55 seconds.

Speakers in that transcript: **Speaker A** is Donato, who opens by introducing himself as a solution architect and stating the scope of the role at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/03-interview-transcript-Siarhei-Sharykhin-phase1.md:28`, and who waits for Antonio at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/03-interview-transcript-Siarhei-Sharykhin-phase1.md:24`; **Speaker B** is Antonio, handed the interview by Donato at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/03-interview-transcript-Siarhei-Sharykhin-phase1.md:84`; **Speaker C** is the candidate, Siarhei Sharykhin, who introduces himself as Sergey at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/03-interview-transcript-Siarhei-Sharykhin-phase1.md:30`.

Note that the two interviewers carry different speaker letters in the two transcripts of this process: in `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md` Donato is Speaker C and Antonio is Speaker B, while in `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/03-interview-transcript-Siarhei-Sharykhin-phase1.md` Donato is Speaker A and Antonio is Speaker B.

Each entry gives the general idea of the question in full form, then the exact wording from the transcript with its timestamp. The transcript is auto-transcribed, so the quoted wording is kept exactly as the transcriber produced it, and the correct term is added in square brackets immediately after each garbled one — the convention for correcting a quotation without destroying it. What the garbled terms mean:

| As transcribed | What was actually said |
| --- | --- |
| "Daniel does attacks", "the Daniel DOS attack" | DDoS attacks, that is distributed denial-of-service attacks |
| "the AWS field" | AWS Shield, the managed DDoS protection service |
| "incompetencies with this guideline" | inconsistencies with this guideline |
| "the draw IO" | draw.io, the diagramming tool |
| "some adoption, existing application to comply" | adaptation of existing applications so that they comply |
| "Amazon yes year service" | Amazon ECR, the Elastic Container Registry |
| "umail diagrams", "YAML diagrams" | UML diagrams |
| "mirror" | Miro, the collaborative whiteboard |
| "right Helen", "right hand application like Uber" | ride hailing, a ride-hailing application like Uber |
| "IP gateway" | API Gateway |
| "CDC ICD pipelines" | CI/CD pipelines |
| "Gitlix" | Gitleaks, the open-source scanner for hard-coded secrets in a Git repository; the second name in the same sentence, "Split", is unresolved and is most plausibly Spectral or git-secrets |
| "UTTCT service discovery" | etcd, the distributed key-value store, used as the service registry |
| "migrated to console" | migrated to HashiCorp Consul, the service discovery and service mesh product |
| "Venom test" | Venom, the declarative end-to-end testing tool |
| "VTC private network" | VPC, the Virtual Private Cloud |

## Part 1 — opening and stakeholders, asked by Donato

1. **Should the candidate introduce himself?** — asked by the candidate after Donato's own introduction and description of the role, and answered in the affirmative.
   - "Okay, so should I introduce myself? Right, yeah, yeah." (00:06:12, candidate)
2. **What is your experience with stakeholders — tell me about a problem you fixed?**
   - "Okay, thank you for this introduction. And what is your experience with the stakeholders? So tell me about your experience. Maybe some problem that you fix and stuff like this." (00:08:29, Donato)

## Part 2 — AWS security, asked by Donato

3. **How would you secure applications running on AWS EKS?**
   - "Okay, okay, good, because we have also we need also a solution actor for building diagrams and managing the stages of the development, the life cycle. Okay, now let's focus more on the security part. So how would you secure Applications running on eks. So AWS EKS I got." (00:12:31, Donato)
4. **How will you manage the secrets, the API keys and the certificates — you mentioned a secret manager, can you go deeper?**
   - "Okay, okay. And how will you manage the secrets, the API keys, the certificates you mentioned before? Secret manager can go deeper in detail" (00:17:39, Donato)
5. **Describe a secure VPC architecture for critical workloads: what are the main components of a VPC and how do you secure them?**
   - "Yeah, it's clear, it's clear. Now let's go on the networking part. So please describe a secure VPC architecture for critical workloads, what are the main components of VPC, how to secure, etc. Etc." (00:19:25, Donato)
6. **Tell me about security groups.**
   - "Okay, and tell me something about the security groups." (00:20:54, Donato)
7. **How will you design enterprise logging and auditing?**
   - "Okay. Okay, good. Now, okay, we talking about the network. Let's go to the audit topic. So how will you design enterprise logging and auditing?" (00:21:28, Donato)
8. **Rephrased after the candidate asked what was meant: which AWS tools will you use to achieve logging and auditing of critical logs?**
   - "Well, what are the tools that you will use on AWS to achieve the logging and auditing of critical logs?" (00:21:50, Donato)
9. **How will you protect applications from DDoS attacks and layer 7 attacks, and which AWS services give you that protection?**
   - "No, I think that nothing came to my mind. Yeah, it's a good response. Okay, now let's go back to the security topic. How will you protect applications from Daniel does [DDoS] attacks and layer seven attacks? So what are the tools that the layer seven attack? So on you have from the network perspective you have multiple levels and you have the layer 7. So it's similar to the Daniel DOS [DDoS] attack. I want to know what are the services that AWS gives to you to achieve this?" (00:22:47, Donato)
10. **You mentioned the web application firewall; there is another one, AWS Shield — have you ever used it?**
    - "So you mentioned the web application firewall. Yeah, we have another one, the AWS field [AWS Shield]. I don't know if you ever use it." (00:24:37, Donato)
11. **You inherit 10 AWS applications with a poor security posture. Describe your 90-day remediation plan.**
    - "Okay, okay, now last one from my side. So let's assume that you inherit 10 AWS applications with with poor security posture. Describe your 90 day remediation plan." (00:24:51, Donato)
    - Rephrased after the candidate asked for a repeat: "You have now 10 AWS application with poor security. Okay, so now you need to improve this security and you have 90 days to do it. So." (00:25:15, Donato)

## Part 3 — methodology, governance and delivery, asked by Antonio

12. **What is your way of working when you have to design a new solution?**
    - "Yes. So what is the pro the way of working that you follow when you have to design a new solution?" (00:29:45, Antonio)
13. **Did you ever manage external approvals from other teams of the organization — an architecture review board, the security team, networking and so on?**
    - "Okay, so. Did you manage for example some external approvals from other teams of the organization? For example from approvals from architecture review board or from the security team, networking and so on?" (00:32:59, Antonio)
14. **You designed a solution following the organization's IT and architecture guidelines as far as possible, but part of the solution turns out not to be compliant with those guidelines. What do you do to address that?**
    - "Okay, so assuming that, assuming that you have a solution, okay. And based on the IT guideline or architecture guideline of the organization, there is some part of this, of this solution that is not properly compliant. Okay. What you do, what do you think to do to be so to. To to address these points. So for example you created, you designed a solution or trying to follow as much as possible the, the guidelines from the architecture team. Okay but at some point you find that there are some incompetencies [inconsistencies] with this guideline. What, what you do in that case." (00:34:23, Antonio)
15. **You are used to working with containerized applications, right?**
    - "Okay. You are used to work with the containerized application, right?" (00:38:17, Antonio)
16. **In which way do you scan Docker images to be sure there are no security issues in the code or in the base image?**
    - "Yeah. So typically you have. You deploy some containerized application using Docker, for example, and so on. So Docker image and so on. What are, let's say the. In which way you perform the scanning of these images to be sure that there are no security issues or some issues related to the code or the image of the machine that you are using in your Docker." (00:38:35, Antonio)
17. **Do you know the names of the scanning tools you just referred to?**
    - "do you know some tools that you have mentioned?" (00:39:44, Antonio)
18. **During development, what kinds of test do you plan?**
    - "Okay. And I don't know, during let's say the development you planned, what kind of test" (00:41:11, Antonio)
19. **When you design a solution, which tool do you use to document the solution?**
    - "Okay. And when you design a solution, what tool you use in terms of let's say to document your solution?" (00:42:06, Antonio)
20. **Do you also use draw.io for the diagrams?**
    - "Also yeah, you use the draw IO [draw.io]" (00:42:54, Antonio)
21. **Do you have questions for us?**
    - "Okay. Okay. No other question" (00:43:23, Antonio), followed by "Yeah, you have question." (00:43:32, Antonio)

## Part 4 — clarifying questions the candidate asked back

These are the questions Speaker C, the candidate Siarhei Sharykhin, put to Donato and Antonio. Questions 22 and 23 are clarifications of an interview question; questions 24, 25 and 26 are the candidate's own questions about the role.

22. **What do you mean by "how"?** — asked about the enterprise logging and auditing question.
    - "What do you mean how?" (00:21:47, candidate)
23. **Could you repeat or rephrase the question?** — asked about the 10 applications and the 90-day plan.
    - "Sorry, could you repeat the question or rephrase? I didn't get it." (00:25:11, candidate)
24. **Can you explain in more detail what the role involves in terms of security and applications?**
    - "Yeah, I have few questions if you don't mind. At the beginning you mentioned that this role would involve not a lot, but there were many questions about security stuff that there would be some adoption [adaptation of], existing application to comply, some security. Maybe you can, if that's possible, you can explain a little bit more about what that role would involve in terms of security and applications." (00:43:34, candidate)
25. **Where did the need come from — signals from an audit, or an internal wish to be aligned with the most secure practices?**
    - "And why did it appear you got some signals from let's say audit or just because you were aware that there were some issues and you want just to be aligned with the most security ways." (00:46:17, candidate)
26. **Is there a long-term vision with deadlines for when the security issues must be closed, or is the work iterative?**
    - "And do you already have like a long term vision, for instance for the following halfway on a year, what part should be already closed in terms of security? Or it just like the way to start iteratively fix security issues and see how it goes. I mean if there are any deadlines regarding when this security issue should be closed." (00:47:31, candidate)

## What the interviewers said about the role — the answers to questions 24, 25 and 26

These answers are the most valuable part of the transcript for preparation, because they state the role's scope in the interviewers' own words.

- **The nature of the work**, Antonio at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/03-interview-transcript-Siarhei-Sharykhin-phase1.md:150`: the customer has several cloud solutions where the security best practices were not always followed — a missing web application firewall, a security group allowing more traffic than required, cryptography done with a self-signed certificate rather than a certificate issued by the organization — and the work is partly hardening and partly complete redesign, mostly on legacy solutions or on solutions that were moved from an on-premises platform to the cloud by a lift-and-shift migration without the corresponding attention.
- **Where the findings come from**, Antonio at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/03-interview-transcript-Siarhei-Sharykhin-phase1.md:154`: periodical security assessments, plus security debts recorded during the original design, plus the output of scanners and checks.
- **The deadline and the division of labour**, Antonio at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/03-interview-transcript-Siarhei-Sharykhin-phase1.md:158`: the list of applications to secure is long and the main deadline is the end of 2027; the architect explores a solution, designs how to solve its issues and hands the recommendation over, and other internal teams of the organization implement the design. Antonio repeats the same division at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/03-interview-transcript-Siarhei-Sharykhin-phase1.md:162`, adding that which team implements depends on the finding — a networking finding such as too many firewall rules or an over-permissive security group is acted on by the networking side, without the application being touched.
- **Technical debt and security debt as the accepted mechanism**, Antonio at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/03-interview-transcript-Siarhei-Sharykhin-phase1.md:102`: when a design cannot be made fully compliant with the organization's standards, a technical debt or security debt is opened with a plan to solve or mitigate it within weeks or months. This matches what Antonio told the other candidate at `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/01-interview-transcript-Yaraslau-Dzmitryieu-phase1.md:204`.

## How this interview differs from the first one

Both interviews were conducted by the same two people, Donato and Antonio, on the same day, and both follow the same two-part shape: Donato asks the hands-on AWS security questions, then Antonio asks the methodological and governance questions. The overlapping topics, which are therefore the ones most likely to be asked again, are the AWS security posture of an existing application, secrets and key management, the web application firewall, centralized logging and auditing, CI/CD security scanning, the design process from requirements to an approved design document, and the handling of a solution that does not comply with the organization's approved patterns.

Topics asked only of this candidate: securing applications on AWS EKS (question 3), a secure VPC architecture and security groups (questions 5 and 6), DDoS and layer 7 protection with AWS Shield named explicitly (questions 9 and 10), the 90-day remediation plan for 10 inherited applications (question 11), Docker image scanning (questions 16 and 17), test planning (question 18), and documentation tooling (questions 19 and 20).

Topics asked only of the first candidate, in `/home/viktar/Projects/Support/preparations/Fincons Architect - PMI/02-interview-questions-Yaraslau-Dzmitryieu-phase1.md`: the role of the certificate in HTTPS, mutual TLS, authenticating a SaaS application against a Microsoft 365 tenant's identity provider, direct integration with Microsoft Entra ID, KMS key management and key rotation, and CloudFront with directory listing prevention.
