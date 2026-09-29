# Siarhei-Sharykhin-CV-Go-Golang-Java-Fincons-Group-20260925-095935

- Source: https://app.bluedothq.com/preview/6ab67aa0fa0a6b005d5ce6a2
- Recorded: 2026-09-25T13:44:00.084Z
- Duration: PT50M55S
- Language: en

## Transcript

**[00:00:00] Speaker A:** It.

**[00:00:51] Speaker B:** That.

**[00:01:21] Speaker C:** Hi. Hello.

**[00:01:25] Speaker B:** Hello everyone.

**[00:01:27] Speaker C:** Hi, how are you?

**[00:01:31] Speaker A:** All good? All good. Nice to meet you.

**[00:01:34] Speaker C:** Nicely meet you too.

**[00:01:37] Speaker A:** Let's wait for Antonio. Okay. I think we can slowly start.

**[00:05:21] Speaker C:** Yeah, sure.

**[00:05:24] Speaker A:** Okay, so first of all, myself, I'm rolling, I'm a solution architect, a lot of experience on the Service or Node JS, Python, etc. Etc. And so we are searching for security Solution architect and the main goal of the main scope of this architect is to help the migration of some. Not migration, check if some architecture are good or not from security point of view.

**[00:06:12] Speaker C:** Okay, so should I introduce myself? Right, yeah, yeah. My name is Sergey. In general, I've been working in IT sphere for around 14 years. During the time I had opportunity to work in different domains like ride hailing, my recent project, Social engagement, fintech and etc. I started from technical perspective. I started as full Stack engineer with primary PHP as primary language on backend. Then I got acquainted with Node js, Golang and also got opportunity to deeply work, especially with Golang. And during that experience I was always eager to take part into, you know, some kind of architectural decision and issues because for me it was every time it was very interesting to find a right approach depending on the trade offs I had. And finally at my recent project, I got opportunity to work as solution architect. That was a ride-hailing application like Uber, but it was operating in France and some African country. At the company I've been working for around five years as solution architect. In my responsibility I was responsible for providing some final solution for implementing different features, different architecture approaches, what kind of technologies and resources to use. When I joined the company, it already used Amazon. That's why I had to work with Amazon cloud provider. And yeah, probably that's the brief introduction regarding team, huge teams. Usually when I took part in different projects, usually teams were not very big around maybe four or five backend developers, few front end mobile depending on the project and then on demand they could be connected to some data analytics or designers and yeah, probably that's the very brief introduction.

**[00:08:29] Speaker A:** Okay, thank you for this introduction. And what is your experience with the stakeholders? So tell me about your experience. Maybe some problem that you fix and stuff like this.

**[00:08:45] Speaker C:** Yes. So in my recent role as solution architect, I had to communicate very closely not only with product, but also with stakeholders for different issues. One of them for instance was a deep integration around HubSpot. Stakeholders and care team, even acquisition team were really interested on integrating our application into HubSpot. When a driver makes a sign up, they wanted to take a lead and Check the flow from the moment driver started the snap process to the moment driver made the first ride. That's why first what I did, I was guarding all the requirements from stakeholders because there was not only one guy, there were a few guys and product and stakeholders, they had slightly different vision. From the product perspective it was not very critical issue. But after communicating with stakeholders I realized that for them it was extremely important. So I gathered the requirements of let's say features that must be implemented first and some that nice to have or something that can be follow up with that requirement later. I went to HubSpot documentation to see what kind of API it provides. How to properly map our domain entities into, let's say, entities that HubSpot provided. So fortunately to me that quite a big system, the API was clear with all the details, so I didn't face any difficulties while I was sourcing. And then finally I created some kind high level diagram mostly for stakeholders. I did it in Miro with some nice block in different color because I wanted to show them how it would look like that integration with partially technical perspective. And partially they understand some implication because so they understand that there could be some kind of eventually consistency stuff that a contact on hubbot may appear with some delay in case of some reload and stuff like that. And then I created UML diagrams based on the code base because it was not super big company and I worked closely with DevOps so I had access with code base. I had pretty good context regarding all the stuff, codebacks, microservices, communication contracts. That's why I created few UML diagrams and came to engineer team with the idea how it could be implemented. And then during the discussion there were some back and forth with some feedback because I remember dev guys shared some concerns regarding unique constraints how to look like. Because in our system driver can be not only driver, but it can be also a fleet manager and has its own company and driver can drive is his own company. So it caused some more back and forth questions which I clarified with stakeholders. But finally yeah, we came to agreement to the final solution and then engineer team implemented it. I was also take part in some code review because I was interested how it would be implemented in the end. But yeah, with a couple of iterations I guess the vast majority of the requirements were covered and fortunately with no big issues.

