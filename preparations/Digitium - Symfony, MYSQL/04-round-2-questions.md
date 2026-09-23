# Digiteum round 2 — questions asked

Questions extracted from `/home/viktar/Projects/Support/preparations/Digitium - Symfony, MYSQL/03-round-2-Aliyev-and-Eugene.md` and `/home/viktar/Projects/Support/preparations/Digitium - Symfony, MYSQL/03-round-2-Heniuk-and-Eugene.md`. In both recordings the interviewer is speaker A and the candidate is speaker B. Each entry gives the general idea of the question in full form, then the exact wording from the transcript (auto-transcribed, so the wording keeps the transcription errors) with its timestamp.

## Questions asked in both interviews

The same interviewer asked these topics in both interviews, so they are the most likely to come up again:

- a challenging task that made you feel "almighty";
- why Docker images are layered and why the order of Dockerfile instructions matters;
- multi-stage builds and multi-arch images;
- why two containers on one Docker host cannot reach each other (they are on different Docker networks);
- slow SQL query optimization;
- unit tests and mock objects;
- monitoring and alerting.

## Interview 1 — Aliyev (2026-06-09, data engineering)

1. **Tell me about a challenging task from your experience that, once you finished it, made you feel you could do anything.**
   - "Maybe you had such task a little bit challenging task. When you finished this task, you think, oh, I'm almighty, I can do everything." (0:50)
2. **How do you structure the code of a data-processing project so that it is stable and easy to configure?**
   - "Can you explain how you structure your code for retail processing?" … "Yeah, for better stability, configuration and so." (2:24, 2:35)
3. **How do you prefer to manage Python dependencies: an old-style `requirements.txt` file or a modern tool such as uv or Poetry?**
   - "Your preference what you prefer? I use old style requirements TXT file for your dependencies or use maybe modern UV poetry." (3:49)
4. **Your pipeline has to process a very large CSV file that does not fit in memory. How do you process it, and how do you re-process it when you find that your transformation was wrong and has to be changed?**
   - "In your pipeline you need to process quite big data set. For example, it would be CSV files." … "How you'll work with it and denote it all memory and" (4:39, 4:49)
   - "you need to process this once, but you need to check output of this file after your transformation. Maybe it's your transformation not very good. And you need to process again this file with new transformation." (5:21)
5. **Your pipeline processes terabytes of CSV files. How do you design it so that processing can be suspended and later resumed from the exact point where it stopped?**
   - "And how you will work with pipeline just to have possibility to suspend processing and resume a little bit later." (6:21)
   - "You need to process a lot of files, terabytes of files, CSV files and your process need to have possibility to suspend processing." … "And resume little bit later. And from this point where it was processed." (6:43, 6:57)
6. **You build a reusable, multi-purpose pipeline framework used across several projects. How do you make it configurable: how to process the data, and how to plug in different sources and destinations?**
   - "How you configure your pipelines. For example, you need to implement or not need you implement multifunctional framework. This framework used in a different your project. And you need to configure how to process this data. How to set a different source, different destination hue pipeline." (7:45)
7. **Your pipeline runs in AWS and reads from an S3 bucket that holds very personal data. How do you connect the pipeline to the bucket, and how do you secure access to the bucket as tightly as possible?**
   - "Your pipeline will be run in AWS somewhere. Somewhere and you need to read data from S3 bucket. Okay, your pipeline, how you'll connect this data to your pipeline. First question and how you'll secure this bucket? Because for example, that is very, very personal and we need to secure access to this data as much as possible." (9:35)
8. **What is AWS Glue used for?**
   - "Okay, for what we can use glue in aws." (11:23)
9. **Your pipeline reads from a PostgreSQL database and runs very slowly because its SQL queries load a lot of data. How do you optimize those queries: where do you start, what do you check, and what do you apply?**
   - "your data source is SQL database postgres for example. And when you start your pipeline, you See that it's processed very, very slowly. You try to check and you understand that problem in your SQL queries, they load a lot of data and quite slow. How you optimize these queries from what you start, what you need to check, what you need to apply or." (12:42)
10. **What are an image and a container in Docker, and how do they differ?**
    - "Can you explain what's the image was the container in Docker in context of Docker here." (15:13)
11. **Why do we say a Docker image is layered, and why is that important when you write a Dockerfile?**
    - "When we try to build a Docker image, we write Docker file. Yep. Why we tell that image is a layered. Why it's very important." (16:13)
    - "But we need to talk about exactly how you build image, how you write docker file, why we need think about that image has layers. Why it has layers and why it's important." (16:45)
12. **What rules do you follow to write the most efficient Dockerfile?**
    - "and what rules you should follow to write most efficient docker file." (17:51)
    - "rules you have to follow to write most efficient Docker file?" (18:19)
