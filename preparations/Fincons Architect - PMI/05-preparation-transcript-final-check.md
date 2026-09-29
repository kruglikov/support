# Check – Viktar Kruhlikau – Final check before interview – Fincons Solution Architect - R-22866

- Source: https://app.bluedothq.com/preview/6abb97629a7d32f05aea7e7f
- Recorded: 2026-09-29T10:48:02.100Z
- Duration: PT55M12S
- Language: en

## Transcript

**[00:00:11] Serhii Kucheruk:** Okay. No, For you.

**[00:00:29] Viktar Kruhlikau:** Sure.

**[00:00:38] Serhii Kucheruk:** Okay. Recording has started. So hello, my name is Sergey. Today I'll be your interviewer on this fincons project. So to start with, could you please briefly introduce yourself, tell me about your achievements or like something that you think is important about you.

**[00:01:01] Viktar Kruhlikau:** Sure, sure. Hi Sergei, I have about 15 years of commercial software development experience and for the last five plus years I've been heavily involved into architectural work. I worked on projects from various domains such as marketing, commercial real estate, e commerce and financial services and other. I have experience as a. I have a solid background. Sorry, backend experience as a software engineer in various pragmatic languages. I work both with monolith and microservice event driven architectures and have solid experience in CO complex API integrations and DevOps practices. And last two projects I heavily involved into architectural activities. On the project before the last one I combined my architectural role with the tech lead role and last project is I had purely architectural role and regarding but regarding both of these last two projects I think I got even bigger architectural experience while working with tenants integrations. So both of These projects were SaaS platforms with multiple B2B clients, mostly E commerce but not only E commerce clients and I was involved into planning and architecture the integrations and usually I joined the business development team to architect the integration into our platform and within and working with business development team. This allowed me to work with different organizations, various sets of stakeholders. I worked with differently architectured environments and infrastructures and I was delivering architect documentation into different documented systems such as Confluence, sparse sub learnix and had experience defending my solutions to various stakeholders. Last project was very interesting also I worked as I mentioned, I worked as a purely solution architect and designed and led the delivery of high load secure AI content processing platform and I led team for more than 10 engineers as an architect. That's it. In general, regarding my experience, if you would like to know something specific regarding my experience, please feel free to ask.

**[00:04:09] Serhii Kucheruk:** Yeah, I muted. Sorry. So regarding your last project, what is the most like complex architectural decision that you had to make?

**[00:04:21] Viktar Kruhlikau:** Well, I would say that the most complex architectural decision that I made it was to decide how we will divide our monolith architecture monolith application, how we are going to divide it into microservices and what microservices should be separated first and what the second we set with the team leads and started to work on the domains which domains are existing in our monolith application and how can we prepare our application to divide and how to draw boundaries between the contexts and it was quite interesting work. And during this work I faced quite a lot of challenges because not only how to say we constantly we are adding new features and usually when we add new features and do some integrations for new customer and new customer requires this feature and everything should be in a fast pace. And that was quite complicated work to make sure that we are not breaking not breaking the boundaries, not add direct calls between domains and continue moving towards separating separate microservices. And that I would say it was even more organizational challenge than architectural. But we managed to move, not to move and separate some microservices and also all integrations and new features were delivered in time.

**[00:06:34] Serhii Kucheruk:** And how many microservices did you get in the result?

**[00:06:38] Viktar Kruhlikau:** Well, we kept the main some big parts of the monolith application, but divided some microservices. It was about eight or ten microservices in general.

**[00:06:57] Serhii Kucheruk:** Good. Okay, let's probably switch to more like generic questions. So as a solution architect on your project, what are you usually delivering? What are the artifacts you mentioned? Confluence, maybe something else. Diagrams?

**[00:07:18] Viktar Kruhlikau:** Yes.

**[00:07:22] Serhii Kucheruk:** What is this set of artifacts that you deliver?

**[00:07:25] Viktar Kruhlikau:** Well, of course it depends on the project, the size of the project that I'm working on. Regarding the documentation, I also often worked with Confluence in some cases even with Notion, but also in bigger companies. I worked in SAP, Linux and Sparks. And regarding the documentation that I deliver, it's usually architectural overview or introducing some. Well, it really depends on what is required. It can start from architectural vision or architectural definition document and gathering some requirement specifications also can be my responsibility. And high level diagrams usually. Well so usually if we talk if we will take into account tog off approach it lists big list of possible artifacts and deliverables that can be applied. But it depends. It really depends on the situation and usually I strive to deliver only what is required. It's usually start with high level diagrams. In most cases I follow C4 approach, start from the C1 the main landscape and then add in some parts. And if it's required in that case we can work on and add some flow diagrams or sequence diagrams into depending on the requirements. If it's the requirements of technical leaders.