**[00:12:31] Speaker A:** Okay, okay, good, because we have also we need also a solution actor for building diagrams and managing the stages of the development, the life cycle. Okay, now let's focus more on the security part. So how would you secure Applications running on eks. So AWS EKS I got.

**[00:13:00] Speaker C:** So there are different ways from. Let's start from the lower level and then go up. So from the code perspective there are different tools that analyze your code that can provide some scanning for vulnerabilities, check for whether the versions that are used in different packages are pinned or not. So that's the first part. This kind of tool can be really easily integrated into CI CD pipelines. So that's probably the simplest stuff because there are many already services and packages for any languages. That's why it's pretty simple. Then there are some. If we go one level up there shouldn't be any hard coded keys or secrets or stuff like that. So that's not that extremely important. One of the most important stuff of course there are also some tools like Gitleaks or Split stuff like that. That's why it's pretty easy to analyze it. But it's very important to develop your application with the design and keeping in mind that all the secrets should be managed secret manager like in my particular case it was used vault but there are other services for when it comes to Amazon it can be used like email service or something like that. Then if we go upper we comes to some kind of networking so we need to define how our application is exposed to external world whether we need what kind of networking we need, what endpoints we should expose and how. In my particular case there was API Gateway where I implemented rate limiting stuff authentication authorization so that's that already allowed to secure. When it came to kubernetes I don't exactly remember if there was something super particular regarding kubernetes because the kubernetes itself was managed by DevOps but of course, at least from the DevOps perspective from time to time I had contact with them regarding if there are any security patches that should be applied or maybe something that we need to take care of maybe some to migrate from RAM service discovery to another. At the beginning it was if I'm not mistaken a standard etcd service discovery used Then it was migrated to Consul and yeah, that's mostly it. Of course I also took into consideration the general Amazon service like to manage the roles who even from membership perspective who should be able to do what and from even application point of view they were also implemented Some not a roles but at least yeah, some sort of a roles. For instance admin operator could get access to everyone but from driver's perspective or passenger perspective or on the design it was. Yeah, it was forcely implemented that one user can't access information from another user. I also played around I had some SMS pumping attack and it was very interesting experience and there were different solution applied. One of them I played around with Amazon firewall service worked pretty well because it came with already some ability to identify the DoS attacks to identify both suspicious activity but unfortunately it costed a lot. I remember that it was quite expensive and the result was not so nice as I expected and in comparison to cost here finally with DevOps and product like I came to agreement with them not to use it because I introduced some other security levels. Actually the vast majority was covered by recaptcha with the extensive configurations that allowed product via launchdarkly flag to configure different configuration like what kind of score or SMS score is allowed for what kind of country for instance in Africa.

**[00:17:39] Speaker A:** Okay, okay. And how will you manage the secrets, the API keys, the certificates you mentioned before? Secret manager can go deeper in detail

**[00:17:55] Speaker C:** so secrets should be stored in this kind of secret management tool. Then if we need we need to think over about maybe rotation how we are going to rotate for instance it's also important to understand if there are some ongoing applications that actively use secrets, not something that is only grabbed on spin and run. If there is applications that are actively with some secrets I also need to take into account how to properly provide the value. For instance if there is a new version and I need to provide it, maybe I can follow more or less the same kind of what feature flag does. So if there is a request from one version I should take a look and return one secret. For another version I should return another value. When it comes to Amazon I didn't like dive deep into its services around secret management, but I think there are some it shouldn't provide some secret stuff to play around with like KMS maybe configuration provider. I guess that kubernetes also should have some good integration with that services. Yeah, probably something like that.