13. **A typical Python Dockerfile goes: `FROM` a base image, install OS packages, copy `requirements.txt`, install the dependencies, and copy the source code last. Why is it written in exactly that order? (Expected answer: the instructions that change least often go first, so their cached layers are reused, and only the last layer with the source code is rebuilt.)**
    - "When you remember when you write docker image, your first usual command like from Samsung base install some dependencies exactly for your system. Copy requirements Text file or not requirements. Txt Restore your packages copy your sources, right?" … "Why we usually create exactly in such way?" (19:00, 19:27)
    - "Yeah, on goes from top to the low and why we put my comments exactly in this order." (21:15)
14. **Two applications run as containers on the same Docker host, for example your pipeline and a Kafka container, and one cannot reach the other. Why can that happen? (Expected answer: the containers are on different Docker networks; exposing ports is not needed between containers on one network.)**
    - "You run one your application in Docker and second and you need to communicate between these two applications. For example, you implement some kind of API with a fast API. Okay, it doesn't matter. And your one part I need to communicate with other. But they cannot communicate. They one your application cannot reach. Second why it can be happened." (23:20)
    - "You built your pipeline, put everything all your code in docker image. You know what you need Kafka queue for communication for store something and your pipeline cannot reach to this Kafka. It can happen." (26:24)
15. **Do you have experience building multi-architecture Docker images, and can you set up a CI/CD pipeline that builds them?**
    - "Yeah, we have experience to build multi arch docker images." (27:09)
    - "For me? Did you have experience to build multi arch images and do you can configure this pipeline for no CI CD pipeline for build temporary images?" (28:49)
16. **What is your experience with Terraform?**
    - "Terraform. Terraform. Terraform. I remember you had terraform." (29:33)
17. **How do you monitor your pipeline: whether it works, its problems, its performance, CPU usage and memory usage? What tools do you use?**
    - "How you monitor. I'm just checking requirements Monitor your pipeline for performance for memory usage. Super usage what you use for this." (30:46)
    - "What you use to monitor how it works." … "Do it work. Hazard problem, CPU usage, memory and so on." (31:24, 31:31)
18. **What is your attitude to unit tests? Do you write them, and why?**
    - "I forgot to ask you about test union test. Do you like it?" (33:08)
19. **What is a mock object in unit testing?**
    - "What's the mock object in unit testing?" (34:18)
20. **Log files on a regular file system grow by gigabytes a day, new files keep arriving every hour, and the file currently being read keeps being appended to. How do you process them memory-efficiently, and resume from the same position in the same file after the process dies?**
    - "you need to process a lot of logs data logs files generate. Gigabytes of information each days and you need to process these files. You have access to file system where this logs stored and how you process these files and organize just to be more memory efficient and with possibility to again resume and suspend and resume processing." (34:53)
    - "No, no, no, it's okay. Let's be on a regular file system." (35:57)
    - "to process them and they like amount of files increase every hours." (36:07)
    - "When your process die we need to continue processing from the same position from the same file. Understand the that current processing file was updated and we need to read this information later to store necessary information in somewhere else." (36:33)


## Interview 2 — Heniuk (2026-07-01, Python backend)

1. **Tell me about a challenging task from your experience that, once you finished it, made you feel you could do anything.**
   - "From start, maybe you remember from your experience situation and challenging task when you finish it, you think, oh, I am almighty. I can do everything." (0:24)
2. **Why is Python so popular for backend development?**
   - "Why Python? Why Python is so popular for backend development?" (2:32)
3. **How do you structure a large backend project that has several APIs and also scheduled (cron) tasks?**
   - "how you structure a usual structure your project. For example, you have quite big backend project with several ap maybe Chrome task also need to implement here how you structure your code." (3:30)
4. **How do you configure your application, instead of hard-coding connection strings and other settings?**
   - "how you configure your application." (5:12)
   - "Well, sometimes I so called base. When we have had hard coded connection strings and so on." (6:04)
5. **Apart from slow SQL, what are the main performance problems of an API, why do they happen, and how do you avoid them?**
   - "Okay, imagine we have API and from your experience what's the main performance problem here, why it's current and how we can avoid them." (6:17)
   - "Also about SQL queries, you can. We will discuss this later. You can skip this part." (6:49)
6. **You build a RESTful API with FastAPI. Give a strict definition: what is REST, and what makes an API RESTful?**
   - "We need develop restful API with fast API library. Can you explain the first what the REST API restful Let be more strict." (7:57)