**[00:09:17] Serhii Kucheruk:** Okay, I see. And what about like non functional requirements? So what usually do you collect?

**[00:09:24] Viktar Kruhlikau:** Well, yes of course it we can work together with business analysts or I can gather myself these no non functional requirements. And of course it is being added into the requirements list regarding how data flow should flow from one part of the system into another and what load it should bear and how many requests it should bear the the load and so on. So of course this is also collected information.

**[00:10:09] Serhii Kucheruk:** Okay. Okay. And if you have to like start the project from the scratch like from the totally like new project, do you follow any like standards patterns like oh, you already mentioned togaf, so maybe maybe you heard about something else like. Or do you usually like use togaf? What is your approach to this?

**[00:10:38] Viktar Kruhlikau:** Well, I wouldn't say that I follow some stricter approach like tog off or something like that. Well, but in general it is general set of how to say steps that are being taken. It's of course usually I start with the collecting the requirements and understanding the stakeholders landscape. So at first usually I start from adding some stakeholders list and understanding how and who is responsible for what and where I can get some information. And of course it's, it's everything. This is to understand the business need because before starting to understand the and propose some technical decision we need to understand, really understand the business need what is behind these requirements that we are gathering. And after that I start to communicate with the stakeholders and gather some architecture requirements like functional and non functional requirements. And after that usually I already have some already able to provide some high level architecture guidelines and something like that. And by the way also usually in companies we have some guidelines and approved patterns. So I also usually investigate the documentations of the company of the parties that are included. Into our project. Well, after that I usually design some options and measure some trade offs. Usually it is obvious that we have two or three directions how we can implement the required if it's obvious decision. In that case, of course we can move forward and start designing the solution. But in some cases we have to deal with the design options, understand some criteria, see whether if we are moving into that direction we have these risks, this cost and some some trade offs. If we choose to move into other direction. In. In that case there can be some other risks. After that, after that I can. If we decided and agreed with stakeholders what solution should be, we can finish the documentation document all decision include including technical decision document like C4 diagrams some data flows, what is required and after final review and getting final approval we can hand over to the technical team and oversee the implementation. That is that is the general pass.

**[00:14:18] Serhii Kucheruk:** Okay, I see. Like speaking of your Linux experience, like what fact sheet do you usually deal with?

**[00:14:27] Viktar Kruhlikau:** Fact sheet? Sorry?

**[00:14:29] Serhii Kucheruk:** Yeah, like Linux is based on fact sheets.

**[00:14:33] Viktar Kruhlikau:** Yes.

**[00:14:35] Serhii Kucheruk:** So which one do you usually use or deal with?

**[00:14:39] Viktar Kruhlikau:** I cannot say that I like Linux. I would say that usually I used it for getting Some information that is collected in the system and fact sheet, I don't remember. In some cases, yes, it depended on the company, on the situations. I don't recall the power particle of fact sheets that I used in Linux.

**[00:15:09] Serhii Kucheruk:** Okay, so let's imagine the situation when a business comes to you and says okay, like okay, for example, you are using the tool like for sending emails or something else. Like you're familiar with it and it works well and everything is okay, but business comes to you and says you need to replace it with the. With another one. What is your approach for like communicating these situations?

**[00:15:42] Viktar Kruhlikau:** Well, in general it depends on the. If. If this idea is really credible and good, if it's really credible and good idea, then we can start moving into that direction. But probably we are asking about the situation when the idea is doubtable in general, right?

**[00:16:05] Serhii Kucheruk:** Yeah. So there is like for example, no reason to lose. Like they just won't.

