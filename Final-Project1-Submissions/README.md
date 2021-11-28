# Project 1 Final Submission

The aim of this project is to build a microservice-based application that would allow users to run Apache Hadoop, Spark, Jupyter Notebooks, SonarQube and SonarScanner without having to install any of them. 

In order to implement this, we will have to first push all the necessary containers on GCP Container registry. Create a kubernetes cluster using Google Kubernetes Engine and deploy these images on it as pods. One of the pods will be the Application UI that will allow the user to click on a button that would re-direct them to the respective microservice.


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


## Steps to push all images on GCP Container Registry -

Commands for pushing application UI:

```
docker pull shalinishukla123/bigdatapythonapp
docker tag shalinishukla123/bigdatapythonapp gcr.io/sincere-idea-136323/shalinishukla123/bigdatapythonapp
docker push gcr.io/sincere-idea-136323/shalinishukla123/bigdatapythonapp
```

Commands for pushing Jupyter notebook image:

```
docker pull jupyter/minimal-notebook
docker tag jupyter/minimal-notebook gcr.io/sincere-idea-136323/shalinishukla123/
docker push gcr.io/sincere-idea-136323/shalinishukla123/
```

Commands for pushing Sonar Scanner image:

```
docker pull shalinishukla123/sonarscanner
docker tag shalinishukla123/sonarscanner gcr.io/sincere-idea-136323/shalinishukla123/
docker push gcr.io/sincere-idea-136323/shalinishukla123/
```

Commands for pushing Spark image:

```
docker pull bitnami/spark
docker tag bitnami/spark gcr.io/sincere-idea-136323/shalinishukla123/
docker push gcr.io/sincere-idea-136323/shalinishukla123/
```

Commands for pushing Hadoop Namenode image:

```
docker pull bde2020/hadoop-namenode
docker tag bde2020/hadoop-namenode gcr.io/sincere-idea-136323/shalinishukla123/
docker push gcr.io/sincere-idea-136323/shalinishukla123/
```

Commands for pushing Hadoop Datanode image:

```
docker pull bde2020/hadoop-datanode
docker tag bde2020/hadoop-datanode gcr.io/sincere-idea-136323/shalinishukla123/
docker push gcr.io/sincere-idea-136323/shalinishukla123/
```

The Screenshot below shows all the images in the Container Registry -




## Steps to deploy images on GCP Kubernetes Engine -

Create a cluster using the following commands on Cloud Shell:

```
gcloud config set project sincere-idea-136323
gcloud services enable container.googleapis.com
gcloud container clusters create --machine-type n1-standard-2 --num-nodes 2 --zone us-central1-a --cluster-version latest k8cluster
```





### Application UI

1. Create a new deployment using the Application UI Image that you uploaded on the Cloud Registry. Keep the yaml configurations as it is. 
2. Create a service to expose this deployment where Target Port: 80 Port: 80.
3. Once the service is created, navigate to the URL 

See the Application-UI screenshot for how the UI looks like.

### Spark

1. Create a new deployment using the Spark Image that you uploaded on the Cloud Registry. Keep the yaml configurations as it is.
2. Create a service to expose this deployment where Target Port: 8080 Port: 8080.
3. Once the service is created, navigate to the URL 

See Sparks-UI screenshot for how the UI looks like.

### Jupyter Notebook

1. Create a new deployment using the Jupyter Image that you uploaded on the Cloud Registry. Keep the yaml configurations as it is.
2. Create a service to expose this deployment where Target Port: 8888 Port: 8888.
3. Once the service is created, navigate to the URL 

See Jupyter-UI screenshot for how the UI looks like.

### Sonar

1. Create a new deployment using the Jupyter Image that you uploaded on the Cloud Registry. Keep the yaml configurations as it is.
2. Create a service to expose this deployment where Target Port: 9000 Port: 9000.
3. Once the service is created, navigate to the URL 

See Sonar-Qube-UI screenshot for how the UI looks like.

### Hadoop Master

1. Create a deployment using the namenode image. Set the environment variables as per the hadoop-env file. Also add environment variable - CLUSTER_NAME to any name. Also change the number of replicas of deployment = 1.
2. Create a service to expose this deployment. Map two target ports. Target Port: 98700 Port: 9870 and Target Port: 9000 Port: 9000.
3. Once the service is created, navigate to the URL 

### Hadoop Worker

1. Create a deployment using the datanode image. Set the environment variables as per the hadoop-env file. Also add environment variable SERVICE_PRECONDITION to http://namenode-service-name:9870.

See Hadoop-Master-W:O-Worker screenshot for how the UI looks like. 
