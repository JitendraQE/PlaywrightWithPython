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
                      -v jenkins_home:/jenkins_home \
                      -w /jenkins_home/workspace/PlaywrightWithPython \
                      mcr.microsoft.com/playwright/python:v1.64.1-noble \
                      bash -c "python -m pip install -r requirements.txt && python -m pytest -v"
                '''
            }
        }
    }
}