7. **What do the URLs in a RESTful API look like: which parts do they have (resources, IDs, version)?**
   - "Okay, how Orel will looks in your API?" (8:44)
   - "It's understand that we need to secure connection. It's a case TCP HTTPs. Not depends on our needs, but exactly parts of URLs how it looks." (8:59)
8. **A user picks a date range and filters, and the API must generate a report, or process an uploaded file into a PDF, which takes several minutes and cannot be sped up. A synchronous request would hit the 30-second default timeout or Cloudflare's one-minute limit. How do you implement this RESTfully? (Expected answer: accept the job, process it in the background through a queue, and let the client check the job's status and fetch the result.)**
   - "Imagine you implement RESTful API, it's quite strict. And we need generate report for user user, select some data on ui, I don't know that range, some filters. And we need to generate report by this data by the spiritual data. Generation of the report can took several minutes. How you can implement this with a restful approach." (9:44)
   - "Yeah, but you forgot that generation can took a lot of time, several minutes." (10:56)
   - "Okay, let it be not report, but imagine processing. We need to upload file, make adjustment on this file and at the end generate PDF file with these images. You cannot speed up this process." (11:34)
   - "and if we use your approach, collect data, send and wait while it will be processed. We have a problem because at least by default timeout can be 30 seconds. If we use several system like, I don't know, Cloud Flower and other. They have stricted them out in one minute. Our request will never finish." (12:39)
9. **How do you secure API endpoints and restrict operations by user role (authentication and authorization)?**
   - "authorization. How we can secure our endpoint, how we can make strict operation split by roles and so on." (13:23)
10. **You use JWTs. What is their main problem? (Expected answer: the backend validates a JWT by its signature without a database lookup, so a stolen or long-lived token cannot be revoked quickly.)**
    - "Okay. We will use JWT token. And what's the problem with this token?" (14:11)
    - "Yeah, but when we use other approach, we also send this information in our request. We can use developer tools and also see what was sent as an in the header or at the top as a parameter. And hacker can use this token to other token. What problem can be on the can mainly with this token." (15:09)
11. **You implement a webhook for a payment provider such as Stripe. It is a public endpoint with no login and no JWT. How do you secure it as much as possible?**
    - "We need to implement webhook and create it quite very strictly and increasing security for this webhook. For example, we try to implement integration with payment system, for example with a stripe, some kind of stripe or PayPal. Not PayPal work in other ways. But we need secure our webhook as much as possible. What you can provide for this." (15:57)
    - "It should be closed webhook usual doesn't work with JBT tokens. They usually use a different approach. It's just very public endpoint. We do not login before accessing to this webhook." (17:05)
    - "Okay, we have the last connection. What else?" (17:49)
12. **How do you verify that the webhook payload (transaction ID, amount, currency) was not modified by a third party? (Expected answer: check a signature of the payload body, such as an HMAC-SHA256 computed with a secret shared with the provider.)**
    - "Okay, how we can check that payload what we receive in this hook is not modified by someone else." (18:05)
    - "I mean exactly payload what was sent for us for data for Processing like what do you create rest of the API. You receive JSON data, what you need process. I don't know, payment information, transaction ID amount, currency and so on. It's stored not in token." (18:29)
13. **You built an API and I am the frontend developer who will use it. How do you give me as much information as possible about the API?**
    - "Yay. When okay, you implement API. I am for 10 developer how you can provide for me as much as possible information about flow API." (19:03)
14. **A public API is already in production and used by partners. The naming convention requires renaming the public field `user_id` to `id`, and the database does not change. How do you make this change without breaking partners?**
    - "Imagine situation. We have a public API. It's already on production. Our partners use this API and we need to make modification here. For example, we have endpoint that users that works with users. And we need to rename property press our model had property user id we need to change just for ID because of our naming convention. How you'll implement these changes." (19:56)
    - "Okay, we don't have problem with database and databases already was incorrect way. We need just update our public models. What goes to to public." (20:44)
15. **In a distributed system, how can the different parts communicate with each other?**
    - "Okay. We have distributed system. Distributed system. We need this how our part can communicate between each other" (21:08)
16. **What is database normalization?**
    - "What is the normalization of database?" (21:51)
17. **When and why do you denormalize tables? Give examples.**
    - "Yeah, when we need to create opposite process. When we need to denormalize some tables." (22:22)
    - "And so why we can need this process" (22:39)
    - "Can you give me some examples where" (22:57)
18. **A query is slow. How do you optimize it: where do you start checking, and what do you implement?**
    - "You see that your query is quite slow. How you'll optimize this from start. What you'll. How you start to check this and what you will implement." (23:43)
19. **Is it good to have many indexes on a table? What does each extra index cost?**
    - "Quite often I hear. Oh, we have a quite slow query. We need to add index and letter. Oh, and we need to add more indexes. Is it better good when we have a lot of indexes?" (24:27)
