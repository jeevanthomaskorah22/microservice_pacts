pipeline {
    agent any

    environment {
        PACTFLOW_BASE_URL = 'https://nitc-0bb42495.pactflow.io'
        PACTFLOW_TOKEN = credentials('PACTFLOW_TOKEN')  // Create in Jenkins credentials
        GIT_COMMIT = "${env.GIT_COMMIT ?: 'HEAD'}"
        GIT_BRANCH = "${env.BRANCH_NAME ?: 'main'}"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/jeevanthomaskorah22/microservice_pacts', branch: 'main'
            }
        }

        stage('Set Up Python Virtual Environment') {
            steps {
                dir('tests') {
                    echo 'Creating virtual environment...'
                    bat 'py -m venv venv'
                    echo 'Installing required Python packages...'
                    bat 'venv\\Scripts\\python.exe -m pip install pact-python pytest requests'
                }
            }
        }

        stage('Run Consumer Tests (Generate Pacts)') {
            steps {
                dir('tests') {
                    echo 'Running consumer Pact tests to auto-start mock server and generate pacts...'
                    bat 'venv\\Scripts\\python.exe -m pytest order_product.py'
                }
            }
        }

        stage('Install Pact CLI (Node.js based)') {
            steps {
                dir('tests') {
                    echo 'Installing Pact CLI using npm...'
                    bat 'npm install -g @pact-foundation/pact-cli || exit /b 0'
                }
            }
        }

        stage('Publish Pacts to PactFlow') {
            steps {
                dir('tests') {
                    echo 'Publishing pacts to PactFlow...'
                    bat """
                    pact publish pacts ^
                      --consumer-version="${GIT_COMMIT}" ^
                      --tag="${GIT_BRANCH}" ^
                      --broker-base-url="${PACTFLOW_BASE_URL}" ^
                      --broker-token="${PACTFLOW_TOKEN}"
                    """
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
        failure {
            echo '❌ Pipeline failed! Check logs for more details.'
        }
        success {
            echo '✅ Pact consumer contract published successfully!'
        }
    }
}
