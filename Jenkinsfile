pipeline {
    agent any

    environment {
        PACT_BROKER_URL = 'https://nitc-0bb42495.pactflow.io'
        PACT_CONSUMER = 'OrderService'
        PACT_DIR = 'tests\\pacts'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/jeevanthomaskorah22/microservice_pacts', branch: 'main'
            }
        }

        stage('Setup Python Env') {
            steps {
                dir('tests') {
                    bat 'py -m venv venv'
                    bat 'venv\\Scripts\\activate.bat && pip install --upgrade pip'
                    bat 'venv\\Scripts\\activate.bat && pip install pytest pact-python requests'
                }
            }
        }

        stage('Run Pact Tests') {
            steps {
                dir('tests') {
                    bat 'venv\\Scripts\\activate.bat && pytest order_product.py'
                }
            }
        }

        stage('Publish Pacts') {
            steps {
                dir('tests') {
                    withCredentials([string(credentialsId: 'PACTFLOW_TOKEN', variable: 'PACT_TOKEN')]) {
                        bat 'npm install -g @pact-foundation/pact-cli || exit /b 0'
                        script {
                            def commitHash = bat(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                            bat """
                            pact publish pacts\\*.json ^
                              --consumer-version="${commitHash}" ^
                              --tag="main" ^
                              --broker-base-url="${PACT_BROKER_URL}" ^
                              --broker-token="${PACT_TOKEN}"
                            """
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