20. **Have you worked with RabbitMQ?**
    - "Okay, I remember you work with Piscaka. Yeah, yeah. Did you work with RabbitMQ?" (25:34)
21. **What is an exchange in RabbitMQ, and what types of exchange exist?**
    - "Can you explain me what's the exchange here and. And what type of exchange exists?" (25:52)
22. **When do you use a fanout exchange?**
    - "Okay, when we use fan out exchange" (26:19)
23. **Have you worked with WebSockets? A dashboard needs real-time, bidirectional updates, and the backend runs on four horizontally scaled servers. How do you tell each user's browser that something on the UI must be updated? (Expected answer: each server holds its own WebSocket connections and consumes from a RabbitMQ fanout exchange, so a message reaches every server.)**
    - "Okay, imagine situation we need to implement. By the way, did you work with websockets?" (26:31)
    - "We need to implement application with serial time communication with directional. For example, we have dashboard. We need to update this dashboard depends on what user selected. And our backend has four servers. It's like scalloped horizontally. How we can implement this functionality to inform user what it's necessary to update something on ui." (26:41)
24. **In that setup, what kind of queue does each backend server declare, and with which queue parameters (for example durable or not)? (Expected answer: a non-persistent queue, because when a server dies its WebSocket connections die too, so no queued message is needed after restart.)**
    - "Okay. And for this case, what type of queue you'll use for each backend?" (27:37)
    - "No, I'm send RabbitMQ exchange for now, but when we create consumer, we need to specify exchange and queue. And queue can have several additional parameters." (27:50)
25. **Everyone likes Docker. Do you, and why?**
    - "Oh, everyone. Everyone Live Doc." … "Do you like. Do you love? Why?" (28:32, 29:10)
26. **When you write a Dockerfile, why is it important to remember that images are layered?**
    - "When we write a Docker file, we built our image from scratch. Why? It's very important remember that images are" (29:32)
27. **Why are multi-stage Docker builds useful: a build stage installs build dependencies and builds, and only its output is copied into the final base image?**
    - "Okay. I would say multi stage build. Why? It's very useful thing multistage builds in" (30:12)
    - "It's not about Docker Compose and what's what depends on it's exactly built. When you build your image we use multi stage build. Try to remember your last Docker file. I think it looks like from something as a base install app. Get install something not later install other dependencies later from Samsung as a build, you install build dependencies, build something later copy from build copy something to your previous base image and receive your new image. Why we implement such." … "Not so direct way to build images." (30:42, 31:43)
28. **Do you have experience building multi-architecture Docker images?**
    - "Do you have experience to build multi average images?" (32:01)
29. **What types of network exist in Docker?**
    - "Networks in Docker. What type of network exists? What type of network exists?" (32:22)
30. **Two containers on one Docker host need to talk to each other but cannot. Why? (Expected answer: they are on different Docker networks; the only case where resolving a container by its name fails is Docker's default bridge network.)**
    - "You have one host, one server here install Docker. You deploy two containers in this document. And these containers need to communicate between each other, but cannot. Why" (33:13)
31. **Can you set up a CI/CD pipeline from scratch, or have you only modified existing pipelines?**
    - "Okay, I remember you had something with CICD and it was git." (33:56)
    - "configure our pipelines for me mostly. Interesting. You can set up CI CD pipeline from scratch or you just usual make some modifications in existing pipeline." (34:49)
32. **Why do we write unit tests, what do we usually use for testing, what is a mock object, and what do we usually mock?**
    - "Unit test. Unit test. Why we write unit test what we use usually test in our application. What's the mock object? What we what we usually mock." (35:32)
33. **How do you test FastAPI endpoints?**
    - "how you can test your fast API endpoints." (37:37)
34. **How do you do logging and monitoring for an application, and how do you configure useful alerts?**
    - "Okay. Logging monitoring what you use it, what you can configure. We need to monitor our application how you will do it, how you do your best to monitor your application." (38:32)
    - "and how you configure nice alerts." (39:18)
35. **Not how to set up a Kubernetes cluster from scratch, but: do you know how to use `kubectl`, check logs in the cluster, and get a shell into a pod to troubleshoot?**
    - "Oh, forgot about kubernetes cluster. I remember it was written your cv. We don't talk about how to configure a cluster from scratch. How to make configuration for me it's important to understand do you have experience and know how to use kubectl command, how to check logs in cluster, how to enter your board and try to resolve problem." (39:58)
36. **Have you written CLI tools, meaning console applications that accept parameters?**
    - "Task what I want what I forgot I'll just check I'll just check what I forgot to ask you talk about this asking pipeline do you have experience to write CLI tools" (41:29)

