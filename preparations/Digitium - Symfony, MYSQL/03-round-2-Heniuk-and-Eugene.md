[DE] - DIgiteum - Heniuk - [round 2] - 2026_07_01 11_48 CEST - Recording - September 22, 2026
https://app.bluedothq.com/preview/6ab2c67fe5e7c4b81a662fcc

---

0:00 - Speaker: A
Hello. Hello. How are you?

0:21 - Speaker: B
Yeah, I'm good. What about you?

0:24 - Speaker: A
I think also good. Today I'll talk a little bit about Python about different general things about API and so on. From start, maybe you remember from your experience situation and challenging task when you finish it, you think, oh, I am almighty. I can do everything.

0:50 - Speaker: B
So I can tell you a bit about my latest project here. I faced some difficult tasks when I was required to analyze such complex JSON XML schemas and to understand how to make pydantic validation, how to make Pandas cleaning. And this was quite complex data structures. Here I was needed to analyze. I was needed to structure somehow and translate it into Pandas and Python cleansing Python code. Yeah, there was quite complex news articles, some shares information coming from external sources into our API and it was quite challenging for me just to collect all of the data sources, collect all of the data and to analyze them. I think this initiative was the most challenging for me. It took a long time, nearly three months or four even just to collect everything in my mind, collect everything in documentation and to translate it in some technical solution that was needed to clean it, ingest it and store it in our storage in GCS. Yeah. Oh, sorry. This was S3 in AWS.

2:32 - Speaker: A
Okay, thank you. Why Python? Why Python is so popular for backend development?

2:39 - Speaker: B
So Python is quite popular because of low barrier intro in Python and it has quite rich ecosystem here. It it's used for developing REST APIs with use of different frameworks. That's quite miniature I would say that's quite old. Have good documentation, have good community and it's widely used right now. And it's some kind of standards to develop simple and to deliver some simple APIs that are not. That are not faced with high load.

3:30 - Speaker: A
Okay, how you structure a usual structure your project. For example, you have quite big backend project with several ap maybe Chrome task also need to implement here how you structure your code.

3:52 - Speaker: B
There's not a definite solution single one solution. I mean we can structure it differently. For example, Django has applications some apps inside of your monorepo to create a new domain. You just creating apps inside of Django repository in case we are developing with Flask or first API you need to structure your project as you can structure differently domain driven development. It could be some onion where you define when you define controllers, services, models and so on. It could be monorepo. It could be a few repos. For example, in order to make Chrome tasks you can create another folder or you can create a new repo. It depends it really depends on the project, on project evolution, on project how, how engineers used to develop

5:12 - Speaker: A
how you configure your application.

5:17 - Speaker: B
Also you can apply a different approach in terms of host APIs identity settings library could be used to read some environment files and to standardize some settings. It could be key vault in aws. Right. So different ways to configure your backends. In Django there's a different approach. You can configure setting Py file. You can create new files and imports e.g. broad dev environments. So it's. It's really so wide question. You can configure it differently?

6:04 - Speaker: A
Well, sometimes I so called base. When we have had hard coded connection strings and so on.

6:12 - Speaker: B
It's no, we need to avoid this.

6:17 - Speaker: A
Okay, imagine we have API and from your experience what's the main performance problem here, why it's current and how we can avoid them.

6:33 - Speaker: B
So in my experience we faced the main performance problems with database itself. So the queries was slow and we required to analyze and to profile database query itself.

6:49 - Speaker: A
Also about SQL queries, you can. We will discuss this later. You can skip this part.

6:57 - Speaker: B
Yeah, Okay. I want to proceed with some asynchronous problems. That's what could be written such a way that I think libraries become not asynchronous. They are not concurrent. They are just sequentially executes the code and it may cause some problems. You can use blocking libraries that also can slow down your backend. That's the main problems I would say. We have also Pyspy tool to analyze backend to analyze the python codes. You just run this library and you can see the profile of your codes. You can see timings and memory consumed by different libraries, processes and so on.

7:57 - Speaker: A
Okay, imagine station. We need develop restful API with fast API library. Can you explain the first what the REST API restful Let be more strict.

