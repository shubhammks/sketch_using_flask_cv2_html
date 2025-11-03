pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/shubhammks/sketch_using_flask_cv2_html.git'
        BRANCH = 'main'
        IMAGE_NAME = 'flask_sketch_app'
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo '📥 Cloning repository...'
                git branch: "${BRANCH}", credentialsId: 'github-token', url: "${REPO_URL}"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running tests (if any)...'
                // Optional: run python tests if available
                sh '''
                    if [ -f "test_app.py" ]; then
                        echo "Running Python tests..."
                        python3 -m unittest discover
                    else
                        echo "No test file found, skipping..."
                    fi
                '''
            }
        }

        stage('Deploy Locally') {
            steps {
                echo '🚀 Deploying container locally...'
                // Stop and remove any old container first
                sh '''
                    docker ps -q --filter "name=flask_app" | grep -q . && docker stop flask_app && docker rm flask_app || true
                    docker run -d -p 5000:5000 --name flask_app ${IMAGE_NAME}:latest
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment Successful! Flask app running at http://localhost:5000'
        }
        failure {
            echo '❌ Build or Deployment Failed. Check logs.'
        }
    }
}
