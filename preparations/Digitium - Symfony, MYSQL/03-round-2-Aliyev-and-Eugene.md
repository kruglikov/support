[DE] - Aliyev - DIgiteum- [Round 2] - 2026_06_09 12_44 CEST - Recording - September 22, 2026
https://app.bluedothq.com/preview/6ab2c3eaa196a8cac3858ee3

---

0:00 - Speaker: A
Hello.

0:42 - Speaker: B
Hi guinea, how are we doing?

0:45 - Speaker: A
Hi. Not bad, thank you. And you?

0:48 - Speaker: B
Fine.

0:50 - Speaker: A
Excellent. Today we'll talk a little bit about Python, about OS and everything else. But let's start from your experience. Maybe you had such task a little bit challenging task. When you finished this task, you think, oh, I'm almighty, I can do everything.

1:18 - Speaker: B
Okay, if you're talking about the task that was quite interesting and challenging for me. I would say once I have been working on a task where we had to like change the all sources. Like we had existing pipeline infrastructure but our sources changed so we had to migrate them with let's say all pipelines. So there we had to create this layer additional one between them. It was quite a hard migration. Of course we knew that after that one we would have a technical depth. But that's something that we accepted and after certain time we could migrate everything. It worked, There was a technical debt. But let's say it was something that we could work on in the future. I would say that it was challenging tasks that projects I have worked on.

2:24 - Speaker: A
Okay, thank you. Can you explain how you structure your code for retail processing?

2:32 - Speaker: B
For the retail processing?

2:35 - Speaker: A
Yeah, for better stability, configuration and so.

2:40 - Speaker: B
Okay, if you're talking about the coding part.

2:43 - Speaker: A
Okay,

2:46 - Speaker: B
I would say let's say they have a project in VS code there I have a configurations source where it will be the whole main code workflows where will be a configuration for workflows like tasks inside it. What else? I would say adding the CI CD pipelines, recommits maybe and except for this one what else can be added here? Maybe about the versioning. So every library that we have been using will be a defined version. Like what else I would say about the OP using the classes functions where possible.

3:49 - Speaker: A
Okay. Your preference what you prefer? I use old style requirements TXT file for your dependencies or use maybe modern UV poetry.

4:07 - Speaker: B
I worked on bus, it was a pointy ones and UV too. But from what I can say that I am like a fan of one like poetry or uv. But before I used like poetry it was fine with uv. Like I'm not sure what is a big difference between them but the last one that I have worked on we moved from the point three to the UV something like that.

4:39 - Speaker: A
Okay. In your pipeline you need to process quite big data set. For example, it would be CSV files.

4:47 - Speaker: B
Okay.

4:49 - Speaker: A
How you'll work with it and denote it all memory and

4:57 - Speaker: B
okay, so let's say we have a CC file that's quite big and it can fit to the memory. I'm not sure how to like address these questions through my data engineering experience. Like I have worked on such, but it depends of like, do I need to process only once or how like.

5:21 - Speaker: A
Oh, it will be in general, yeah, you need to process this once, but you need to check output of this file after your transformation. Maybe it's your transformation not very good. And you need to process again this file with new transformation.

5:41 - Speaker: B
So first one. Okay, let's divide it by chunks and processing H by each so it can fit in the memory. What else to say? Generally, I would use maybe Spark. If a file really big. Because spark allows you to work on each file. And if it doesn't fit, it will clear it by the like clear the chunking and continue processing. It will take more time if we don't have enough memory, but at the end it will proceed or maybe do it. Talking about the custom approach.

6:21 - Speaker: A
No, it's quite enough. And how you will work with pipeline just to have possibility to suspend processing and resume a little bit later.

6:37 - Speaker: B
Okay, come again please.

6:43 - Speaker: A
You need to process a lot of files, terabytes of files, CSV files and your process need to have possibility to suspend processing.

6:57 - Speaker: B
Okay.

