pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/mohamedYassinChayada/mock_flask.git'
            }
        }

        stage('Build') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install flake8
                    echo "=== Checking for syntax errors and code issues ==="
                    flake8 *.py --count --select=E9,F63,F7,F82 --show-source --statistics
                    echo "=== Full lint report ==="
                    flake8 *.py --count --max-line-length=120 --statistics
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install pytest
                    python -m pytest --junitxml=test-results.xml -v
                '''
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