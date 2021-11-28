# Project 1 Final Submission

The aim of this project is to build a microservice-based application that would allow users to run Apache Hadoop, Spark, Jupyter Notebooks, SonarQube and SonarScanner without having to install any of them. 

In order to implement and deploy this application on Google Cloud Platform, we will have to first push all the necessary images to GCP Container registry. Then, create a kubernetes cluster using Google Kubernetes Engine and deploy these images on it as containers running inside pods. Once done, we will have to expose these pods using services and bind our application.


To build Containers we would first need their respective images.


List of images used for this project:

1. Hadoop Worker - https://hub.docker.com/r/bde2020/hadoop-datanode
2. Hadoop Master - https://hub.docker.com/r/bde2020/hadoop-namenode
3. Jupyter Notebook - https://hub.docker.com/r/jupyter/minimal-notebook
4. Spark - https://hub.docker.com/r/bitnami/spark
5. Sonar - https://hub.docker.com/r/shalinishukla123/sonarscanner
6. Application UI - https://hub.docker.com/r/shalinishukla123/bigdatapythonapp


The Application is built on top of nginx image.
The Dockerfile for the application looks like this - 

```
FROM nginx
COPY index.html /usr/share/nginx/html
```

Here, index.html is the UI for the application that contains the necessary buttons that allow redirection to microservices.

Push the Application UI to your docker hub account using the following command -

```
docker build -t shalinishukla123/bigdatapythonapp:latest .
docker push shalinishukla123/bigdatapythonapp:latest
```


## Steps to push all images to GCP Container Registry -

Commands for pushing application UI:

```
docker pull shalinishukla123/bigdatapythonapp
docker tag shalinishukla123/bigdatapythonapp gcr.io/sincere-idea-136323/shalinishukla123/bigdatapythonapp
docker push gcr.io/sincere-idea-136323/shalinishukla123/bigdatapythonapp
```

Commands for pushing Jupyter notebook image:

```
docker pull jupyter/minimal-notebook
docker tag jupyter/minimal-notebook gcr.io/sincere-idea-136323/shalinishukla123/minimal-notebook
docker push gcr.io/sincere-idea-136323/shalinishukla123/minimal-notebook
```

Commands for pushing Sonar Scanner image:

```
docker pull shalinishukla123/sonarscanner
docker tag shalinishukla123/sonarscanner gcr.io/sincere-idea-136323/shalinishukla123/sonarscanner
docker push gcr.io/sincere-idea-136323/shalinishukla123/sonarscanner
```

Commands for pushing Spark image:

```
docker pull bitnami/spark
docker tag bitnami/spark gcr.io/sincere-idea-136323/shalinishukla123/spark-image
docker push gcr.io/sincere-idea-136323/shalinishukla123/spark-image
```

Commands for pushing Hadoop Namenode image:

```
docker pull bde2020/hadoop-namenode
docker tag bde2020/hadoop-namenode gcr.io/sincere-idea-136323/shalinishukla123/hadoop-namenode
docker push gcr.io/sincere-idea-136323/shalinishukla123/hadoop-namenode
```

Commands for pushing Hadoop Datanode image:

```
docker pull bde2020/hadoop-datanode
docker tag bde2020/hadoop-datanode gcr.io/sincere-idea-136323/shalinishukla123/hadoop-datanode
docker push gcr.io/sincere-idea-136323/shalinishukla123/hadoop-datanode
```

The Screenshot below shows all the images in the Container Registry -


<img width="1440" alt="Screen Shot 2021-11-28 at 3 28 43 PM" src="https://user-images.githubusercontent.com/19831012/143784731-f10aa5ff-cc5b-440b-9e67-97c3c65a8201.png">





## Steps to deploy images on GCP Kubernetes Engine -

Create a kubernetes cluster using the following commands on Cloud Shell:

```
gcloud config set project sincere-idea-136323
gcloud services enable container.googleapis.com
gcloud container clusters create --machine-type n1-standard-2 --num-nodes 2 --zone us-central1-a --cluster-version latest big-data-project
```

Navigate to Kubernetes Engine on the UI and you can see your cluster that you created -

<img width="1440" alt="Screen Shot 2021-11-28 at 3 33 38 PM" src="https://user-images.githubusercontent.com/19831012/143784918-c1a6fa24-3636-4207-a145-c7bae9270fbb.png">


Now lets create deployments for our micro-services -

### Spark

1. Create a new deployment using the Spark Image that you uploaded on the Cloud Registry by navigating to that image and clicking on Deploy to GKE option. Keep the yaml configurations as it is.
2. Once the deployment is created, create a service to expose this deployment where Target Port: 8080 Port: 8080.
3. Once the service is created, navigate to the URL 



Spark UI looks like this -