6:57 - Speaker: A
And resume little bit later. And from this point where it was processed.

7:05 - Speaker: B
Okay, let's use a metadata to store this like information. From the last one, I would say if we're talking about the different technologies, it will be similar to the Kafka. Let's say where we have topics partitioning and offsets. Offsets is exactly similar to this one. Where we have at some points which our consumers already consumed like some id. And if we stop, we will continue from this one in the future. Generally it's good for the processing, parallelization and foul tolerance.

7:45 - Speaker: A
Okay, when you explained how you structure your code, you tell me I have some way configuration source CI CD pipeline How you configure your pipelines. For example, you need to implement or not need you implement multifunctional framework. This framework used in a different your project. And you need to configure how to process this data. How to set a different source, different destination hue pipeline.

8:23 - Speaker: B
Okay, so I need to create a pipeline that reads from some sources and have a target. Okay, so let's say for example airflow about the systems where we can monitor all the changes, make a scheduling. We have to take into account the data quality. It depends on what you use. From my last project, I have been using great expectations with a pyspark. I believe the data quality can be like a different one on the fly and posts after you Process the data. Also I would say about the parameterization of the tasks. Item potendency. That's every task, even if it fails, it will have the same results. It will have the same results every time we run it. What else to add? Maybe something I have missed.

9:35 - Speaker: A
Oh, it's. Your pipeline will be run in AWS somewhere. Somewhere and you need to read data from S3 bucket. Okay, your pipeline, how you'll connect this data to your pipeline. First question and how you'll secure this bucket? Because for example, that is very, very personal and we need to secure access to this data as much as possible.

10:12 - Speaker: B
Okay, if we're talking about AWS S3 backend and let's say we have a pipeline that is the data, but it's like personal one. I believe that we can use masking for the data. Let's say there is a pin data in a detail which cannot be shared with anyone. So we can mask the data and share it with like it's part of it or anything. Also, if you're talking about the AWS system, we have to use VBAAs I am for the like roles group and permission following the like logic with at least needed permission for each role. What else to add? What else to add? Depending on what you use. Like for example, if you use spyspark and Gloom, you can configure it to read all the S3 and it have its own authorization. Well, additionally one let's say for the security.

11:23 - Speaker: A
Okay, for what we can use glue in aws.

11:29 - Speaker: B
For me, AWS glue mostly runs on top of Spark Pyspark. It can be done on Python, but most of the cases that I worked on it was Pyspark. It used for the processing of the data. Like big amount of data. If there is not enough one, then it's better to use less consuming one. Also it's a serverless service used for the etl. Also there is a data cataloging of the data of the tables. Let's say more closely, more precisely. Also it's a no code, low code integration. What else to add? Maybe we can move to the PI Spark. Actually like how it works this this way. Because mainly glue is a detailed process. So it's important to know about the Pyspark and how it works. Like optimization techniques and different. 1.

12:42 - Speaker: A
One second, I recheck the requirement. Do we need Spark or not? I have no idea. Oh, I do not see any requirement. Okay, yeah, no requirement, no problem. Okay, your data source is SQL database postgres for example. And when you start your pipeline, you See that it's processed very, very slowly. You try to check and you understand that problem in your SQL queries, they load a lot of data and quite slow. How you optimize these queries from what you start, what you need to check, what you need to apply or.

13:35 - Speaker: B
Okay, so first of all let's take a look at SQL itself. Maybe we see that there is some part of the code that we don't need at all. Also I would have take a look at the execution plan. There you can see exactly where is bottlenecks. Or maybe there is partitions that we have but it isn't used. Or like we don't have partitioning so we have to use the partition indexing, the predicate push down earlier for the filters. So it will process less the data. More or less. What else I would say about this one? I said about the query optimization, indexing, partitioning. I think that should be more than enough. Maybe about processing aggregated data earlier also depends on how big the SQL you have. Like from where I work with the tail data there was very big SQLs in thousands. So from time to time they have added the code code at the bottom with statement without looking at the main one. So we have to see where you can like optimize it at this point.