8:17 - Speaker: B
Yeah, okay, I understand it stands for representational state transfer. It has six main principles under the hood. It implements the JSON communication between services or it can implement the API with use of JSON data structures that should be defined in your project.

8:44 - Speaker: A
Okay, how Orel will looks in your API?

8:54 - Speaker: B
You mean this just default HTTPs.

8:59 - Speaker: A
It's understand that we need to secure connection. It's a case TCP HTTPs. Not depends on our needs, but exactly parts of URLs how it looks.

9:12 - Speaker: B
If we implement some different domains. We want to separate some domains. First of all I want to make it slash users, slash products, slash news, whatever. And then we need to implement some endpoints with different Methods, post, deletes, puts, get and then slash. Version for example could be used to define the version before the domain. Actually, yeah.

9:44 - Speaker: A
Imagine you implement RESTful API, it's quite strict. And we need generate report for user user, select some data on ui, I don't know that range, some filters. And we need to generate report by this data by the spiritual data. Generation of the report can took several minutes. How you can implement this with a restful approach.

10:18 - Speaker: B
So the default approach is to create some front end server that's that has some button that had some form to insert it. And then front end server sends request to our backend server and it handles it so we can understand it, parse some arguments and make a query into our database. And SQL query gets some data from database and the conservative returns it to front end, right?

10:56 - Speaker: A
Yeah, but you forgot that generation can took a lot of time, several minutes.

11:01 - Speaker: B
Yes, of course in this case we can use different databases. We can use some NoSQL databases, columnar, it could be document oriented. MongoDB for example, we can cache something. So it could be. There are a lot of approaches to speed up your queries, right? You can apply. You can apply indexes in database. That's the most simple approach. You can.

11:34 - Speaker: A
There's no problem. Exactly. With sped up. You cannot speed up this process. Okay, let it be not report, but imagine processing. We need to upload file, make adjustment on this file and at the end generate PDF file with these images. You cannot speed up this process.

12:01 - Speaker: B
In this case we can vertical scale our backend in order to process some images more quickly, right?

12:13 - Speaker: A
No, we cannot. Okay, it's still slow because we cannot. Exactly. We really cannot speed up to accept receive response quite fast in the seconds it will took several minutes, 100%.

12:36 - Speaker: B
So. Okay,

12:39 - Speaker: A
and if we use your approach, collect data, send and wait while it will be processed. We have a problem because at least by default timeout can be 30 seconds. If we use several system like, I don't know, Cloud Flower and other. They have stricted them out in one minute. Our request will never finish.

13:08 - Speaker: B
Yeah, okay, I understand this case. You can implement some queues in order

13:12 - Speaker: A
to

13:14 - Speaker: B
receive the request and process it in the background. Yeah,

13:23 - Speaker: A
authorization. How we can secure our endpoint, how we can make strict operation split by roles and so on.

13:38 - Speaker: B
We implement this with use of frameworks, right? I mean role based access control for the APIs and authentication methods could be different. JSON Web Token, it could be just password session authentication, fingerprints. You can implement QR codes, two factor authentication. There are lots of Approaches also you can log in with Google. That's oauth authentication, right.

14:11 - Speaker: A
Okay. We will use JWT token. And what's the problem with this token?

14:20 - Speaker: B
Usually problem is everyone can see what it's how it looks like.

14:28 - Speaker: A
Yeah.

14:29 - Speaker: B
You can get JSON web token and you can see in JWT IO site you can read the payload. The problem could be that hacker can can get this code with developer tool and he can forge the request and you and he will access the API. The server will think that it's user who logged in who is in beloved.

15:09 - Speaker: A
Yeah, but when we use other approach, we also send this information in our request. We can use developer tools and also see what was sent as an in the header or at the top as a parameter. And hacker can use this token to other token. What problem can be on the can mainly with this token.

15:41 - Speaker: B
So I'm not sure you you're really talking about, but it could be a time of refresh of this token. You. You should implement the refresh token in order to regenerate an access token.

