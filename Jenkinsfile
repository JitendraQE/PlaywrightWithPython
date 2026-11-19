pipeline {
    agent any

    stages {
        
        stage('Docker Verification') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh '''
                    docker run --rm --ipc=host \
                      -v "$WORKSPACE:/app" \
                      -w /app \
                      mcr.microsoft.com/playwright/python:v1.64.1-noble \
                      bash -c "python -m pip install -r requirements.txt && pytest -v"
                '''
            }
        }
    }
}