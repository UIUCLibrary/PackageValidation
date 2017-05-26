#!/usr/bin/env groovy
pipeline{
  agent any

  stages {
    stage("Cloning source") {
      agent any

      steps{
        echo "Cloning source"
        stash includes: "**", name: "source", useDefaultExcludes: false
      }
    }
    stage("Unit tests") {
            steps {
                parallel(
                        "Windows": {
                            node(label: 'Windows') {
                                deleteDir()
                                unstash "source"
                                bat "${env.TOX}  --skip-missing-interpreters"
                                junit 'reports/junit-*.xml'

                            }
                        },
                        "Linux": {
                            node(label: "!Windows") {
                                deleteDir()
                                unstash "source"
                                withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {
                                    sh """
                                    ${env.PYTHON3} -m venv .env
                                    . .env/bin/activate
                                    pip install -r requirements.txt
                                    tox  --skip-missing-interpreters -e py35 || true
                                    """
                                }
                                junit 'reports/junit-*.xml'
                            }
                        }
                )
            }
        }

    stage("Packaging"){
      agent any
      steps{
        node(label: "!Windows") {
            deleteDir()
            unstash "source"
            withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {
                sh """
                ${env.PYTHON3} -m venv .env
                . .env/bin/activate
                pip install -r requirements.txt
                ${env.TOX}  --skip-missing-interpreters -e py35
                python setup.py sdist
                """
                dir("dist") {
                  archiveArtifacts artifacts: "*.tar.gz", fingerprint: true
                }

            }
          }
      }
    }
  }
}
