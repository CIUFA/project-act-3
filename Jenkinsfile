pipeline {
    agent any

    tools {
        python 'Python313' // must match the name in Jenkins Global Tool Configuration
    }

    environment {
        VENV_DIR = "${WORKSPACE}\\venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/CIUFA/project-act-3.git'
            }
        }

        stage('Setup Python') {
            steps {
                bat """
                python -m venv "%VENV_DIR%"
                call "%VENV_DIR%\\Scripts\\activate"
                python -m pip install --upgrade pip
                python -m pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                call "%VENV_DIR%\\Scripts\\activate"
                set PYTHONPATH=%CD%
                pytest --junitxml=results.xml
                """
            }
        }
    }

    post {
        always {
            junit 'results.xml'
        }
        success {
            echo '✅ All tests passed!'
        }
        failure {
            echo '❌ Tests failed. Check logs.'
        }
    }
}