15:03 - Speaker: A
Okay. As I remember you have experience with Docker, Docker Compose and everything. Everything connected to Docker.

15:11 - Speaker: B
Yep.

15:13 - Speaker: A
Can you explain what's the image was the container in Docker in context of Docker here.

15:21 - Speaker: B
What is the image and container in the contents of Docker? So generally that's. Let's say it's a block isolated one which can be used for deployment. It can be used for anything. Let's say for the postgres database. And by using the Docker and images we can have and like resolve the issue where it works only on my machine, but everywhere it's one of the main things why we use it with the CI CD pipelines. So if you're talking about the image, it's already predefined. Let's say blueprints which you can just use without setting up everything by yourself.

16:13 - Speaker: A
Okay. When we try to build a Docker image, we write Docker file. Yep. Why we tell that image is a layered. Why it's very important.

16:28 - Speaker: B
Isolated.

16:29 - Speaker: A
Yeah.

16:31 - Speaker: B
Okay. So as I mentioned, if we. If we're talking about isolation, it means that every. Let's say PC laptop have its own like environments.

16:45 - Speaker: A
And when we go you go in wrong way in other way. I talk about exactly about image, about isolation. It's a little bit as a context and concept. But we need to talk about exactly how you build image, how you write docker file, why we need think about that image has layers. Why it has layers and why it's important.

17:17 - Speaker: B
Okay, let me recall. I think it's used for the caching. So we also can use the space for the what else it was for the smart downloading. I think it was used maybe like a common one for the security. I would say

17:51 - Speaker: A
first your thought was correct for caching. It's work for caching for both way when you build image and when you download image and what rules you should follow to write most efficient docker file.

18:14 - Speaker: B
Excuse me, could you come again? Which

18:19 - Speaker: A
rules you have to follow to write most efficient Docker file?

18:30 - Speaker: B
Which rules exactly?

18:33 - Speaker: A
Okay, that remember your last docker file when you built him as I think

18:40 - Speaker: B
you have to like leverage caching. As we mentioned before, use a multi stage buildings and like minimal images that you have. Like if you don't need some like images, don't use it like from time to time. I see there is a docker file.

19:00 - Speaker: A
I'll help you with my question. When you remember when you write docker image, your first usual command like from Samsung base install some dependencies exactly for your system. Copy requirements Text file or not requirements. Txt Restore your packages copy your sources, right?

19:26 - Speaker: B
Yes.

19:27 - Speaker: A
Maybe something download extra for your sources if you need. Why we usually create exactly in such way?

19:37 - Speaker: B
Why we use it in such way?

19:40 - Speaker: A
Yeah, but for example, we put install all dependencies for your operation system for this image.

19:52 - Speaker: B
Okay.

19:52 - Speaker: A
Exactly like this second command after from base.

19:59 - Speaker: B
To be honest, I don't quite follow with a question as well like okay,

20:06 - Speaker: A
okay, I can repeat in other ways in Dockerfile each line like a comment Usual we use run copy and a lot of other things. And when we write docker file quite often it looks like for python code. First line from base image from such image as base Next line we run apt get install and install dependencies for operation system. Next line we copy your requirements to. Txt file next or in one line no copying first. Next we restore our dependencies Next line we copy our sources.

20:57 - Speaker: B
Yes. So why it's designed why we use

21:03 - Speaker: A
all go in such way? Yeah, in this order.

21:07 - Speaker: B
Okay. Do you mean that dockerfile is executes by running from the top to the low? So that's why.

21:15 - Speaker: A
Yeah, on goes from top to the low and why we put my comments exactly in this order.

21:25 - Speaker: B
Okay. So it goes from the bottom button from the top to the Bottom it's catches the results of each step. Let's. So if it's like doesn't change from the last time we have built an image, it skips the steps that's like and reuses existing one. But not sure what else to add.

