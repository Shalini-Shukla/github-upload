
Steps to get the Sentiment Analyser Application run on GKE - 

Clone repository - https://github.com/rinormaloku/k8s-mastery

Navigate to your sa-frontend directory and type the following commands - 
```
npm install
npm start
npm run build
```

Navigate to your sa-webapp and type the command  - ```mvn install``` 
This will create a jar file that you will be copying to your root directory in your container as per your Dockerfile


Build images locally and push to your DockerHub - 

Navigate to your sa-frontend directory and type the following commands - 
```
docker build -f Dockerfile -t shalinishukla123/sentiment-analysis-frontend:latest .
docker push shalinishukla123/sentiment-analysis-frontend:latest
```


Navigate to your sa-webapp directory and type the following commands - 
```
docker build -f Dockerfile -t shalinishukla123/sentiment-analysis-web-app:latest .
docker push shalinishukla123/sentiment-analysis-web-app:latest
```

Navigate to your sa-logic directory and type the following commands - 
```
docker build -f Dockerfile -t shalinishukla123/sentiment-analysis-logic .
docker push shalinishukla123/sentiment-analysis-logic:latest
```


Commands for M1 Mac, the commands are as follows - 

```
docker buildx build --platform linux/amd64 -t shalinishukla123/sentiment-analysis-frontend:latest .
docker push shalinishukla123/sentiment-analysis-frontend:latest

docker buildx build --platform linux/amd64 -t shalinishukla123/sentiment-analysis-web-app:latest .
docker push shalinishukla123/sentiment-analysis-web-app:latest

docker buildx build --platform linux/amd64 -t shalinishukla123/sentiment-analysis-logic:latest .
docker push shalinishukla123/sentiment-analysis-logic:latest
```

Now, that our images are on DockerHub, lets move to GCP!


Login to your Google Cloud Platform and open Cloud Shell. All the commands mentioned below are to be typed on Cloud Shell.

Push docker images from docker hub to GCP container registry:
```
docker pull shalinishukla123/sentiment-analysis-logic:latest
docker tag shalinishukla123/sentiment-analysis-logic:latest gcr.io/sincere-idea-136323/shalinishukla123/sentiment-analysis-logic:latest
docker push gcr.io/sincere-idea-136323/shalinishukla123/sentiment-analysis-logic:latest


docker pull shalinishukla123/sentiment-analysis-frontend:latest
docker tag shalinishukla123/sentiment-analysis-frontend:latest gcr.io/sincere-idea-136323/shalinishukla123/sentiment-analysis-frontend:latest
docker push gcr.io/sincere-idea-136323/shalinishukla123/sentiment-analysis-frontend:latest



docker pull shalinishukla123/sentiment-analysis-web-app:latest
docker tag shalinishukla123/sentiment-analysis-web-app:latest gcr.io/sincere-idea-136323/shalinishukla123/sentiment-analysis-web-app:latest
docker push  gcr.io/sincere-idea-136323/shalinishukla123/sentiment-analysis-web-app:latest
```

Now, create a Kubernetes cluster using the following commands:-

```
gcloud config set project sincere-idea-136323
gcloud services enable container.googleapis.com
gcloud container clusters create --machine-type n1-standard-2 --num-nodes 2 --zone us-central1-a --cluster-version latest shalinishuklak8cluster
```

