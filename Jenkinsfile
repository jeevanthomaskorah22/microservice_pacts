// Jenkinsfile (or Jenkinsfile_Consumer) for microservice_pacts repository

pipeline {
    agent any // Or a specific agent with necessary tools (e.g., agent { label 'my-windows-agent' })

    environment {
        PACTFLOW_BASE_URL = 'https://nitc-0bb42495.pactflow.io'
        PACTFLOW_TOKEN = credentials('PACTFLOW_AUTH_TOKEN')
        GIT_COMMIT = "${env.GIT_COMMIT ?: 'HEAD'}"
        GIT_BRANCH = "${env.BRANCH_NAME ?: 'main'}"
    }

    stages {
        stage('Checkout Source') {
            steps {
                script {
                    echo "Workspace: ${WORKSPACE}"
                    dir('tests') {
                        echo "Navigated to tests directory: ${pwd()}"
                    }
                }
            }
        }

        stage('Install Python Dependencies') {
            steps {
                dir('tests') {
                    echo "Installing Python dependencies..."
                    // Use 'bat' for Windows Batch commands
                    bat 'py -m pip install --upgrade pip' // Use 'py' for Python launcher on Windows
                    bat 'pip install virtualenv'
                    bat 'py -m venv venv'
                    // Activate virtual environment and install Python pact dependencies
                    // For Windows, activation script is `venv\Scripts\activate.bat`
                    bat 'venv\\Scripts\\activate.bat && pip install pytest pact-python requests'
                    echo "Python dependencies installed."
                }
            }
        }

        stage('Install Node.js Dependencies') {
            steps {
                dir('tests') {
                    echo "Installing Node.js dependencies..."
                    bat 'npm install'
                    echo "Node.js dependencies installed."
                }
            }
        }

        stage('Run Python Consumer Tests') {
            steps {
                dir('tests') {
                    echo "Running Python consumer tests to generate pacts..."
                    // Activate and run pytest
                    bat 'venv\\Scripts\\activate.bat && pytest order_product.py payment-order.py --pact-dir=.\\pacts'
                    echo "Python Pact files generated in ${pwd()}\\pacts"
                }
            }
        }

        stage('Run Node.js Consumer Tests') {
            steps {
                dir('tests') {
                    echo "Running Node.js consumer tests to generate pacts..."
                    bat 'npm test'
                    echo "Node.js Pact files generated in ${pwd()}\\pacts"
                }
            }
        }

        stage('Publish Pacts to PactFlow') {
            steps {
                dir('tests') {
                    echo "Publishing Pact files to PactFlow..."
                    // Install pact-cli
                    bat 'npm install -g @pact-foundation/pact-cli || exit /b 0' // || exit /b 0 for "ignore errors" in batch

                    // Publish all pact files found in the 'pacts' directory.
                    // Note: Line continuation in batch is different (^) but for long commands,
                    // it's often easier to put it on one line or use a separate .bat script.
                    // For readability, I'll keep it on one line here.
                    bat """
                        pact publish .\\pacts\\*.json --consumer-version="${GIT_COMMIT}" --tag="${GIT_BRANCH}" --broker-base-url="${PACTFLOW_BASE_URL}" --broker-token="${PACTFLOW_TOKEN}"
                    """
                    echo "Pact files published to PactFlow successfully."
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up workspace..."
            cleanWs()
            echo "Workspace cleaned."
        }
        failure {
            echo "Pipeline failed! Check logs for details."
        }
        success {
            echo "Pipeline completed successfully!"
        }
    }
}