**[00:19:25] Speaker A:** Yeah, it's clear, it's clear. Now let's go on the networking part. So please describe a secure VPC architecture for critical workloads, what are the main components of VPC, how to secure, etc. Etc.

**[00:19:47] Speaker C:** Unfortunately I didn't have very deep practice in it but overall when we defined VPC private network so we should define what should be in terms of aws. We should define like whether it should be multi zone VPC or it should be tied to a specific zone. Then we can define what should be exposed onto the Internet and what should remain inside your vpc so for instance, if there are communication between services and they are not exposed to Internet, so they should live in their own private network that nobody can reach them apart one that we allowed. And as far as I know Kubernetes service has pretty good integration with Amazon VPC service. So where you can define all the stuff with subnets if needed, with Internet facing balancers and stuff like that.

**[00:20:54] Speaker A:** Okay, and tell me something about the security groups.

**[00:20:58] Speaker C:** Security group provides you a set of rules where you can define what exactly can be exposed. For instance, which exact port can be exposed and for whom. You can expose a subset of ports for another for a subset of services or even for the whole Internet. And by using this security group so you can define like some kind of level access.

**[00:21:28] Speaker A:** Okay. Okay, good. Now, okay, we talking about the network. Let's go to the audit topic. So how will you design enterprise logging and auditing?

**[00:21:47] Speaker C:** What do you mean how?

**[00:21:50] Speaker A:** Well, what are the tools that you will use on AWS to achieve the logging and auditing of critical logs?

**[00:22:01] Speaker C:** So overall, so AWS provides some well defined services like CloudWatch, Amazon X Ray for tracing and you can use mostly cloud watches used for logging. And then probably you can use some other service if I'm not mistaken, it's called cloud trail for analyzing. Yeah, and yeah, and then again you can define the rules for Amazon X Ray. You can define and monitor all the tracing information. So what else?

**[00:22:47] Speaker A:** No, I think that nothing came to my mind. Yeah, it's a good response. Okay, now let's go back to the security topic. How will you protect applications from DDoS attacks and layer seven attacks? So what are the tools that the layer seven attack? So on you have from the network perspective you have multiple levels and you have the layer 7. So it's similar to the DDoS attack. I want to know what are the services that AWS gives to you to achieve this?

**[00:23:38] Speaker C:** So first that actually yeah I had experience with is Amazon firewall service that already provides detection of the dose and some other rules. Yeah, it's quite flexible. If I'm not mistaken, it also provides rate limiting because rate limiting probably the simplest way to cope with the DOS attack. Also as far as I know, even Amazon API Gateway if I'm not mistaken also provides rate limiting feature. Then that's from Amazon perspective point of view, maybe even with the DOS security groups probably can also be used maybe to play around and protect some of your maybe ports or inputs. What else?

**[00:24:37] Speaker A:** So you mentioned the web application firewall. Yeah, we have another one, the AWS Shield. I don't know if you ever use it.

**[00:24:48] Speaker C:** I had it, but no, I didn't use it.

**[00:24:51] Speaker A:** Okay, okay, now last one from my side. So let's assume that you inherit 10 AWS applications with with poor security posture. Describe your 90 day remediation plan.

**[00:25:11] Speaker C:** Sorry, could you repeat the question or rephrase? I didn't get it.

**[00:25:15] Speaker A:** You have now 10 AWS application with poor security. Okay, so now you need to improve this security and you have 90 days to do it. So.