22:00 - Speaker: A
Yeah, everything connected for caching our build processor and for caching our layers and we put on a top layer that will be changed more rarely.

22:14 - Speaker: B
Yep.

22:16 - Speaker: A
Dependencies. Yeah, very rarely. When we need extra dependencies. Yeah. We need to rebuild all our images

22:26 - Speaker: B
from this point.

22:29 - Speaker: A
It works exactly for this point.

22:31 - Speaker: B
Right.

22:33 - Speaker: A
Because you need to cache and speed up your build process. Speed up your download the image. During deployment we need to put on the top of your file. Exactly. Commands but change it very rarely. You put all basic commands on the top and you copy your code. The last comment. Because your sources change it quite often. And in Happy Pass you just need to rebuild your last layer only copy your sources and your image is ready.

23:13 - Speaker: B
Got you. Interesting. I think I followed this, but I didn't know why. Like why exactly.

23:20 - Speaker: A
It's like it looks in each example what you have in Docker hub and docker documentation. From this you have layer and yeah extra multi stage build. When you have separate build image for build with div dependencies and later just copy output in your previous from previous layer. Okay. Question, Mrs. Stark. You run one your application in Docker and second and you need to communicate between these two applications. For example, you implement some kind of API with a fast API. Okay, it doesn't matter. And your one part I need to communicate with other. But they cannot communicate. They one your application cannot reach. Second why it can be happened.

24:24 - Speaker: B
Maybe port is not open between them so they can't reach each other.

24:30 - Speaker: A
We run in one docker engine on one server. We don't need open ports

24:41 - Speaker: B
to rerun the docker image. We don't need a port.

24:45 - Speaker: A
When you run docker image on one machine.

24:49 - Speaker: B
Okay.

24:50 - Speaker: A
In one docker you don't need exposed port. It's not necessary. You expose port when you try to reach to this container from outside. But when you run a lot of containers inside one docker it's. It's not necessary.

25:13 - Speaker: B
What can be an issue.

25:14 - Speaker: A
Yeah, your application lists on some port. But inside of docker you can reach them if you follow several rules.

25:26 - Speaker: B
Actually I can't say much this like mostly I have been working as a data engineer with the data with the building models deploying from some time to time the docker images that I need. But let me think what it can

25:42 - Speaker: A
be connected Okay, I can give you example. You need. Yes, you built your pipeline, but you need Kafka for processing. And you deploy Kafka as a second container in your on your host.

26:03 - Speaker: B
Kafka. Okay, Kafka which run on the container

26:07 - Speaker: A
in container on this host on the same host where you run your pipeline.

26:14 - Speaker: B
Okay, and my pipeline like I have a pyspark on the same like.

26:24 - Speaker: A
No, for test propose you have a standalone barometle server. You can run everything here. Why not? You built your pipeline, put everything all your code in docker image. You know what you need Kafka queue for communication for store something and your pipeline cannot reach to this Kafka. It can happen.

27:00 - Speaker: B
Okay, maybe they are not on the same like docker network. That's why.

27:09 - Speaker: A
Yes, yes. It's main reason. When you have different different networks, they usually cannot connect each other. If you put exactly in the same network, it's no problem. It's no need to expose ports. No needs. They can reach without any issues. Okay. Yeah, we have experience to build multi arch docker images. I asked about a lot of docker because in their requirement it's necessary to build images.

27:49 - Speaker: B
So like building the docker images is one of the requirements for the like this position.

27:55 - Speaker: A
One of. Yeah. Instead we have such rules because that engineer built on this position. Exactly. Pipeline, configure CI CD pipeline build docker images.

28:15 - Speaker: B
Okay, so if we're talking about the multi architectural docker image generates a single image tag that runs I think multiple like variants but builds for the different. But what else to add.

