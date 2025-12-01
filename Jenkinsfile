pipeline {
    agent any
    
    environment {
        // Suppress pip and python verbose output
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        PIP_NO_WARN_SCRIPT_LOCATION = '1'
        PYTHONDONTWRITEBYTECODE = '1'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                // Clean checkout without excessive git output
                checkout scmGit(
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/mohamedYassinChayada/mock_flask.git']]
                )
                script {
                    echo "=========================================="
                    echo "CHECKOUT COMPLETE"
                    echo "=========================================="
                    echo "Branch: main"
                    echo "Commit: ${env.GIT_COMMIT ?: 'unknown'}"
                }
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    echo "=========================================="
                    echo "SETTING UP ENVIRONMENT"
                    echo "=========================================="
                    python3 -m venv venv --quiet 2>/dev/null || python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt --quiet 2>&1 | grep -E "(ERROR|error:|Successfully)" || true
                    pip install flake8 pytest pytest-json-report --quiet 2>&1 | grep -E "(ERROR|error:|Successfully)" || true
                    echo "Environment setup complete"
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    
                    echo "=========================================="
                    echo "LINT CHECK - SYNTAX ERRORS"
                    echo "=========================================="
                    
                    # Run lint with clean output - only errors
                    flake8 *.py --format='[LINT ERROR] %(path)s:%(row)d:%(col)d: %(code)s - %(text)s' \
                        --select=E9,F63,F7,F82 --show-source 2>&1 || {
                        echo ""
                        echo "=========================================="
                        echo "LINT FAILED - Fix the errors above"
                        echo "=========================================="
                        exit 1
                    }
                    
                    echo ""
                    echo "=========================================="
                    echo "LINT CHECK - CODE QUALITY"
                    echo "=========================================="
                    
                    # Run full lint check but don't fail on style issues
                    flake8 *.py --format='[LINT WARNING] %(path)s:%(row)d:%(col)d: %(code)s - %(text)s' \
                        --max-line-length=120 --ignore=E9,F63,F7,F82 2>&1 || true
                    
                    echo "Lint check complete"
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    
                    echo "=========================================="
                    echo "RUNNING TESTS"
                    echo "=========================================="
                    
                    # Run pytest with verbose output and clear formatting
                    python -m pytest test_app.py \
                        -v \
                        --tb=short \
                        --no-header \
                        --junitxml=test-results.xml \
                        2>&1 || {
                        
                        echo ""
                        echo "=========================================="
                        echo "TESTS FAILED - See errors above"
                        echo "=========================================="
                        exit 1
                    }
                    
                    echo ""
                    echo "=========================================="
                    echo "ALL TESTS PASSED"
                    echo "=========================================="
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
    
    post {
        always {
            echo "=========================================="
            echo "BUILD SUMMARY"
            echo "=========================================="
            echo "Status: ${currentBuild.currentResult}"
            echo "Duration: ${currentBuild.durationString}"
            echo "Build URL: ${env.BUILD_URL}"
        }
        
        failure {
            echo ""
            echo "=========================================="
            echo "BUILD FAILED"
            echo "=========================================="
            echo "Review the errors above to fix the issue."
            echo "Common fixes:"
            echo "  - Syntax errors: Check for typos like 'retursn' instead of 'return'"
            echo "  - Import errors: Ensure all dependencies are in requirements.txt"
            echo "  - Test failures: Check test assertions and expected values"
        }
        
        success {
            echo ""
            echo "=========================================="
            echo "BUILD SUCCEEDED"
            echo "=========================================="
        }
    }
}