The output of the command looks like below :
```
shalini_shukla1501@cloudshell:~ (sincere-idea-136323)$ gcloud container clusters create --machine-type n1-standard-2 --num-nodes 2 --zone us-central1-a --cluster-version latest shalinishukla123
WARNING: Currently VPC-native is the default mode during cluster creation for versions greater than 1.21.0-gke.1500. To create advanced routes based clusters, please pass the `--no-enable-ip-alias` flag
WARNING: Starting with version 1.18, clusters will have shielded GKE nodes by default.
WARNING: Your Pod address range (`--cluster-ipv4-cidr`) can accommodate at most 1008 node(s).
WARNING: Starting with version 1.19, newly created clusters and node-pools will have COS_CONTAINERD as the default node image when no image type is specified.
Creating cluster shalinishukla123 in us-central1-a...done.     
Created [https://container.googleapis.com/v1/projects/sincere-idea-136323/zones/us-central1-a/clusters/shalinishukla123].
To inspect the contents of your cluster, go to: https://console.cloud.google.com/kubernetes/workload_/gcloud/us-central1-a/shalinishukla123?project=sincere-idea-136323
kubeconfig entry generated for shalinishukla123.
NAME: shalinishukla123
LOCATION: us-central1-a
MASTER_VERSION: 1.21.4-gke.2300
MASTER_IP: 34.70.165.194
MACHINE_TYPE: n1-standard-2
NODE_VERSION: 1.21.4-gke.2300
NUM_NODES: 2
STATUS: RUNNING
```

You can verify nodes using command - ```kubectl get nodes```
You can verify pod creation using command - ```kubectl get pods```


Now your kubernetes cluster is up.
Next step is to create deployments for frontend, web app and logic on this newly created cluster.

I went with the bottom up approach, which means I first created my logic deployment, then web-app deployment and lastly my front-end deployment.


SA-Logic Deployment Creation Steps - 
Go to Container Registry -> Click on the SA-Logic Image -> There will be an option called Deploy on the top, click on it -> Choose Deploy to GKE
This will automatically generate a yaml for you. Enter the new deployment name(‘sa-logic’ in my case) and press Confirm.
This will create an SA Logic Deployment with 3 pods in it.


SA-Logic Service Creation Steps -
Once the deployment is created, go to the Google Kubernetes Engine and go to Workloads on the left panel.
You will be able to see your SA-Logic deployment on the screen. Click on it and on the right there will be an option called “Expose”
Click on that and enter target port as 5000 and internal port as 5050. Click confirm and wait for the service to come up.
You can verify the service by going to 'Service and Ingress' option on the left panel of Google Kubernetes Engine. 
Make a note of the ip and port of the SA-logic service.


SA-Web App Deployment Creation Steps - 
Go to Container Registry -> Click on the SA-Webapp image -> There will be an option called Deploy on the top, click on it -> Choose Deploy to GKE

This will automatically generate a yaml for you. Enter the new deployment name(‘sa-webapp’ in my case). 
Ans Add environment variable:-
key: SA_LOGIC_API_URL 
value: http://sa_logic_ip:5050/     <========= this contains the sa_logic service ip that you copied in the last step

Press confirm. You will be able to see your SA-Webapp deployment on the screen. You can also confirm this by running “kubectl get pods” on cloud shell.


SA-Web App Service Creation Steps -
Once the deployment is created, go to the Google Kubernetes Engine and go to workloads on the left panel.
You will be able to see your SA-Webapp deployment on the screen. Click on it and on the right there will be an option called “Expose”
Click on that and enter target port as 8080 and internal port as 8080. Click confirm and wait for the service to come up.
You can verify the service by going to 'Service and Ingress' option on the left panel of Google Kubernetes Engine. Make a note of the external ip of the SA-Webapp service.


Before running your front-end deployment, you need to make changes to your App.js file.

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            sentence: '',
            polarity: undefined
        };
    };

    analyzeSentence() {
        fetch('http://35.193.3.211:8080/sentiment',            <==================== this should be the External IP of the Web-App Service from the previous step
       { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({sentence: this.textField.getValue()})
        })

Once you make this change, run command - ```npm run build``` and create a new docker image for SA-frontend and push it to docker hub and GCP Container registry. Once done follow the exact same steps as above to create SA-Frontend deployment and service. In this case, the target port and the internal port is 80. Once the SA-Frontend service is exposed, you can click on its external IP and voila! your sentimental analyser app is live!!!