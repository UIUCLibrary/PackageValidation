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
        parallel(
          "Source Package": {
            node(label: "!Windows") {
              deleteDir()
              unstash "source"
              withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {
                sh """
                ${env.PYTHON3} -m venv .env
                . .env/bin/activate
                pip install -r requirements.txt
                python setup.py sdist
                """
                dir("dist") {
                  archiveArtifacts artifacts: "*.tar.gz", fingerprint: true
                }
                }
            }
          },
          "Python Wheel: (Universal)" :{
            node(label: "Windows") {
              deleteDir()
              unstash "source"
              withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {
                bat """
                  ${env.PYTHON3} -m venv .env
                  echo "Building wheel"
                  call .env/Scripts/activate.bat
                  python setup.py bdist_wheel --universal
                """
                dir("dist") {
                  archiveArtifacts artifacts: "*.whl", fingerprint: true
                }
              }
            }
          }
        )
      }
    }
  }
}