**[00:16:12] Viktar Kruhlikau:** Yeah, they just want. Well, it depends. First thing that I need to understand is who is asking. Because usually in big companies we have big, big amount of stakeholders and each stakeholder has its own responsibility and area, area of control. So if it's not very good idea, I can, I need to understand whether I have to follow these orders as. As we say or I can reject it in some case so I can communicate with other stakeholders. If we find some common ground and understand that okay, it's not required to. To be implemented, then also by the way, I can communicate with the initiator of this change and provide some arguments for them that this change is not really required. I mean it's really important to communicate in words that your party, your stakeholder understands. Even with technical people it's worth to communicate with technical terms and technical language. And with business people it's. It is important to communicate with on their language of terms, costs and delays. Something like that. And if, but if, nevertheless, if I cannot defend my solution and I have to follow it, of course I will follow it in. But I mean that the business usually trumps the technician approach. I mean that we as technicians, we serve the business. So okay, if this solution is wrong and it introduce some technical debt or some other depth, in that case I will for sure highlight these problems and put them into depth list depth tracking systems for future maybe deal with these depths.

**[00:18:35] Serhii Kucheruk:** By the way, how do you usually track technical depths

**[00:18:41] Viktar Kruhlikau:** and in general in any documentation? Usually I usually either create general section that is called technical debt or it's technical debt and that is related to some area. For example, to this particular part of the system to this particular server to this or if it's security debt in that case it will be in security part of the documentation. So in general and it can be even in some in main documents as a part of the some paragraphs related to technical depth. But in general what is important is to make sure this information is noted and collected.

**[00:19:28] Serhii Kucheruk:** Yeah. And like how do you deliver this information to the like people who will like resolve this technical depth? Like so like is it some manager that just. Well you notify that you register a technical debt and then it's their duty or like who is the responsible for that?

**[00:19:50] Viktar Kruhlikau:** Well, it depends. Yeah, always there is always in for any part of this system if it's there is an owner of this system. Usually if we have. If we introduce some technical depth or other types of debt that I notify them separately that okay, here is the problem here we introduce some debt. Okay, let's. Let's plan when we will fix it. Usually if it's really some important debt always should be some plan when we will start to fixing it. So in general I usually notify and we plan some actions and some timeline and some steps mitigation steps when and how we plan to deal with this debt. And of course there can be mitigation plans or migration plans, something like that.

**[00:20:57] Serhii Kucheruk:** Okay. Okay, good. Probably. What. What else should I ask you? Okay, maybe you can tell me like the principles like that that you follow when you design cloud native application

**[00:21:17] Viktar Kruhlikau:** in general. Cloud native most often I worked with AWS and so it's. For me it's easier to provide examples with that. But yeah, the principles are are the same for any other cloud solution. And if we talk about. Were you asking about just planning and architecture cloud solution or some in a secure part of this planning you can

**[00:22:01] Serhii Kucheruk:** cover secure part as well. Why not?

**[00:22:04] Viktar Kruhlikau:** Well okay. So regarding the planning cloud solution of course usually I start with the high level overview of the system that should be implemented and it's like C1 level to understand big parts and landscape of the system where it lives and which big parts communicate with each other. After that we go to the next level with the components and starting to build the components. But if we talk about cloud native applications, what is important? I think there's several layers here and probably on identity and access layer what is important it's to use IAM roles prefer IAM roles for managing the communication between parts of the system on the network network layer. If we talk about, for example endpoints and make sure that we strive to make our Endpoints private and make them public only with restrictions with some restrictions and understand the consequences. And also what is important is to plan proper VPC and subnets boundaries make sure that everything is divided according to the main parts and put private subnets make sure that outgoing traffic goes through NAT gateway and give private make sure that access to internal resources such as S3 or Secrets Manager and so on are through private access. And regarding the incoming traffic, make sure that it is secured and WAF in front of alb and maybe AWS shield is used to prevent DDoS attacks. And what else? Also regarding the secrets and protection layer, also make sure we do not store some secrets in code or something like that and use Secrets Manager instead. And also of course detection, logging, auditing also should be properly set up and. And so on. Okay, maybe. Maybe directly. Maybe I'm moved in the wrong direction.

**[00:25:15] Serhii Kucheruk:** Oh no, no, it's okay. So maybe you can like name few AWS tools that can be used like for incidents review for like adoring or like security monitoring. Like there is a bunch of them. So maybe you worked with some of some of the tools.

**[00:25:39] Viktar Kruhlikau:** Well, what comes to my mind is cloud front of course where also can be set up the alerting and something like that. Cloud trail of course also guardduty for security setups. What else? You mean regarding monitoring, what else?

**[00:26:05] Serhii Kucheruk:** Monitoring and incidence review

**[00:26:09] Viktar Kruhlikau:** Cloudtrail of course, what else? Maybe I missed something but of course there is a lot of tools in AWS for that.

