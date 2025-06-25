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

                    // 1. Ensure global pip is up-to-date and virtualenv is installed globally
                    //    Using 'py' is fine as it uses the default python on PATH.
                    bat 'py -m pip install --upgrade pip'
                    bat 'py -m pip install virtualenv'

                    // 2. Create the virtual environment using the system Python
                    bat 'py -m venv venv'

                    // 3. Install dependencies *into the virtual environment*
                    //    Explicitly use the python.exe inside the venv for all venv-related pip commands.
                    bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip' // Update venv's pip
                    bat 'venv\\Scripts\\python.exe -m pip install pytest pact-python requests'

                    echo "Python dependencies installed."

                    // --- DIAGNOSTIC STEPS (Good to keep these for now) ---
                    echo "Verifying Python environment..."
                    // Use 'activate.bat && command' for commands that rely on PATH being set by activate.
                    // For direct Python commands in venv, use venv\Scripts\python.exe.
                    bat 'venv\\Scripts\\activate.bat && where python' // Shows python from venv first
                    bat 'venv\\Scripts\\python.exe -m pip freeze'  // List installed packages in venv
                    bat 'venv\\Scripts\\python.exe -m pytest --version' // Show pytest version from venv
                    // Make findstr non-failing, as no match returns exit code 1.
                    bat 'venv\\Scripts\\activate.bat && pytest --help | findstr pact || exit /b 0'
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
                    // Explicitly run pytest as a module using the venv's python.
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