28:49 - Speaker: A
For me? Did you have experience to build multi arch images and do you can configure this pipeline for no CI CD pipeline for build temporary images?

29:02 - Speaker: B
I think I have used manifest list for this one, but I don't recall that it's like. Was like use multi arc image. Actually from what I recall it's like one big giant file containing the two sets of codes, maybe more. And it's using manifest lists. But what else to add? I'm not sure.

29:33 - Speaker: A
It's necessary to make several changes in your docker file to have correct images for different architecture in general. Okay. Terraform. Terraform. Terraform. I remember you had terraform.

29:52 - Speaker: B
I think I have been using on my last project SDK not a terraform. But now they're similar because I had experience with each of them about with the SDK because it's like a more pythonic way to define the infrastructure.

30:15 - Speaker: A
Okay.

30:17 - Speaker: B
Like as I know the terraform that I have been using can be used with the python Tool. So in any case for the CI CD pipelines we haven't used the Jenkins like Jenkins when we push, we use the Jenkins to trigger and deploy. And then for the CDK we deploy the architecture to store the aws.

30:46 - Speaker: A
Okay, one second. Get interesting. Not interesting. How you monitor. I'm just checking requirements Monitor your pipeline for performance for memory usage. Super usage what you use for this.

31:15 - Speaker: B
Sorry, I didn't hear there was like interruption for some reason.

31:20 - Speaker: A
Okay, monitoring Coherer pipeline.

31:24 - Speaker: B
Yep.

31:24 - Speaker: A
What you use to monitor how it works.

31:30 - Speaker: B
Okay.

31:31 - Speaker: A
Do it work. Hazard problem, CPU usage, memory and so on.

31:38 - Speaker: B
Okay, so if we're talking about the main building of our pipeline generally I have been using the airflow there we can see the like schedule our pipelines, run it and see if there are any failures. If we're talking about the product, we'll have a mail notifications on when the DAC or something that you have is failing. Also we can use a Slack additionally to see that there is some issues with the pipelines that we need to resolve. Also we can have as a like retry policies depending on where to use. If it's like a very big broad pipeline, then maybe it's better to take a look first than retry because it consumes too much of our resources. Also if you're talking about AWS I would say I use the CloudWatch alerts and login where we can see it's like capture of the logs infrastructure one or the any anomalies that we have what else to add? We can use the elasticsearch for the full text of the logs. Let's say at least that it's quite fast one. What else to add? We have trial policies, SLAs notifications I think for the endurance that should be enough.

33:08 - Speaker: A
Yeah, it's enough. I forgot to ask you about test union test. Do you like it?

33:17 - Speaker: B
I think that's not about the liking but I say that I have been using it for our my code and I believe that it's quite important to use at every project that they are working on. At the beginning you spend more time on a unit testing but after that you can much easily like maintain it to make changes without breaking your code. So it's important on the production. Let's say you have been using. You have like can you use it for as a gateway for the coverage let's say of unit tests that it needs to be more than some three holds. We have had like 80%. So for example when you push a new code you have to make end Unit testing for them. So it helps with the maintenance of the code. It's used in a CI CD with the pre commit let's say. So generally that's it.

34:18 - Speaker: A
Yeah. What's the mock object in unit testing?

34:22 - Speaker: B
What is a mock object? Generally it's objects that use like to replace some part of the code. Let's say API that goes to the third party and you don't want to actually go to this API so you replace it with in unit testing. And also generally you isolate your own like parts of the code and you can use it only inside your local environment.

34:53 - Speaker: A
Question about. I asked it about this and you explain it me. But just to one more example how you will process. Okay, you need to process a lot of logs data logs files generate. Gigabytes of information each days and you need to process these files. You have access to file system where this logs stored and how you process these files and organize just to be more memory efficient and with possibility to again resume and suspend and resume processing.

35:52 - Speaker: B
So we have a files that stored as S3 bucket and.

