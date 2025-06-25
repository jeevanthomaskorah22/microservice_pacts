pipeline {
    agent any

    environment {
        PACTFLOW_BASE_URL = 'https://nitc-0bb42495.pactflow.io'
        PACTFLOW_TOKEN = credentials('PACTFLOW_TOKEN')
        PATH = "C:\\Ruby32-x64\\bin;%PATH%" // Ruby PATH addition is fine
        // Define the absolute path to your Python executable
        PYTHON_EXE_PATH = "C:\\Program Files\\Python312\\python.exe" // <-- REPLACE THIS WITH YOUR ACTUAL PATH
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/jeevanthomaskorah22/microservice_pacts', branch: 'main'
            }
        }

        stage('Setup Python Virtual Env') {
            steps {
                dir('tests') {
                    echo "Creating Python virtual environment..."
                    // Use the absolute path to python.exe for venv creation
                    bat "${PYTHON_EXE_PATH} -m venv venv"

                    echo "Upgrading pip in virtual environment..."
                    // Explicitly use the venv's python.exe for all venv operations
                    bat "venv\\Scripts\\python.exe -m pip install --upgrade pip"

                    echo "Installing Python dependencies (pytest, pact-python, requests)..."
                    // Install dependencies directly into the venv using its python.exe
                    bat "venv\\Scripts\\python.exe -m pip install pytest pact-python requests"

                    // --- Optional Diagnostic Steps ---
                    echo "Verifying venv Python and installed packages..."
                    bat "venv\\Scripts\\python.exe --version"
                    bat "venv\\Scripts\\python.exe -m pip freeze"
                    bat "venv\\Scripts\\pytest.exe --version" // Verify pytest is recognized from venv
                    // --- End Diagnostic Steps ---
                }
            }
        }

        stage('Run Consumer Pact Tests') {
            steps {
                dir('tests') {
                    echo "Running Python consumer pact tests..."
                    // Directly call pytest from the virtual environment
                    // Removed 'activate.bat &&' as it's not strictly necessary if you're directly invoking
                    // the venv's executables. `--capture=tee-sys` is good for Jenkins logs.
                    bat "venv\\Scripts\\pytest.exe order_product.py payment-order.py --pact-dir=.\\pacts --capture=tee-sys"
                }
            }
        }

        stage('Publish Pact to PactFlow') {
            steps {
                dir('tests') {
                    // Install pact-cli globally on the agent machine for simplicity here.
                    // If you want to use a Docker image for pact-cli, the command needs to be different (mount volumes, etc.)
                    // npm install -g needs Node.js/npm installed on the Jenkins agent.
                    echo "Installing Pact CLI (Node.js version)..."
                    bat 'npm install -g @pact-foundation/pact-cli || exit /b 0'

                    echo "Publishing Pact files to PactFlow..."
                    // Ensure GIT_BRANCH is available, e.g., from a multibranch pipeline or manually defined.
                    // Adding --tag for the branch name is highly recommended for PactFlow's features.
                    bat """
                        pact publish .\\pacts\\*.json ^
                            --consumer-version="%BUILD_NUMBER%" ^
                            --tag="${env.BRANCH_NAME ?: 'main'}" ^
                            --broker-base-url="${PACTFLOW_BASE_URL}" ^
                            --broker-token="${PACTFLOW_TOKEN}"
                    """
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
            echo "✅ Pact contract published successfully!"
        }
        failure {
            echo "❌ Pact pipeline failed. Check logs."
        }
    }
}
