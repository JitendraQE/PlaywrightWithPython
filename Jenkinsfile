
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
                withCredentials([
                    usernamePassword(
                        credentialsId: 'playwright-login',
                        usernameVariable: 'LOGIN_USERNAME',
                        passwordVariable: 'LOGIN_PASSWORD'
                    )
                ]) {
                    sh '''
                        docker run --rm --ipc=host \
                          -e LOGIN_USERNAME \
                          -e LOGIN_PASSWORD \
                          -v jenkins_home:/jenkins_home \
                          -w /jenkins_home/workspace/PlaywrightWithPython \
                          mcr.microsoft.com/playwright/python:v1.64.1-noble \
                          bash -c "python -m pip install -r requirements.txt && python -m pytest -v"
                    '''
                }
            }
        }
    }
}