15:57 - Speaker: A
Okay. Usually this token has a short lifetime. And on backend we just validate is a token valid check signature and check other information without accessing the database. And if tokens exactly steal it or was created for a long period. We cannot revoke these tokens very fast. We need to implement a lot of other things. Okay. We need to implement webhook and create it quite very strictly and increasing security for this webhook. For example, we try to implement integration with payment system, for example with a stripe, some kind of stripe or PayPal. Not PayPal work in other ways. But we need secure our webhook as much as possible. What you can provide for this.

17:01 - Speaker: B
So it should read JSON web token signature first of all.

17:05 - Speaker: A
Right. It should be closed webhook usual doesn't work with JBT tokens. They usually use a different approach. It's just very public endpoint. We do not login before accessing to this webhook.

17:27 - Speaker: B
Yep. So in order to secure the endpoint as strictly as possible, you must implement defense in depth framework. It means TLS 1.3 encryption with SHA256 signature.

17:49 - Speaker: A
Okay, we have the last connection. What else?

17:56 - Speaker: B
It should be some expiration time, for example, five or even less minutes. All right.

18:05 - Speaker: A
Okay, how we can check that payload what we receive in this hook is not modified by someone else.

18:20 - Speaker: B
We can see it in JSON web token and if signature is not correct, we will see it.

18:29 - Speaker: A
I mean exactly payload what was sent for us for data for Processing like what do you create rest of the API. You receive JSON data, what you need process. I don't know, payment information, transaction ID amount, currency and so on. It's stored not in token.

18:52 - Speaker: B
Yeah, we will have some signature that's generated that could be generated by different methods. For example SHA256.

19:03 - Speaker: A
Yay. When okay, you implement API. I am for 10 developer how you can provide for me as much as possible information about flow API.

19:22 - Speaker: B
You mean the documentation we can implement Swagger ui. It's available in Django, it's available in fast API. So we can configure some Pybantic models in first API that will define how a first API receive and how it handles the request. And first API will generate this wagon documentation. Exactly how you define your identity schemas.

19:56 - Speaker: A
Imagine situation. We have a public API. It's already on production. Our partners use this API and we need to make modification here. For example, we have endpoint that users that works with users. And we need to rename property press our model had property user id we need to change just for ID because of our naming convention. How you'll implement these changes.

20:28 - Speaker: B
So you will need to rename it everywhere. First of all, it will be some models rename. Right. And you will need to recreate the migration file in order to.

20:44 - Speaker: A
Okay, we don't have problem with database and databases already was incorrect way. We need just update our public models. What goes to to public.

20:57 - Speaker: B
Okay, I understood. There's a simple solution to make API versions. You can slash v2 for the second version, for example.

21:08 - Speaker: A
Yeah. Okay. We have distributed system. Distributed system. We need this how our part can communicate between each other

21:24 - Speaker: B
with some gateway with use of broker. Right? You mean parts of our micro of our backend microservices.

21:36 - Speaker: A
So yeah, Microservices is one name, but in general it's called distributor system.

21:42 - Speaker: B
Okay.

21:43 - Speaker: A
Different parts somewhere

21:47 - Speaker: B
also

21:51 - Speaker: A
some kind of a guide or kills. Okay. Databases. You explain what you can have a problem with database? Well, yeah, for start maybe some kind of general question. What is the normalization of database?

22:11 - Speaker: B
Normalization is the process when you define some new tables in order to reduce duplicates or reduce some anomalies in data. The schema.

22:22 - Speaker: A
Yeah, when we need to create opposite process. When we need to denormalize some tables.

22:30 - Speaker: B
Yep. We will create. Not create, but expand some old tables to make them wider.

22:39 - Speaker: A
And so why we can need this process

22:46 - Speaker: B
in order to speed up our queries to reduce latencies for joins.

22:57 - Speaker: A
Can you give me some examples where

23:00 - Speaker: B
it can be used for Example, if we have some NC relational diagram with products, categories, users, right? For analytical purposes you can create some white table or calculated table, whatever it could be some layered approach, bronze, silver, gold layer and you will create some white table. And here you will contain all of the columns from previous tables from entity relation diagrams in order to reduce joints overhead. Okay,

23:43 - Speaker: A
You see that your query is quite slow. How you'll optimize this from start. What you'll. How you start to check this and what you will implement.

