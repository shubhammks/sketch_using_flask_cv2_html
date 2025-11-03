pipeline {
    agent any

    environment {
        IMAGE_NAME = "shubhammlks/flask-cv2-app"
        IMAGE_TAG = "latest"
        DOCKER_CREDS = "dockerhub-creds"   // create in Jenkins → Credentials
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/shubhammlks/sketch_using_flask_cv2_html.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo "✅ No unit tests configured for this project"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                            docker tag ${IMAGE_NAME}:${IMAGE_TAG} $DOCKER_USER/${IMAGE_NAME}:${IMAGE_TAG}
                            docker push $DOCKER_USER/${IMAGE_NAME}:${IMAGE_TAG}
                            docker logout
                        '''
                    }
                }
            }
        }

        stage('Deploy Locally') {
            steps {
                script {
                    sh '''
                        docker rm -f flask-cv2-container || true
                        docker run -d --name flask-cv2-container -p 5000:5000 ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "🎉 Build, Push & Deploy completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check console logs."
        }
    }
}
