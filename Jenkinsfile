pipeline {
    agent any

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
                "C:\\Program Files\\Python313\\python.exe" -m venv "%VENV_DIR%"
                "%VENV_DIR%\\Scripts\\python.exe" -m pip install --upgrade pip
                "%VENV_DIR%\\Scripts\\python.exe" -m pip install -r "%WORKSPACE%\\requirements.txt"
                """
            }
        }

        stage('Run Tests') {
            steps {
                bat """
                "%VENV_DIR%\\Scripts\\python.exe" -m pytest --junitxml="%WORKSPACE%\\results.xml"
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