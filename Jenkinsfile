// Jenkinsfile (or Jenkinsfile_Consumer) for microservice_pacts repository

pipeline {
    agent any

    environment {
        PACTFLOW_BASE_URL = 'https://nitc-0bb42495.pactflow.io'
        PACTFLOW_TOKEN = credentials('PACTFLOW_TOKEN')
        GIT_COMMIT = "${env.GIT_COMMIT ?: 'HEAD'}"
        GIT_BRANCH = "${env.BRANCH_NAME ?: 'main'}"
    }

    stages {
        stage('Initialize Workspace and Navigate') {
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
                    bat 'py -m pip install --upgrade pip'
                    bat 'pip install virtualenv'
                    bat 'py -m venv venv'
                    // Activate virtual environment and install Python pact dependencies
                    bat 'venv\\Scripts\\activate.bat && pip install pytest pact-python requests'
                    echo "Python dependencies installed."

                    // --- DIAGNOSTIC STEPS ---
                    echo "Verifying Python environment..."
                    bat 'venv\\Scripts\\activate.bat && where python' // Show which python is being used
                    bat 'venv\\Scripts\\activate.bat && pip freeze'  // List installed packages
                    bat 'venv\\Scripts\\activate.bat && pytest --version' // Show pytest version and plugins
                    bat 'venv\\Scripts\\activate.bat && pytest --help | findstr pact' // Check if --pact-dir is mentioned in help
                    // --- END DIAGNOSTIC STEPS ---
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
                    // Run pytest to generate pact files for Python consumers
                    // The --pact-dir=./pacts argument tells pact-python to save the generated pact files
                    // in the 'pacts' subdirectory within the 'tests' folder.
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
                    bat 'cmd /c "npm install -g @pact-foundation/pact-cli || exit /b 0"'

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