**[00:26:22] Serhii Kucheruk:** Yeah, so let's probably dive into like more details like speaking of the security like in the code, do you like enforce any tools to scan the code or to scan the containers or it's like. Or it's not your responsibility like to do this?

**[00:26:50] Viktar Kruhlikau:** Well, usually I not set them up but of course usually I plan these tools. They are like AWS Inspector and such things to run some static analysis, dependency analysis inside Docker containers, image and secret scanning. So yes, mostly it's like AWS inspector and of course there are some tools that are open source but in AWS we strive to use AWS tools for that.

**[00:27:41] Serhii Kucheruk:** Okay, so let's imagine you have couple of like microservices and you need to like plan the integration between them. So what is your approach for designing the API? Like

**[00:28:00] Viktar Kruhlikau:** are these. Do you mean this microservices are within the same VPC and or with. With the same or kind of really distributed services?

**[00:28:15] Serhii Kucheruk:** Yeah. Okay, let's assume they are like even within the same kubernetes cluster.

**[00:28:22] Viktar Kruhlikau:** Well, we need to understand the relations between these microservices and regarding the connection between them, we we still can use IAM roles for that and we can use EKS POD Identity and cluster Access Manager for managing the ability to communicate between pods within the cluster. What else? And in my opinion what is important here if we talking about the planning and the communication and boundaries and how they communicate it is important just to make sure that we planned the access right properly. Also of course it's secrets and data protection layer also should be planned correctly. And. And the other means like like I mentioned previously, like detection, sorry inspection of Dr. Containers and something like that also should be implemented properly.

**[00:29:49] Serhii Kucheruk:** Oh, okay. So and how do you manage like API version and backward compatibility in your microservices?

**[00:30:00] Viktar Kruhlikau:** Well, let me think. Okay. API versions version. Well, usually we have just. API with not. We do not usually do not use API version in headers. When we implement some API we usually use it version in the actual API URL stuff like that.

**[00:30:35] Serhii Kucheruk:** So you stick to URLs. Okay, why not? Again, what is your criteria criteria between selecting like relational database or NoSQL database?

**[00:30:50] Viktar Kruhlikau:** Well, it's. It depends on the requirements that we have. If we need to really consistent data in that case we should use relational databases. Of course, if we. If relations between between parts of the entities is important and something like that in that case relation that database is the best choice. But if we need to work with the non structured data and we just need to store it and then process it and it's not something that is have strict relation between entities and especially if the structure of the objects may distinct in that case we use some NoSQL database.

**[00:31:52] Serhii Kucheruk:** So you probably worked with Mongo, right? So you know.

**[00:31:56] Viktar Kruhlikau:** Yes.

**[00:31:57] Serhii Kucheruk:** What is like AWS like an analog of Mongo. So what is like a replacement?

**[00:32:08] Viktar Kruhlikau:** We used Elastic for such things like Mongo related but it's not. I think it's not direct replacement. Also in some cases I forgot the replacement for Redis in AWS also Elastic cache or something like that. But the actual replacement probably it's slipped from my mind

**[00:32:42] Serhii Kucheruk:** is documentdb documentdb?

**[00:32:45] Viktar Kruhlikau:** Yes.

**[00:32:47] Serhii Kucheruk:** So and how will you decide if you are going to use documentdb or like self hosted Mongo?

**[00:33:01] Viktar Kruhlikau:** Well usually we strive to use it's kind of. On most of my last projects it was like the rule that we strive to use the native AWS tools. So we would strive to avoid using MongoDB as a self hosted in any case. So I'm not sure that in which cases self hosted mongodb would be better than the AWS Solution?

**[00:33:41] Serhii Kucheruk:** Well, only in terms of costs. Not always. But not always. But you can tweak it. Okay, imagine like a vendor provided you a containerized application, so you have like a container. What are the options to deploy it in aws?

**[00:34:04] Viktar Kruhlikau:** Containerized application? We can use Fargate for easy scaling. Of course we can use our own machine, like EC2 machine and set up it manually. Sorry, deploy it with our own approach, what else? Of course we can rework this application and move it. By the way, when you mentioned containerized application, did you mean Kubernetes containerized application?

**[00:34:50] Serhii Kucheruk:** Well, you have just a Docker container.

**[00:34:53] Viktar Kruhlikau:** Oh yes. Okay, so bare EC2 instance can be used. Fargate can be used, I think. Well, what else? That's two of them that comes to my mind.

