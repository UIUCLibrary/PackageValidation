#!/usr/bin/env groovy
@Library("ds-utils")
import org.ds.*

pipeline {
    agent any
    environment {
        mypy_args = "--junit-xml=mypy.xml"
        pytest_args = "--junitxml=reports/junit-{env:OS:UNKNOWN_OS}-{envname}.xml --junit-prefix={env:OS:UNKNOWN_OS}  --basetemp={envtmpdir}"
    }
    parameters {
        string(name: "PROJECT_NAME", defaultValue: "Package Qc", description: "Name given to the project")
        booleanParam(name: "UNIT_TESTS", defaultValue: true, description: "Run Automated Unit Tests")
        booleanParam(name: "PACKAGE", defaultValue: true, description: "Create a Packages")
        booleanParam(name: "DEPLOY", defaultValue: false, description: "Deploy to SCCM")
        booleanParam(name: "BUILD_DOCS", defaultValue: true, description: "Build documentation")
        booleanParam(name: "UPDATE_DOCS", defaultValue: false, description: "Update the documentation")
        string(name: 'URL_SUBFOLDER', defaultValue: "package_qc", description: 'The directory that the docs should be saved under')


    }

    stages {
        stage("Cloning source") {
            agent any

            steps {
                echo "Cloning source"
                stash includes: "**", name: "Source", useDefaultExcludes: false
                stash includes: 'deployment.yml', name: "Deployment"
            }
        }
        stage("Unit tests") {
            when {
                expression { params.UNIT_TESTS == true }
            }
            steps {
                parallel(
                        "Windows": {
                            script {
                                def runner = new Tox(this)
                                runner.env = "pytest"
                                runner.windows = true
                                runner.stash = "Source"
                                runner.label = "Windows"
                                runner.post = {
                                    junit 'reports/junit-*.xml'
                                }
                                runner.run()
                            }
                        },
                        "Linux": {
                            script {
                                def runner = new Tox(this)
                                runner.env = "pytest"
                                runner.windows = false
                                runner.stash = "Source"
                                runner.label = "!Windows"
                                runner.post = {
                                    junit 'reports/junit-*.xml'
                                }
                                runner.run()
                            }
                        }
//                        "Windows": {
//                            node(label: 'Windows') {
//                                deleteDir()
//                                unstash "source"
//                                bat "${env.TOX}  --skip-missing-interpreters"
//                                junit 'reports/junit-*.xml'
//
//                            }
//                        },
//                        "Linux": {
//                            node(label: "!Windows") {
//                                deleteDir()
//                                unstash "source"
//                                withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {
//                                    sh """
//                            ${env.PYTHON3} -m venv .env
//                            . .env/bin/activate
//                            pip install -r requirements.txt
//                            tox  --skip-missing-interpreters -e py35 || true
//                            """
//                                }
//                                junit 'reports/junit-*.xml'
//                            }
//                        }
                )
            }
        }
        stage("Additional tests") {
            when {
                expression { params.ADDITIONAL_TESTS == true }
            }

            steps {
                parallel(
                        "Documentation": {
                            script {
                                def runner = new Tox(this)
                                runner.env = "docs"
                                runner.windows = false
                                runner.stash = "Source"
                                runner.label = "!Windows"
                                runner.post = {
                                    dir('.tox/dist/html/') {
                                        stash includes: '**', name: "HTML Documentation", useDefaultExcludes: false
                                    }
                                }
                                runner.run()

                            }
                        },
                        "MyPy": {
                            script {
                                def runner = new Tox(this)
                                runner.env = "mypy"
                                runner.windows = false
                                runner.stash = "Source"
                                runner.label = "!Windows"
                                runner.post = {
                                    junit 'mypy.xml'
                                }
                                runner.run()

                            }
                        }
                )
            }

        }
//        stage("Documentation") {
//            agent any
//            when {
//                expression { params.BUILD_DOCS == true }
//            }
//
//            steps {
//                deleteDir()
//                unstash "Source"
//                withEnv(['PYTHON=${env.PYTHON3}']) {
//                    dir('docs') {
//                        sh 'make html SPHINXBUILD=$SPHINXBUILD'
//                    }
//                    stash includes: '**', name: "Documentation source", useDefaultExcludes: false
//                }
//            }
//            post {
//                success {
//                    sh 'tar -czvf sphinx_html_docs.tar.gz -C docs/build/html .'
//                    archiveArtifacts artifacts: 'sphinx_html_docs.tar.gz'
//                }
//            }
//        }

        stage("Packaging") {
            agent any
            when {
                expression { params.PACKAGE == true }
            }
            steps {
                parallel(
                        "Source Package": {
                            node(label: "!Windows") {
                                deleteDir()
                                unstash "Source"
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
                        "Python Wheel:": {
                            node(label: "Windows") {
                                deleteDir()
                                unstash "Source"
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
                        "Python CX_Freeze Windows": {
                            node(label: "Windows") {
                                deleteDir()
                                unstash "Source"

                                withEnv(["PATH=${env.PYTHON3}/..:${env.PATH}"]) {

                                    // Build the exe so that pytest can be run
                                    bat "${env.PYTHON3} cx_setup.py build --build-exe build/tmp"
                                    script {
                                        echo("Checking for VCRUNTIME140.dll")
                                        if (fileExists('build/tmp/VCRUNTIME140.dll')) {
                                            echo("Found for VCRUNTIME140.dll")
                                        } else {
                                            fail("Missing VCRUNTIME140.dll")
                                        }
                                    }

                                    // run pytest on exe
                                    bat """
                  build\\tmp\\qcpkg.exe --pytest --verbose  --junitxml=reports/junit-frozen.xml --junit-prefix=frozen
                  if not %errorlevel%==0 (
                    echo errorlevel=%errorlevel%
                    exit /b %errorlevel%
                  )
                """
                                    junit 'reports/junit-*.xml'

                                    // Package the exe into MSI
                                    bat "${env.PYTHON3} cx_setup.py bdist_msi --add-to-path=true"
                                    dir("dist") {
                                        archiveArtifacts artifacts: "*.msi", fingerprint: true
                                        stash includes: "*.msi", name: "msi"
                                    }

                                    // junit 'reports/junit-*.xml'

                                    // validate MSI contents

                                }
                            }
                            node(label: "Windows") {
                                deleteDir()
                                git url: 'https://github.com/UIUCLibrary/ValidateMSI.git'
                                unstash "msi"
                                // validate_msi.py

                                bat """
                ${env.PYTHON3} -m venv .env
                call .env/Scripts/activate.bat
                pip install -r requirements.txt
                python setup.py install

                echo Validating msi file(s)
                FOR %%A IN (*.msi) DO (
                  python validate_msi.py %%A frozen.yml
                  if not %errorlevel%==0 (
                    echo errorlevel=%errorlevel%
                    exit /b %errorlevel%
                  )
                )
              """
                                archiveArtifacts artifacts: "*.msi", fingerprint: true


                            }
                        }
                )
            }
        }
        stage("Update online documentation") {
            agent any
            when {
                expression { params.UPDATE_DOCS == true && params.BUILD_DOCS == true }
            }

            steps {
                deleteDir()
                script {
                    echo "Updating online documentation"
                    unstash "Documentation source"
                    try {
                        sh("rsync -rv -e \"ssh -i ${env.DCC_DOCS_KEY}\" docs/build/html/ ${env.DCC_DOCS_SERVER}/${params.URL_SUBFOLDER}/ --delete")
                    } catch (error) {
                        echo "Error with uploading docs"
                        throw error
                    }

                }
            }
        }
        stage("Deploy - Staging") {
            agent any
            when {
                expression { params.DEPLOY == true && params.PACKAGE == true }
            }
            steps {
                deleteDir()
                unstash "msi"
                sh "rsync -rv ./ \"${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/\""
                input("Deploy to production?")
            }
        }

        stage("Deploy - SCCM upload") {
            agent any
            when {
                expression { params.DEPLOY == true && params.PACKAGE == true }
            }
            steps {
                deleteDir()
                unstash "msi"
                sh "rsync -rv ./ ${env.SCCM_UPLOAD_FOLDER}/"
            }
            post {
                success {
                    git url: 'https://github.com/UIUCLibrary/sccm_deploy_message_generator.git'
                    unstash "Deployment"
                    sh """${env.PYTHON3} -m venv .env
                      . .env/bin/activate
                      pip install --upgrade pip
                      pip install setuptools --upgrade
                      python setup.py install
                      deploymessage deployment.yml --save=deployment_request.txt
                  """
                    archiveArtifacts artifacts: "deployment_request.txt"
                    echo(readFile('deployment_request.txt'))
                }
            }
        }
    }
}
