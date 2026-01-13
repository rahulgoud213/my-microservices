pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        DOCKER_USER = 'rahulgoud21' 
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    credentialsId: 'github-creds', 
                    url: 'https://github.com/rahulgoud213/my-microservices.git'
            }
        }

        stage('Build & Push Backend') {
            steps {
                dir('backend') {
                    script {
                        sh "docker build -t ${DOCKER_USER}/backend:latest ."
                        sh "echo \$DOCKERHUB_CREDENTIALS_PSW | docker login -u \$DOCKERHUB_CREDENTIALS_USR --password-stdin"
                        sh "docker push ${DOCKER_USER}/backend:latest"
                    }
                }
            }
        }

        stage('Build & Push Frontend') {
            steps {
                dir('frontend') {
                    script {
                        // 1. Run sed FIRST to update the file in the workspace 🔄
                        sh "sed -i '' 's|http://localhost:5001|http://backend-service:5001|g' index.html"
                        
                        // 2. Build the image with the modified file 🏗️
                        sh "docker build -t ${DOCKER_USER}/frontend:latest ."
                        
                        // 3. Push the image 🚀
                        sh "docker push ${DOCKER_USER}/frontend:latest"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh "kubectl apply -f k8s/"
                    sh "kubectl rollout restart deployment/backend-deployment"
                    sh "kubectl rollout restart deployment/frontend-deployment"
                }
            }
        }
    } // This closes 'stages'

    post {
        always {
            cleanWs()
        }
    }
}