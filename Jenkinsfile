// Jenkinsfile (complete) for publishing and verifying Pact contracts

pipeline {
    agent any

    environment {
        PACTFLOW_BASE_URL = 'https://nitc-0bb42495.pactflow.io'
        PACTFLOW_TOKEN = credentials('PACTFLOW_TOKEN')
        GIT_COMMIT = "${env.GIT_COMMIT ?: 'HEAD'}"
        GIT_BRANCH = "${env.BRANCH_NAME ?: 'main'}"
    }

    stages {
        stage('Navigate to Tests Directory') {
            steps {
                dir('tests') {
                    echo "Entered tests directory: ${pwd()}"
                }
            }
        }

        stage('Install Python Dependencies') {
            steps {
                dir('tests') {
                    bat 'py -m pip install --upgrade pip'
                    bat 'pip install virtualenv'
                    bat 'py -m venv venv'
                    bat 'call venv\\Scripts\\activate.bat && pip install pytest pact-python requests'
                    bat 'call venv\\Scripts\\activate.bat && pytest --version'
                }
            }
        }

        stage('Install Node.js Dependencies') {
            steps {
                dir('tests') {
                    bat 'npm install'
                }
            }
        }

        stage('Run Python Consumer Tests') {
            steps {
                dir('tests') {
                    bat 'call venv\\Scripts\\activate.bat && pytest order_product.py payment-order.py --pact-dir=.\\pacts'
                }
            }
        }

        stage('Run Node.js Consumer Tests') {
            steps {
                dir('tests') {
                    bat 'npm test'
                }
            }
        }

        stage('Publish Pact Files to PactFlow') {
            steps {
                dir('tests') {
                    echo "Publishing pact files to PactFlow..."
                    bat "pact publish .\\pacts\\*.json --consumer-version=\"${GIT_COMMIT}\" --tag=\"${GIT_BRANCH}\" --broker-base-url=\"${PACTFLOW_BASE_URL}\" --broker-token=\"${PACTFLOW_TOKEN}\""
                }
            }
        }

        stage('Verify Pact Files (Optional)') {
            steps {
                dir('tests') {
                    // Only needed if you're verifying from consumer side using CLI
                    echo "You can run verification CLI manually as needed."
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning workspace..."
            cleanWs()
        }
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed. Check logs for errors."
        }
    }
}
