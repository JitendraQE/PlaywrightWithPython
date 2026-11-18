pipeline {
    agent any

    stages {

        stage('Docker Verification') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Python Verification') {
            steps {
                sh '''
                    docker run --rm \
                      mcr.microsoft.com/playwright/python:v1.64.1-noble \
                      python --version
                '''
            }
        }

        stage('Playwright Verification') {
            steps {
                sh '''
                    docker run --rm \
                      mcr.microsoft.com/playwright/python:v1.64.1-noble \
                      bash -c "python -m pip install playwright==1.64.1 && python -c \\"import playwright; print('Playwright working')\\""
                '''
            }
        }
    }
}
