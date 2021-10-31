# Project 1 Checkpoint 1

List of images used for this Checkpoint:

1. Hadoop Worker - https://hub.docker.com/r/bde2020/hadoop-datanode
2. Hadoop Master - https://hub.docker.com/r/bde2020/hadoop-namenode
3. Jupyter Notebook - https://hub.docker.com/r/jupyter/minimal-notebook
4. Spark - https://hub.docker.com/r/bitnami/spark
5. Sonar - https://hub.docker.com/r/shalinishukla123/sonarscanner
6. Application UI - https://hub.docker.com/r/shalinishukla123/bigdatapythonapp


## Steps to deploy all images on GCP Kubernetes Engine -

Create a cluster using the following commands on Cloud Shell:

```
gcloud config set project sincere-idea-136323
gcloud services enable container.googleapis.com
gcloud container clusters create --machine-type n1-standard-2 --num-nodes 2 --zone us-central1-a --cluster-version latest k8cluster
```

Upload all the above images on Cloud Registry using the following commands:

```
docker pull shalinishukla123/bigdatapythonapp
docker tag docker pull shalinishukla123/bigdatapythonapp gcr.io/sincere-idea-136323/shalinishukla123/bigdatapythonapp
docker push gcr.io/sincere-idea-136323/shalinishukla123/bigdatapythonapp
```

Do this for all the images.


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
