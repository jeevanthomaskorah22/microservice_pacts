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
                    bat 'venv\\Scripts\\activate.bat && pip install pytest pact-python requests'
                    echo "Python dependencies installed."

                    // --- DIAGNOSTIC STEPS (Good to keep these for now) ---
                    echo "Verifying Python environment..."
                    bat 'venv\\Scripts\\activate.bat && where python'
                    bat 'venv\\Scripts\\activate.bat && pip freeze'
                    bat 'venv\\Scripts\\activate.bat && pytest --version'
                    bat 'venv\\Scripts\\activate.bat && pytest --help | findstr pact'
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
                    // *** CRITICAL CHANGE HERE: Explicitly run pytest as a module ***
                    bat 'venv\\Scripts\\python.exe -m pytest order_product.py payment-order.py --pact-dir=.\\pacts'
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