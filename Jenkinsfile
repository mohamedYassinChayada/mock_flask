pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/mohamedYassinChayada/mock_flask.git'
            }
        }

        stage('Build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'python -m pytest --junitxml=test-results.xml || true'
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: '**/*.py', allowEmptyArchive: true
                junit allowEmptyResults: true, testResults: 'test-results.xml'
            }
        }
    }
} 