35:57 - Speaker: A
No, no, no, it's okay. Let's be on a regular file system.

36:01 - Speaker: B
Okay, we have a files. It's a regular system that we need

36:07 - Speaker: A
to process them and they like amount of files increase every hours.

36:17 - Speaker: B
Okay, gotcha. So we need like. And what is the problem with it? Like. Okay, depending on what. Sorry.

36:33 - Speaker: A
When your process die we need to continue processing from the same position from the same file. Understand the that current processing file was updated and we need to read this information later to store necessary information in somewhere else.

36:53 - Speaker: B
Okay, so let's say it depends on how often we need this data. Do we need a near real time or it's a batching? If we talk about the batching then I believe that whatever the file system that we use important to use like files that are good for the storage and for the processing like a parque file. Also on top of that we can use the iceberg. If we are talking about the AWS ecosystem which works as a table format on top of the parquet file. At least that's for example so it reduce the compaction push down filters for the Apache like arcades because it's a corner say file format. Also. What else that we converted to the parquet file. We process it whenever the new file comes, we process it through whatever we have. Let's say AWS glue. If we're talking about the real time. I believe it depends of how much streams we have. It's if it's quite like if we don't have much of streams. We can use the Firehouse. It's a lightweight real time solution in AWS so that we can use to process the data as they come. Also we can define the. Let's say which file formats we can store to our system. If we have much more steams then it's better to use Kafka let's say at this point because it has partitioning topics and consumer rooms we can set up and scale. I think that should be enough. Or maybe I can miss something.

38:59 - Speaker: A
No, that's quite enough. And looks like I don't have more questions for you. Maybe you have, but I'm not sure that I can answer about this project. I do not work on this.

39:12 - Speaker: B
You don't work on it?

39:14 - Speaker: A
No, no, no. I work another project. I hope Lucas explained you everything on previous call.

39:23 - Speaker: B
Actually he said that every technical question that you have you can ask them on the next one on a technical interview.

39:29 - Speaker: A
Yeah, exactly. Technical that connected to them just to try to filter a person who can goes to next step. Because more details you can exactly receive only from them. Because they work on this project. They know everything about how they work, what they use. I just have a list of requirements that is necessary to know to candidate.

39:57 - Speaker: B
So do you know about anything about the team? Maybe.

40:02 - Speaker: A
No. No.

40:08 - Speaker: B
I'm not sure what to ask this. Maybe. Maybe do you know more about the clients like as I know the next step.

40:16 - Speaker: A
I don't know. Yeah, it's Oxford Dictionary. Exactly. Your department, your part of project. They need to process dictionaries. They buy dictionaries in different organization for example or publishers. And they need to convert all this dictionary to their own format.

40:39 - Speaker: B
Okay.

40:40 - Speaker: A
They have a configured pipeline. They just change. Change how to load data, how to transform to the format. And a little bit like a dictionary exists not problems. Tricky thing about words, how they should be used truncated ending. It's linguistic things. It's not for me. I'm not very familiar with linguistic and what problems they have. But some problems problems they have. As I know. Yeah. And mostly as. As for me they both dictionary. You need to write pipeline. Fix pipeline to process this dictionary and exposed in their own format.

41:32 - Speaker: B
I think I had experience working on a similar like case. So more or less it's quite understandable. Maybe. Do you know who exactly going to be on the next step? No. No. Okay, maybe the last question. Like when I talked about the last step. It says that it's better to prepare like two slides.

42:04 - Speaker: A
Oh, better right. Ask Lucas about this. Write him.

42:10 - Speaker: B
Okay. Then apart from this one. I don't have questions.

42:16 - Speaker: A
Hey, thank you for your time. It's nice to talk with you.

42:20 - Speaker: B
Thank you to you too. And have a nice day.

42:23 - Speaker: A
Thank you. You too. Bye.

42:25 - Speaker: B
Bye. Bye. 