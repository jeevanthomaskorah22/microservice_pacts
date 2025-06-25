// Jenkinsfile (or Jenkinsfile_Consumer) for microservice_pacts repository

pipeline {
    agent any // Or a specific agent with necessary tools (e.g., agent { label 'my-linux-agent' })

    environment {
        PACTFLOW_BASE_URL = 'https://nitc-0bb42495.pactflow.io'
        // Get the PactFlow token from Jenkins credentials. Ensure 'PACTFLOW_AUTH_TOKEN' ID matches your Jenkins Secret Text credential.
        PACTFLOW_TOKEN = credentials('PACTFLOW_TOKEN')
        // GIT_COMMIT and GIT_BRANCH are automatically populated by Jenkins for SCM-triggered builds.
        // The ?: 'HEAD' and ?: 'main' provide fallbacks if running locally or not from a Git checkout.
        GIT_COMMIT = "${env.GIT_COMMIT ?: 'HEAD'}"
        GIT_BRANCH = "${env.BRANCH_NAME ?: 'main'}"
    }

    stages {
        stage('Checkout Source') {
            steps {
                script {
                    // Jenkins automatically checks out the repository where the Jenkinsfile resides.
                    // If your Jenkins job is configured to clone your forked microservice_pacts repo,
                    // this step is implicitly handled. No explicit `git clone` needed here.
                    echo "Workspace: ${WORKSPACE}"
                    // Navigate into the tests directory where your Pact tests are located.
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
                    // Ensure pip is up to date and install virtualenv
                    sh 'python3 -m pip install --upgrade pip'
                    sh 'pip install virtualenv'
                    // Create a virtual environment
                    sh 'python3 -m venv venv'
                    // Activate virtual environment and install Python pact dependencies
                    sh '. venv/bin/activate && pip install pytest pact-python requests'
                    echo "Python dependencies installed."
                }
            }
        }

        stage('Install Node.js Dependencies') {
            steps {
                dir('tests') {
                    echo "Installing Node.js dependencies..."
                    // This assumes you have a package.json file in the 'tests' directory
                    sh 'npm install'
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
                    sh '. venv/bin/activate && pytest order_product.py payment-order.py --pact-dir=./pacts'
                    echo "Python Pact files generated in ${pwd()}/pacts"
                }
            }
        }

        stage('Run Node.js Consumer Tests') {
            steps {
                dir('tests') {
                    echo "Running Node.js consumer tests to generate pacts..."
                    // Run Node.js consumer tests to generate pact files
                    // This assumes your package.json has a "test" script that runs your consumer tests (e.g., "mocha ...").
                    sh 'npm test'
                    echo "Node.js Pact files generated in ${pwd()}/pacts"
                }
            }
        }

        stage('Publish Pacts to PactFlow') {
            steps {
                dir('tests') {
                    echo "Publishing Pact files to PactFlow..."
                    // Install pact-cli if not already installed on the agent.
                    // It's highly recommended to have pact-cli pre-installed on your Jenkins agent.
                    // The '|| true' allows the step to continue even if npm install -g fails (e.g., due to permissions, or if already installed).
                    sh 'npm install -g @pact-foundation/pact-cli || true'

                    // Publish all pact files found in the 'pacts' directory.
                    // --consumer-version: Use the Git commit hash for unique versioning.
                    // --tag: Use the Git branch name (e.g., 'main', 'develop'). This is crucial for wiring up "can-i-deploy" later.
                    sh """
                        pact publish \\
                            ./pacts/*.json \\
                            --consumer-version="${GIT_COMMIT}" \\
                            --tag="${GIT_BRANCH}" \\
                            --broker-base-url="${PACTFLOW_BASE_URL}" \\
                            --broker-token="${PACTFLOW_TOKEN}"
                    """
                    echo "Pact files published to PactFlow successfully."
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up workspace..."
            cleanWs() // Clean up the workspace after the build, regardless of success or failure.
            echo "Workspace cleaned."
        }
        failure {
            echo "Pipeline failed! Check logs for details."
            // You can add notifications here, e.g., email or Slack
        }
        success {
            echo "Pipeline completed successfully!"
        }
    }
}