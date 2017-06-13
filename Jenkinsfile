#!/usr/bin/env groovy
pipeline{
  agent any
  parameters {
  booleanParam(name: "UPDATE_DOCS", defaultValue: false, description: "Update the documentation")
  booleanParam(name: "PACKAGE", defaultValue: true, description: "Create a Packages")
}

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
      stage("Documentation") {
          agent any

          steps {
              deleteDir()
              unstash "source"
              withEnv(['PYTHON=${env.PYTHON3}']) {
                  dir('docs') {
                      sh 'make html SPHINXBUILD=$SPHINXBUILD'
                  }
                  stash includes: '**', name: "Documentation source", useDefaultExcludes: false
              }
          }
          post {
              success {
                  sh 'tar -czvf sphinx_html_docs.tar.gz -C docs/build/html .'
                  archiveArtifacts artifacts: 'sphinx_html_docs.tar.gz'
              }
          }
      }

    stage("Packaging"){
      agent any
      when{
        expression{params.PACKAGE == true}
      }
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
          "Python Wheel:" :{
            node(label: "Windows") {
              deleteDir()
              unstash "source"
              withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {
                bat """
                  ${env.PYTHON3} -m venv .env
                  call .env/Scripts/activate.bat
                  pip install -r requirements.txt
                  python setup.py bdist_wheel
                """
                dir("dist") {
                  archiveArtifacts artifacts: "*.whl", fingerprint: true
                }
              }
            }
          },
          "Python CX_Freeze Windows" :{
            node(label: "Windows") {
              deleteDir()
              unstash "source"

              withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {
                bat """

                  ${env.PYTHON3} cx_setup.py build --build-exe build/tmp
                  build\\tmp\\qcpkg.exe --pytest --verbose  --junitxml=reports/junit-frozen.xml --junit-prefix=frozen
                  if %errorlevel%==0 (
                    ${env.PYTHON3} cx_setup.py bdist_msi --add-to-path=true
                    ) else (
                      echo errorlevel=%errorlevel%
                      exit /b %errorlevel%
                      )
                """
                junit 'reports/junit-*.xml'
                dir("dist") {
                  archiveArtifacts artifacts: "*.msi", fingerprint: true
                }
              }
            }
          }
        )
      }
    }
    stage("Update online documentation") {
      agent any
      when{
        expression{params.UPDATE_DOCS == true}
      }

      steps {
          deleteDir()
          script {
              echo "Updating online documentation"
              unstash "Documentation source"
              try {
                sh("scp -r -i ${env.DCC_DOCS_KEY} docs/build/html/* ${env.DCC_DOCS_SERVER}/package_qc/")
              } catch(error) {
                echo "Error with uploading docs"
                throw error
              }

          }
      }
    }
  }
}
