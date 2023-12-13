# Play with Kubernetes

# Google Cloud and GKE Setup Guide

This guide walks you through the process of setting up Google Cloud, authenticating Docker with Google Container Registry (GCR), building a Docker image, creating a GKE cluster, and deploying a service into GKE.

## 1. Google Cloud Setup

1.1. **Create a Google Cloud Project:**
   - Visit the [Google Cloud Console](https://console.cloud.google.com/).
   - Click on the project dropdown in the top navigation bar and click "New Project."
   - Enter a project name and click "Create."

1.2. **Enable Billing:**
   - In the Google Cloud Console, navigate to "Billing."
   - Link your project to a billing account.

1.3. **Enable APIs:**
   - Enable the Kubernetes Engine API:
     ```bash
     gcloud services enable container.googleapis.com --project=your-project-id
     ```

## 2. Authenticate Docker with GCR

2.1. **Install Google Cloud SDK:**
   - Follow the instructions [here](https://cloud.google.com/sdk/docs/install) to install the Google Cloud SDK.

2.2. **Configure Docker to Use GCR Credentials:**
   - Run the following command:
     ```bash
     gcloud auth configure-docker
     ```

## 3. Build Docker Image

3.1. **Build your Docker Image:**
   - Navigate to your project directory containing the Dockerfile.
   - Run:
     ```bash
     docker build -t gcr.io/your-project-id/your-image:your-tag .
     ```

3.2. **Push Docker Image to GCR:**
   - Run:
     ```bash
     docker push gcr.io/your-project-id/your-image:your-tag
     ```

## 4. Create GKE Cluster

4.1. **Create GKE Cluster:**
   - Run the following command to create a GKE cluster:
     ```bash
     gcloud container clusters create your-cluster-name --num-nodes=1 --zone=your-preferred-zone
     ```

4.2. **Get Cluster Credentials:**
   - Run:
     ```bash
     gcloud container clusters get-credentials your-cluster-name --zone=your-preferred-zone
     ```

## 5. Deploy Service into GKE

5.1. **Deploy your Service:**
   - Create a Kubernetes deployment and service YAML file (e.g., `deployment.yaml` and `service.yaml`).
   - Apply the configuration:
     ```bash
     kubectl apply -f deployment.yaml
     kubectl apply -f service.yaml
     ```

5.2. **Access Your Service:**
   - After deployment, get the external IP using:
     ```bash
     kubectl get services
     ```
   - Access your service at the provided external IP.

5.3. **Alternative: Use `kubectl port-forward` to Access Your Service:**
   - If you are unable to get an external IP for your service, you can use `kubectl port-forward` to access it directly from your local machine.
   - Identify the name of your pod:
     ```bash
     kubectl get pods
     ```
   - Run the following command to forward a local port to a port on the pod:
     ```bash
     kubectl port-forward your-pod-name 8080:5000
     ```
   - Access your service at `http://localhost:8080` in your web browser.


