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
                                bat "mkdir reports"
                                bat "${env.TOX}  --skip-missing-interpreters"
                                junit 'reports/junit-*.xml'

                            }
                        },
                        "Linux": {
                            node(label: "!Windows") {
                                deleteDir()
                                unstash "source"
                                withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {
                                    sh "mkdir reports"
                                    sh "${env.TOX}  --skip-missing-interpreters -e py35"
                                }
                                junit 'reports/junit-*.xml'
                            }
                        }
                )
            }
            post {
              always {
                junit 'reports/junit-*.xml'
              }
            }
        }

  }
}