**[00:35:13] Serhii Kucheruk:** Okay, like what? What is the difference between like using the EKS like Amazon Kubernetes cluster and setting up Kubernetes manually on EC2 machines. Like what, what are the benefits of each approach and what are the drawbacks?

**[00:35:35] Viktar Kruhlikau:** Well, if we use EKS service, in that case we have fully managed Kubernetes service service provided by AWS and this brings us full benefits from standard services that exist. And inside EKS service it's like EKS Cluster Access Manager, XIS POD Identity. It's also integrated with some security like tools like GuardDuty KS protection and also of course IAM management of identity also can be used very deeply inside eks. And also some other tools are also integrated into this service like CloudWatch and some login things. And monitoring. It's much easier with the AWS services? Well, it's kind of native for that and so it's much more easier to use all this set big set of tools, monitoring and security and identity tools if we use EKs instead of manual Kubernetes deployment.

**[00:37:15] Serhii Kucheruk:** Okay, can you name some tools for monitoring and observability both inside AWS and outside aws?

**[00:37:32] Viktar Kruhlikau:** Inside AWS usually.

**[00:37:33] Serhii Kucheruk:** Oh yeah. I mean what, what AWS provides And if you are not in aws, what other options do you have?

**[00:37:41] Viktar Kruhlikau:** Well, in AWS usually we use Cloud Watch or in some cases we also used El Castech and outside aws. Probably the most common common is El Castech, at least in my experience, for gathering logs information and track this information and present it in some way. And

**[00:38:16] Serhii Kucheruk:** what about distributed tracing? What are the like tools of choice?

**[00:38:24] Viktar Kruhlikau:** Distributed tracing? Well, I'm not sure you name it. Probably I know it, but doesn't come to my mind.

**[00:38:37] Serhii Kucheruk:** AWS X ray, maybe you worked with that or heard about it.

**[00:38:44] Viktar Kruhlikau:** Well, I heard about it, but actually not used.

**[00:38:49] Serhii Kucheruk:** Okay, maybe you have experience with time series databases.

**[00:38:59] Viktar Kruhlikau:** Yes. You mean something like Cassandra?

**[00:39:04] Serhii Kucheruk:** I don't know. Well, I don't know if Cassandra is time series. Like it's something like InfluxDB or TimesCaledB.

**[00:39:14] Viktar Kruhlikau:** Well, not so often. We worked with such databases. I worked with such databases, so probably not so familiar with these technologies.

**[00:39:26] Serhii Kucheruk:** Okay, no problem. So for example, like if you are setting up some okay. Monitoring and sort of ability or something else. What like how do you decide what is an alert and what is just an info information on a dashboard?

**[00:39:49] Viktar Kruhlikau:** Well, if we work in AWS and usually use cloudtrail and set up monitoring and always should be login always should be set up properly. And regarding what is alert and what is. Sorry, what is the second one alert and just regular load.

**[00:40:18] Serhii Kucheruk:** Yeah, just information on the dashboard.

**[00:40:22] Viktar Kruhlikau:** Information on the dashboard? Yes, on the dashboard we should track for sure. We should track important information that reflects the health of our application. So this can be something like CPU utilization or the amount of data or the size of the bucket that is used or something like that. That is important for us to see the health of the applications regarding the alerts. This can be signs that this health is not. Is not in a good state or it's either something happened like error or something like that and this requires immediate actions to fix this problem or these healthy parameters are closing to the values that are sign that the application not in the health health approach in not health situation.

**[00:41:37] Serhii Kucheruk:** Okay, like let's imagine you have like some secrets stored like in. Okay. In Secrets Manager for example AWS Secrets Manager. What is your approach to secrets rotation strategy like how to do it properly in order to not to interrupt services work

**[00:42:04] Viktar Kruhlikau:** and okay, yes Secrets Manager and we need to update these secrets from time to time and if we. But if these secrets are stored in some service in that case this will lead to the situation when some service may store the old value but it's not already a valid value. In that case probably we can use. KMS for storing and for encrypting these secrets. And this would allow automatic rotation of customer managed keys. When new key arrives, all the key material is kept. Probably something like that.

**[00:43:19] Serhii Kucheruk:** Oh, okay, okay, okay. I don't have. Okay, so maybe you can. Maybe you can explain what is DevOps like what does it mean to you?