**[00:25:29] Speaker C:** So I have 10 AW applications. Okay, so maybe what I would in terms of security. First of all I would analyze each application regarding if for what security policies they should be aligned to. Because maybe there are some internal security policies, maybe there are some regulations from countries that don't comply in terms of security. And after that maybe I would create some sort of plan so and split it into a few failures. For instance from for the first month from day one day one to day three I will run through this application and check like some standard stuff what kind of network is used. If there are Amazon in terms of roles, what are roles are used, what kind of people can access to this application. Then I would go what how secrets are managed, how it is in general exposed and deployed where they just use standard EC2 machines or maybe there are already inused services like kubernetes. Then I would go to check on a from API perspective if there are used some services if not how those API handles the request. Again this is what we have discussed in terms of DDoS attack and stuff like that. And then I would move further to check what is applied on if in general there are CI/CD pipelines and if so if there are any what is done in terms of security if there are any drops for looking for vulnerabilities for analyzed code check checking some simple security issues like even SQL injection or also checking if there are hard coded secrets. So that's what's pretty easy because it just runs one by one and checking each of these stuff. And then depending on my research on the second phase, let's say second month I would go and start iteratively fixing all these issues for instance roles. Then if started with roles for every application then check security. If we need to use some sort of secret manager, maybe some of this application already has integration with KMS and maybe it's better to use integration with KMS or stuff like that user are any what kind of encryption is used if there is for instance S3 service used. So just the second phase probably the fixing all the stuff and the last phase, I think it would some sort of monitoring to ensure that all the changes I applied really would really work.

**[00:28:48] Speaker A:** Okay.

**[00:28:49] Speaker C:** Monitoring maybe to see SLO logs if there are any services for tracking errors like Sentry. So it's also good, maybe I can play around and maybe do some tests. Yeah, why not? It depends of course whether it's possible not to affect the end users. But still can be. Can be one of the approaches and yeah, if during that period there are more issues appear or something that I might have missed, that's. Yeah, I got back and fixed it.

**[00:29:30] Speaker A:** Okay. Okay, good. That's all from my side. Thank you.

**[00:29:36] Speaker C:** Yeah.

**[00:29:39] Speaker A:** I don't know. Antonio, if you want to ask something.

**[00:29:45] Speaker B:** Yes. So what is the pro the way of working that you follow when you have to design a new solution?

**[00:30:01] Speaker C:** So first I discussed. I would discuss it with product owner or stakeholders to gather all the requirements. It's very important first to get high level idea to realize the business value and the business impact. Then with the requirements, high level requirements I would go further and maybe decomposite and gather more detailed requirements. So and after that it's maybe similar to C4 methodology. So start from the high level and go down after that with having high level of what should be implemented. I mean what product wants, what they expect. And it's very important when the so called the criticity it's another. Another very important part. And then I will start defining like high level components. Maybe if there are any integration how those components should interact between each other. If there is something based on the existing maybe solution if there is already a platform with all the available components, maybe something that can be implemented within the scope of existing component or maybe it's something that may require creating a totally new implementation. Then of course it's very important to keep in mind some trade offs because usually it's not always available to build something from scratch to use tools I want. Sometimes there are already limits and I have to cope with something that I have on my plate with having high level design. This is maybe what I would only share with engineering team or maybe I would go a little bit further and I would try to create some YAML. Not YAML sorry, UML diagrams. If I'm aware of the code base, if I know how it would communicate so I can think over contracts, I can at least try to draw some UML diagrams and then share with it with engineering team to get some feedback because dev guys can be more aware about some context. Maybe there are some limitations. That's why for Me at least important to get some feedback from engineering team and then I would go also to contact with DevOps team regarding if there are any limits or issues from their perspective and after that if everything would look okay, we can finalize that solution and I can just delegate it to the engineering team to implement. Antonia.

**[00:32:59] Speaker B:** Okay, so. Did you manage for example some external approvals from other teams of the organization? For example from approvals from architecture review board or from the security team, networking and so on?

**[00:33:27] Speaker C:** Probably not in the way you mean because at my recent project I was only the one solution architect but as I previously mentioned, all the ideas, all the solutions I was sharing with engineering team and when they get back with some feedback regarding that some contracts wouldn't work in practice, yeah, I could revisit the implementation and in terms of security I also communicated with DevOps regarding again resources if there are any issues they may point out if not. Yeah, but unfortunately I didn't have experience when I had let's say a high level architect who should validate and approve my solution. But yeah, that would be, that would be a really nice experience but unfortunately I didn't have one.

