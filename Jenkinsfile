pipeline {
    agent any

    environment {
        PACTFLOW_BASE_URL = 'https://nitc-0bb42495.pactflow.io'
        PACTFLOW_TOKEN = credentials('PACTFLOW_TOKEN')
        PATH = "C:\\Ruby32-x64\\bin;%PATH%" // ✅ Add Ruby executables to PATH
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
                    bat 'py -m venv venv'
                    bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip'
                    bat 'venv\\Scripts\\activate.bat && pip install pytest pact-python requests'
                }
            }
        }

        stage('Run Consumer Pact Tests') {
            steps {
                dir('tests') {
                    bat 'venv\\Scripts\\activate.bat && pytest order_product.py --capture=tee-sys'
                }
            }
        }

        stage('Publish Pact to PactFlow') {
            steps {
                dir('tests') {
                    bat 'npm install -g @pact-foundation/pact-cli || exit /b 0'
                    bat """
                        pact publish pacts\\*.json ^
                          --consumer-version="%BUILD_NUMBER%" ^
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