23:54 - Speaker: B
First of all, we need to profile it with some database built in tools. Explain, expand, analyze. In postgres, for example, you will see an exam an exact execution plan and you can rewrite your code. You can implement some indices and some helper tables to quickly join another table. Since bridge tables also known as. Yeah, so different approaches here.

24:27 - Speaker: A
Quite often I hear. Oh, we have a quite slow query. We need to add index and letter. Oh, and we need to add more indexes. Is it better good when we have a lot of indexes?

24:41 - Speaker: B
So it depends on your business inputs. It depends on your queries. You will need to speed up the queries itself. For example, if you see that query not filters by date, you will not need to implement the index by date, right? You need first you need to see to analyze your queries and then only after that you will need to implement indexes because they can even slow down your queries. Just because it needs some time to create a new data structure. I mean indexes. And also I can mention the different types of indexes in Postgres. It's B3, the default one hand hash indexes, gist, SP, gist and so on.

25:34 - Speaker: A
Okay, I remember you work with Piscaka. Yeah, yeah. Did you work with RabbitMQ?

25:44 - Speaker: B
Yeah, I had experienced. I have had experience in some secondary project with RabbitMQ.

25:52 - Speaker: A
Can you explain me what's the exchange here and. And what type of exchange exists?

26:00 - Speaker: B
So the exchange is like a pipe where you store your messages and then ribbitmq decides how to exchange these messages. It could be by some rules. It could be randomly or just a fan out for your consumers.

26:19 - Speaker: A
Okay, when we use fan out exchange

26:25 - Speaker: B
usual in order to send notification for all of our consumers.

26:31 - Speaker: A
Okay, imagine situation we need to implement. By the way, did you work with websockets?

26:38 - Speaker: B
Yeah, yeah, fine.

26:41 - Speaker: A
We need to implement application with serial time communication with directional. For example, we have dashboard. We need to update this dashboard depends on what user selected. And our backend has four servers. It's like scalloped horizontally. How we can implement this functionality to inform user what it's necessary to update something on ui.

27:19 - Speaker: B
So these nodes will have some websocket endpoints, right? And you will need to implement RabbitMQ exchange to find out to broadcast this message to all of the nodes and the nodes will receive requests.

27:37 - Speaker: A
Okay. And for this case, what type of queue you'll use for each backend?

27:47 - Speaker: B
I would rather RabbitMQ.

27:50 - Speaker: A
No, I'm send RabbitMQ exchange for now, but when we create consumer, we need to specify exchange and queue. And queue can have several additional parameters.

28:08 - Speaker: B
You mean your messages should be persist

28:12 - Speaker: A
to this or not persist in this

28:15 - Speaker: B
case RabbitMQ by default, as I remember not persisting it messages we need to. I'm not sure, but we can configure it, I suppose. Or we can implement our own mechanisms from right ahead log.

28:32 - Speaker: A
Oh, for example, for me, for this case, we don't need a persistent queue because on application died, one backend server died and when it's restored we don't need privacy queue because all our connection were used before. We don't have such connection. We don't need to inform any users that were connected before on this server. Okay, what I want to ask. Oh, everyone. Everyone Live Doc.

29:09 - Speaker: B
Yes.

29:10 - Speaker: A
Do you like. Do you love? Why?

29:13 - Speaker: B
Yeah, just because you can implement some docker Docker Compose files and you can wrap up your whole application that could be easily managed in different environments. It could be started with just a single comment Docker compose app.

29:32 - Speaker: A
Okay. When we write a Docker file, we built our image from scratch. Why? It's very important remember that images are

29:45 - Speaker: B
layered because Docker caches all of the layers. And if you implement something new Docker cached, it's already on the application side. And if you make some changes with git push for example, the docker on application site receives these updates and it's not resembles all image from scratch. It just updates new layers.

30:12 - Speaker: A
Okay. I would say multi stage build. Why? It's very useful thing multistage builds in

30:23 - Speaker: B
CI CD Pro progress.

30:24 - Speaker: A
You mean in context of Docker we still was talking about.

30:31 - Speaker: B
Okay, some of services. Some containers could depend on others and then you will implement depends on keywords.