**[00:43:34] Viktar Kruhlikau:** Well, in general DevOps it's set of practices for me. Set of practices which include. Which are on somewhere in between. We have a development itself and we have cloud and we have operations of Delivering this code into cloud. So like CI CD pipelines and other stuff. So so. And since the main activities of development usually traditionally was concentrated in the code part, in the development part, not in the delivery part, delivered the solution onto into cloud, the DevOps part it's kind of not so often used. Usually team that develops the applications is bigger than and we have only one DevOps in team who is responsible for the delivery of the application into the cloud. So for me it's set of practices. It can be usually this area belongs to one person who is actually DevOps engineer, but in general it's not a law. Also regular developers also may work with this infrastructure infrastructure score approach and things like that.

**[00:45:11] Serhii Kucheruk:** Okay, good. So maybe you can name a few container registries like other than Docker Hub

**[00:45:22] Viktar Kruhlikau:** container registers. Well, AWS container register of course it's in custom solutions we use AWS ECS or sorry, ECR register. What other? I'm not sure that I know other solutions for container registry except AWS ecr.

**[00:45:50] Serhii Kucheruk:** Well, like every like cloud provider has it is Google of course, yes, of course, yes. GitHub Container Registry. So there are a lot of them. Okay, so let's imagine that you have an application and you want to automate the deployment and it's not in kubernetes like what tools are like available to you.

**[00:46:22] Viktar Kruhlikau:** Okay, so how to automate CI CD Pub I pipelines for our cloud application, right? Well, of course. Do you mean some service in AWS

**[00:46:46] Serhii Kucheruk:** for not only not in AWS.

**[00:46:50] Viktar Kruhlikau:** Well, okay, so in that case we can use GitLab or GitHub. Both of these solutions has strong CI CD approaches. Also BitBucket can be used. So and this is if we talk about the actual tools. Usually we used GitLab as a tool for setting up CI CD pipelines and while developing, while planning this CI CD pipelines, it is important to make sure that all tests are being run and static analysis is being run during the CI CD deployment. And if we talk about tools that can be used during the CI CD scans, it can be something like can be named like Snyk or Dependabot or something like that for tracking and scanning dependencies. By the way, in AWS also we have some tools for for dependency scanning, if I'm not mistaken, it's AWS Inspector or something like that which inspects dependencies inside containers. And it's not only inspected during the CI CD pipeline, but it also continually inspects when new CVE new CVE was released and thus it provides continuous security immediately when a New vulnerability was discovered. Well, there are some tools, other tools like Security Hub on. On AWS and also. Should I continue or it's.

**[00:49:06] Serhii Kucheruk:** No, no, no. It's. It's good. It's enough.

**[00:49:08] Viktar Kruhlikau:** Okay.

**[00:49:09] Serhii Kucheruk:** Okay. So maybe you can name couple of zero downtime release strategies that you can use.

**[00:49:19] Viktar Kruhlikau:** Okay. Of course we can use blue green deployment when we switch immediately the environment also I mean switch the traffic from one to new released environment. Or we can use Canary releases. It's when we gradually move traffic to the new environment. New updated version of the application and see if everything is okay. In that case we move the whole traffic to the new environment. New application. New version of the application. Sorry. These are two main approaches. I think. What else? Maybe I missed something.

**[00:50:08] Serhii Kucheruk:** It's okay. It's okay. It's good. No green canary. That's okay. I actually don't have any more questions and we actually running out of time. So probably we can conclude or maybe. Okay, like last question, you mentioned like C4 diagrams that you create. Like do you use like some specific tools to. To create them? Like to draw them?

**[00:50:42] Viktar Kruhlikau:** Only regarding the diagrams. Usually it's either in Confluence or in some specific tool. In Confluence it's like usually some integrated tools like draw IO on some project. We used mirror for drawing diagrams. What else in. In tools like Linux, it's. It has its own diagramming tool.

**[00:51:14] Serhii Kucheruk:** So yeah, it's. It's draw your. Yeah, they have it embedded. Like they forked it and embedded. Okay. Okay. Okay. I don't have any more questions, so we can conclude here.

**[00:51:34] Viktar Kruhlikau:** Okay, thank you very much.

**[00:51:37] Serhii Kucheruk:** Let me just stop the recording. How to stop it? Okay. Protocol of a. Protocol.

**[00:54:20] Viktar Kruhlikau:** Okay. Okay.

**[00:55:03] Serhii Kucheruk:** No key to the lord.
