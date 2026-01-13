pipeline {
    agent any

    environment {
        // Using the IDs we created in Jenkins Credentials
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        DOCKER_USER = 'rahulgoud21' 
    }

    stages {
        stage('Checkout') {
            steps {
                // Pulling your latest code from GitHub
                git branch: 'main', 
                    credentialsId: 'github-creds', 
                    url: 'https://github.com/rahulgoud213/my-microservices.git'
            }
        }

        stage('Build & Push Backend') {
            steps {
                dir('backend') {
                    script {
                        // 🛠️ Build the backend image
                        sh "docker build -t ${DOCKER_USER}/backend:latest ."
                        
                        // 🔐 Login and Push to Docker Hub
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
                        // 🛠️ Build the frontend image
                        sh "docker build -t ${DOCKER_USER}/frontend:latest ."
                        
                        // 🚀 Push to Docker Hub
                        sh "docker push ${DOCKER_USER}/frontend:latest"
                        sh "sed -i '' 's|http://localhost:5001|http://backend-service:5001|g' index.html"
                    }
                }
            }
        }

stage('Build & Push Frontend') {
    steps {
        dir('frontend') {
            script {
                // 🛠️ Build the frontend image
                sh "docker build -t ${DOCKER_USER}/frontend:latest ."
                
                // 🚀 Push to Docker Hub
                sh "docker push ${DOCKER_USER}/frontend:latest"

                // 🔄 The sed command
                sh "sed -i '' 's|http://localhost:5001|http://backend-service:5001|g' index.html"
            }
        }
    }
}

    post {
        always {
            // 🧹 Clean up the workspace to save space on your Mac
            cleanWs()
        }
    }
}