30:42 - Speaker: A
No, no, no, no, no, no, no, no, no, no. Not this. It's not about Docker Compose and what's what depends on it's exactly built. When you build your image we use multi stage build. Try to remember your last Docker file. I think it looks like from something as a base install app. Get install something not later install other dependencies later from Samsung as a build, you install build dependencies, build something later copy from build copy something to your previous base image and receive your new image. Why we implement such.

31:43 - Speaker: B
Yeah, I understand.

31:43 - Speaker: A
Not so direct way to build images.

31:46 - Speaker: B
Yeah, yeah, I understood. From keyboard is used you can split the environments while building the Docker image.

32:01 - Speaker: A
All right here. Dr. Okay. Do you have experience to build multi average images?

32:11 - Speaker: B
Multi arch. Not sure,

32:18 - Speaker: A
not sure. Maybe yes, maybe no.

32:21 - Speaker: B
Yeah, no, no. Not really.

32:22 - Speaker: A
Really, I mean. Okay. Networks in Docker. What type of network exists? What type of network exists?

32:34 - Speaker: B
There are several types that's could be configured for different purposes. The network is a way to communicate between the containers. Right. As I know, we can configure some network that forwards our ports outside of Docker and we can create a bridge network that will connect containers inside of Docker environments.

33:13 - Speaker: A
You have one host, one server here install Docker. You deploy two containers in this document. And these containers need to communicate between each other, but cannot. Why

33:30 - Speaker: B
in one single host, right?

33:32 - Speaker: A
Yes, one single host, one Docker host.

33:40 - Speaker: B
They cannot communicate improperly configured networks. It could be the case. It could be the case that domain name resolution is not correct inside of your environments.

33:56 - Speaker: A
My name resolution only in one case. I know when you create in default network. Because here the NAS is doesn't work here. No problem. When we create our containers on different networks, by default they cannot communicate. Okay, I remember you had something with CICD and it was git. Oh, hold on.

34:39 - Speaker: B
I can tell you about different tools. I used GitHub workflows. I used Jenkins with groovy language to

34:49 - Speaker: A
configure our pipelines for me mostly. Interesting. You can set up CI CD pipeline from scratch or you just usual make some modifications in existing pipeline.

35:04 - Speaker: B
Yeah, I had a chance to configure it from scratch.

35:07 - Speaker: A
Thank you. Because usually it doesn't matter what system you use. GitHub Action GitLab Jenkins. If you understand what this tool can do what you used before, you always can find solution. Another thing.

35:25 - Speaker: B
Yeah.

35:25 - Speaker: A
Not always, but maybe 90%.

35:29 - Speaker: B
Yeah, yeah, I agree.

35:32 - Speaker: A
Unit test. Unit test. Why we write unit test what we use usually test in our application. What's the mock object? What we what we usually mock.

35:45 - Speaker: B
Okay. I like pytest to be honest. Because it's simplicity. Because it's wide range of libraries. You can coverage. You can configure some parameterized functions in order to imitate endpoints to imitate some tests. So it's short, it's concise, it has good documentation, it has a lot of add ons libraries And I prefer pytest to be honest. So in my practice I used test driven developments and first before the deployments I run all the tests. I configured CI CD print progress with tests before the deployment and only then our code could be could be deployed and updated in production. So you asked about mocks. Also I can mention patch function. That's Mock function is a function that imitates Imitates the behavior of some function. Yeah, you can configure mock object and you configure some return results from it. And in order to test some endpoints you can just configure few mock objects and not execute some endpoints or execute real code. You just can imitate it. Patch also can be used when we can't mock objects because because of code structure. So we can use patch

37:37 - Speaker: A
how you can test your fast API endpoints.

37:41 - Speaker: B
So my preferred approach is use pytest and to configure the endpoints. The process looks looked like the

37:56 - Speaker: A
the

37:56 - Speaker: B
starting of testing database initialization of our models, then filling it with some testing data and then running all of the tests that was configured in pytest. It was parameterized parameterized decorator on top of tests. Also you can configure some fixtures that that's convenient to fill database or run your migrations into database. Yeah.