**[00:34:23] Speaker B:** Okay, so assuming that, assuming that you have a solution, okay. And based on the IT guideline or architecture guideline of the organization, there is some part of this, of this solution that is not properly compliant. Okay. What you do, what do you think to do to be so to. To to address these points. So for example you created, you designed a solution or trying to follow as much as possible the, the guidelines from the architecture team. Okay but at some point you find that there are some inconsistencies with this guideline. What, what you do in that case.

**[00:35:28] Speaker C:** Interesting, interesting question. So how would, how I would act? No, first of all, of course I I wouldn't ignore those guidelines or bypassing silently. So I need to analyze why it happened, why my solution turned to be not compliant. So probably there were some mistakes made, maybe I didn't gather enough requirements or maybe my expectation was wrong and then I need to think over if there is a way within that period of time to fully adapt my solution to that compliance. If let's suppose there is no quick way according maybe if there are some deadlines in the worst case scenario I would think over if there is a way to at least to move further with the critical part and just with the follow up steps incrementally to apply the rest. Yeah, that's probably the plan that I would do.

**[00:36:40] Speaker B:** So you can introduce a risk, let's say because you are not compliant and have a plan to mitigate or reduce or remove this. This risk later. Yes, because probably is not depending on you on what you designed, but you are forced to have this design because some, let's say some constraints of the particular solution are not comp. Are not compliant with the. The guidelines.

**[00:37:17] Speaker C:** Yeah, makes sense. Yeah, you're right. So it's important to analyze what kind of risks we can accept and what kind of risks we can't accept. And we need to be fully aligned with that.

**[00:37:31] Speaker B:** Okay. We call it technical depth or security depth in cases more very more specific and related to the security. So usually we know that the design is not fully compliant with the standards of the organization. But because there is no other way, we open the technical depth that we. We plan to be solved or mitigate

**[00:38:02] Speaker A:** in months

**[00:38:05] Speaker B:** or let's say weeks. Depends on the. On the solution.

**[00:38:14] Speaker C:** Yeah, I see.

**[00:38:17] Speaker B:** Okay. You are used to work with the containerized application, right?

**[00:38:32] Speaker C:** Yeah, yeah. It's getting more and more popular.

**[00:38:35] Speaker B:** Yeah. So typically you have. You deploy some containerized application using Docker, for example, and so on. So Docker image and so on. What are, let's say the. In which way you perform the scanning of these images to be sure that there are no security issues or some issues related to the code or the image of the machine that you are using in your Docker.

**[00:39:25] Speaker C:** There are a few ways. First of all, there are some tools that can be used for scanning images for any security risk. So that's why that this is. That can be used even on CICD pipeline. The second way is that in general,

**[00:39:44] Speaker B:** do you know some tools that you have mentioned?

**[00:39:49] Speaker C:** To be honest, maybe no. I would say no. But here, if I'm not mistaken, in my recent project, I used Amazon ECR service. And if not mistaken, Amazon comes with its own security check. Yeah. And what they wanted to point out that it's also important to use let's say reliable images. So there are some official images that. That let's say well trusted and not. Not worth taking something that were produced by, I don't know, not Malician, but the. The author or provider that you are not aware of. And yeah, and the less, maybe the less dependencies and image has, the better it is. It's true for everything. But again, because if there are many dependencies, it's also another level of risk and you should also be aware it. And maybe even if it's possible to analyze those dependencies.

**[00:41:11] Speaker B:** Okay. And I don't know, during let's say the development you planned, what kind of test

**[00:41:25] Speaker C:** unit Test is simplest. One integration test when you can spin up some dependencies and test the whole flow. Also in my recent project I used Venom, this kind of tool that provides you to write the whole flows, the whole scenarios, let's say the whole signup process which may consist of many calls and many steps. Then when it comes to UI it's more for qa but there are some end to end test. It's also a really nice tool when you can do again to test the whole flow from user's perspective.

**[00:42:06] Speaker B:** Okay. And when you design a solution, what tool you use in terms of let's say to document your solution?