<img width="1440" alt="Screen Shot 2021-11-28 at 3 36 11 PM" src="https://user-images.githubusercontent.com/19831012/143785019-0179f920-f03a-434e-a651-9819dc698db2.png">



### Jupyter Notebook

1. Create a new deployment using the Jupyter Image that you uploaded on the Cloud Registry. Keep the yaml configurations as it is.
2. Once the deployment is created, create a service to expose this deployment where Target Port: 8888 Port: 8888.
3. Once the service is created, navigate to the URL 

Jupyter UI looks like -

<img width="1440" alt="Screen Shot 2021-11-28 at 3 36 40 PM" src="https://user-images.githubusercontent.com/19831012/143785040-e3e81ac4-b44d-4e13-87e1-5370d88f3d8e.png">




### Sonar

1. Create a new deployment using the Jupyter Image that you uploaded on the Cloud Registry. Keep the yaml configurations as it is.
2. Once the deployment is created, create a service to expose this deployment where Target Port: 9000 Port: 9000.
3. Once the service is created, navigate to the URL 

Sonar-Qube-UI looks like -


<img width="1440" alt="Screen Shot 2021-11-28 at 3 38 14 PM" src="https://user-images.githubusercontent.com/19831012/143785080-351c4ea7-ecd0-4013-9bf0-ba40f9c5c900.png">


### Hadoop Master

1. Create a deployment using the namenode image. Set the environment variables as per the hadoop-env file. Also add environment variable - CLUSTER_NAME to any name. Also change the number of replicas of deployment = 1.
2. Create a service to expose this deployment. Map two target ports. Target Port: 98700 Port: 9870 and Target Port: 9000 Port: 9000.
3. Once the service is created, navigate to the URL 


Contents of the hadoop-env file -

```
CORE_CONF_fs_defaultFS=hdfs://namenode:9000
CORE_CONF_hadoop_http_staticuser_user=root
CORE_CONF_hadoop_proxyuser_hue_hosts=*
CORE_CONF_hadoop_proxyuser_hue_groups=*
CORE_CONF_io_compression_codecs=org.apache.hadoop.io.compress.SnappyCodec
HDFS_CONF_dfs_webhdfs_enabled=true
HDFS_CONF_dfs_permissions_enabled=false
HDFS_CONF_dfs_namenode_datanode_registration_ip___hostname___check=false

```


### Hadoop Worker

1. Create a deployment using the datanode image. Set the environment variables as per the hadoop-env file. Also add environment variable SERVICE_PRECONDITION to http://namenode-service-name:9870.

Hadoop-Master-W:O-Worker UI looks like this - 

<img width="1440" alt="Screen Shot 2021-11-28 at 3 38 47 PM" src="https://user-images.githubusercontent.com/19831012/143785104-87be5ad2-073b-4825-b117-4b14c2fa3453.png">


### Application UI

Once the services for all exposed deployments come up successfully, modify your Application's index.html (the href attribute of the button html element) to point to the IP address of the micro-service that we exposed. This way we make sure that when a button corresponding to Jupyter Notebook is clicked, the UI associated with Jupyter Notebook micro-service comes up. Once again repeat the steps above, create a new image and uplodad it to Docker Hub and Google Container Registry. 


1. Create a new deployment using the Application UI Image that you uploaded on the Cloud Registry by navigating to that image and clicking on Deploy to GKE option. Keep the yaml configurations as it is. 
2. Once the deployment is created, create a service to expose this deployment where Target Port: 80 Port: 80.
3. Once the service is created, navigate to the URL. 

Our application is now up and running!


The Application-UI looks like this -


<img width="1440" alt="Screen Shot 2021-11-28 at 3 35 27 PM" src="https://user-images.githubusercontent.com/19831012/143784984-f7636c74-2aeb-4db8-8c8e-ca1ebc5a2ff9.png">


### GKE UI

Once all the services are exposed, the Services and Ingress Tab on your GCP looks like the image below -


<img width="1440" alt="Screen Shot 2021-11-28 at 3 40 01 PM" src="https://user-images.githubusercontent.com/19831012/143785141-2ef7b9f2-b493-4a6d-b990-86b690368692.png">

And all your deployments look like -

<img width="1440" alt="Screen Shot 2021-11-28 at 3 40 11 PM" src="https://user-images.githubusercontent.com/19831012/143785146-5ab3d29c-616d-41af-be7d-09bfd40f02db.png">


On Cloud Shell -

<img width="1440" alt="Screen Shot 2021-11-28 at 3 39 32 PM" src="https://user-images.githubusercontent.com/19831012/143785123-5419ebf0-043e-4245-808f-0027dd01bf46.png">



<img width="1440" alt="Screen Shot 2021-11-28 at 3 39 53 PM" src="https://user-images.githubusercontent.com/19831012/143785136-a9fdabe7-87f6-4df6-85be-64924fac75e6.png">