38:32 - Speaker: A
Okay. Logging monitoring what you use it, what you can configure. We need to monitor our application how you will do it, how you do your best to monitor your application.

38:50 - Speaker: B
So first of all I will tell you about my latest project and most recent experience in AWS. We saved all of our logs in S3 files and we can read it files inside of S3 buckets.

39:05 - Speaker: A
Yeah.

39:07 - Speaker: B
In order to analyze it. In order to monitor our containers we used CloudWatch

39:18 - Speaker: A
and how you configure nice alerts.

39:28 - Speaker: B
Yeah, we need to configure alerts if something urgent. If something really bad happens. We don't need to send notifications for each of small problem for all of the info debug logs. Right. And in in my latest project we configured sns that sent messages in Slack and Gmail.

39:58 - Speaker: A
Oh, forgot about kubernetes cluster. I remember it was written your cv. We don't talk about how to configure a cluster from scratch. How to make configuration for me it's important to understand do you have experience and know how to use kubectl command, how to check logs in cluster, how to enter your board and try to resolve problem.

40:28 - Speaker: B
So I configured it in my bright project. I wanted to learn about it and I am familiar with these containers spots nodes cluster the database inside of cluster Kubectl also was used right to implement this pet project in my experience I have used Kubernetes previously as a user. I just entered the containers with Lens id. You can join your you can connect to your Docker Kubernetes cluster with this ID lens and I used it as user, not as DevOps engineer. I didn't implement some new features, some containers and so on.

41:29 - Speaker: A
Task what I want what I forgot I'll just check I'll just check what I forgot to ask you talk about this asking pipeline do you have experience to write CLI tools

41:50 - Speaker: B
like CLI tools So not really it was just separation of our environments. I created some scripts that's implemented that

42:08 - Speaker: A
read

42:10 - Speaker: B
parameters from console and depends on your parameters different files or different environments executed. So that's my experience.

42:24 - Speaker: A
Yes, this is any console application that accepts different parameters. It's some kind of so there is not a problem. Yes, and I think maybe I do not have more questions for you. Maybe you have but to be honest, I cannot explain a lot about this project. I do not work on this.

42:47 - Speaker: B
Can you. Can you tell me how the further interviewing process will look like?

42:54 - Speaker: A
I send my review to Lucas and later everything be after Lucas what he explained that maybe next step and communication is exactly this team. What team? Someone from this team from exactly this team where it's necessary to work and they can explain a lot of interesting question about project but I do not know exactly who will present on next step because as I remember it was Scrum Master or it might be it's for assets. I'm not sure.

43:36 - Speaker: B
Okay, I understand. So when to expect the feedback from this interview?

43:42 - Speaker: A
Today is Wednesday. Maybe tomorrow before noon, I hope. Yeah.

43:50 - Speaker: B
Okay, sounds great. So if you don't know much about this position, I can't ask.

43:57 - Speaker: A
I can explain that this company has a lot of teams they implement different think it's we have data engineers here on this project detail processing team Everyone work with Python they have once in process different vocabularies converted in correct format is our ET Altium and they have also API and some front end to provide this data to their partners and I think your position is exactly team who make API and some kind of website but it's quite quite easy website a little bit JavaScript main language Python they use AWS for their infrastructure. A lot of tests. A lot of tests. Yeah, I remember it was a lot of tests.

44:59 - Speaker: B
So okay. I have a rich experience in data engineering. Would you require this or not?

45:05 - Speaker: A
Or maybe. Yes, but not a lot because mainly they looking for writing API but maybe before communication with that engineer team.

45:21 - Speaker: B
Okay, I understand this is full stack front end plus backend position, right? Mainly backends.

45:30 - Speaker: A
As I understand, mainly back and from front end. It was maybe makes small fix in JavaScript or TypeScript because they have someone who. Exactly. Front end developer. Yeah.

45:46 - Speaker: B
Okay. To be honest, sounds good for me.

45:51 - Speaker: A
Thank you for your time.

45:53 - Speaker: B
Yeah, thank you.

45:55 - Speaker: A
See you.

45:55 - Speaker: B
See you.

45:56 - Speaker: A
Bye. 