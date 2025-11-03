pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/shubhammks/sketch_using_flask_cv2_html.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                . venv/bin/activate
                nohup python3 app.py &
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Flask App is running successfully!'
            echo '🌐 Access it at http://localhost:5000'
        }
        failure {
            echo '❌ Build or Run failed. Check Jenkins console for details.'
        }
    }
}