**[00:42:18] Speaker C:** Usually it depends on what kind of tool company prefers. At my recent project I intensively used notion and Miro. So all the details and specifications I was written in notion and in Miro. I was drawing some diagrams and then attach it. Previously I intensively work with Confluence. It's very similar tool where I also was providing the documentation with attaching some diagrams and flows. And it's quite powerful tools.

**[00:42:54] Speaker B:** Also yeah, you use the draw.io

**[00:43:00] Speaker C:** for the diagrams driver but most of my experience I worked with Miro.

**[00:43:06] Speaker B:** Miro. Okay.

**[00:43:08] Speaker C:** Driver also very very similar. But I don't know, maybe historically when I joined the company Miro wasn't used and there were already many diagrams based on Miro and that's why I'm just used to using the Miro.

**[00:43:23] Speaker B:** Okay. Okay. No other question

**[00:43:31] Speaker C:** I have.

**[00:43:32] Speaker B:** Yeah, you have question.

**[00:43:34] Speaker C:** Yeah, I have few questions if you don't mind. At the beginning you mentioned that this role would involve not a lot, but there were many questions about security stuff that there would be some adaptation of existing applications to comply, some security. Maybe you can, if that's possible, you can explain a little bit more about what that role would involve in terms of security and applications.

**[00:44:07] Speaker B:** Okay. So basically. Basically this customer has different application. Okay. Different solutions in

**[00:44:29] Speaker A:** cloud. But

**[00:44:35] Speaker B:** not always all the best the security best practices were followed. So can happen that for example you not configured the WAF or you configure the. Let's say the security group not in the right way allowing more traffic than is requested. Okay. Or other stuff, I don't know. The cryptography is done for example with the self signed certificate, not with the certificates issued by the organization. So different different issues. Let's say so something. Something is to harden. Let's say something else is to completely redesigned depends on the specific solution. We are talking more about legacy solution. Okay. Or some solution that in the past were in on prem were on prem platform and then was migrated lift and shift without let's say such attention in. In the cloud. So this is so just a very high level overview of the work.

**[00:46:17] Speaker C:** And why did it appear you got some signals from let's say audit or just because you were aware that there were some issues and you want just to be aligned with the most security ways.

**[00:46:31] Speaker B:** Yeah, there are let's say periodical assessment on the applications. So we know that some security let's say issues are not found and not covered by the solution. So yes, basically this will comes from an assessment security assessment. So there are already all security depths already creating during the design. So we know at the beginning that the solution has several technical or security depths to solve or something was fined after some scanners, some checks, assessments and so on.

**[00:47:31] Speaker C:** And do you already have like a long term vision, for instance for the following halfway on a year, what part should be already closed in terms of security? Or it just like the way to start iteratively fix security issues and see how it goes. I mean if there are any deadlines regarding when this security issue should be closed.

**[00:47:59] Speaker B:** So basically there is a list of applications to be let's say to be too secure. Okay, the list is say is long. So the time range is end of 2027, the main deadline. Clearly, step by step you are let's say exploring the solution. You provide the design to solve these issues. Other teams internally on the organization will keep this recommendation and develop accordingly to your design the points to be addressed. Okay, so. And then you can go on with another application and so on. Okay, so basically the architect should recommend should redesign some part of the solution to be more secure. But the let's say the development part. So how to put in practice. This recommendation and design should be in charge of another team.

**[00:49:34] Speaker C:** Makes sense.

**[00:49:35] Speaker B:** Different team, I would say depends on the points that you find. So it is networking. So basically the application is not touched, but you have to touch some on the physical physical network. For example you find that the the number of firewall reuse is too much. So you have to to act on the networking side or for example the security group allowing to traffic. So then you have to recommend how to deal with it. And then another team will do the changes.

**[00:50:24] Speaker C:** I see, I see. Okay, thank you. I guess, I guess that that's it from my side.

**[00:50:36] Speaker B:** Okay, thank you for your time then and see you.

**[00:50:43] Speaker C:** Yes, thank you and have a nice day.

**[00:50:45] Speaker A:** Thank you.

**[00:50:47] Speaker B:** You too. Thank you.

**[00:50:48] Speaker A:** Bye bye.
