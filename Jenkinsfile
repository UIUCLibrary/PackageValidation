#!/usr/bin/env groovy
@Library("ds-utils")
import org.ds.*


def PKG_NAME = "unknown"
def PKG_VERSION = "unknown"
def DOC_ZIP_FILENAME = "doc.zip"
def junit_filename = "junit.xml"
def REPORT_DIR = ""
def VENV_ROOT = ""
def VENV_PYTHON = ""
def VENV_PIP = ""

pipeline {
    agent {
        label "Windows && Python3"
    }
    options {
        disableConcurrentBuilds()  //each branch has 1 job running at a time
        timeout(60)  // Timeout after 60 minutes. This shouldn't take this long but it hangs for some reason
        checkoutToSubdirectory("source")
    }
    environment {
        mypy_args = "--junit-xml=mypy.xml"
        pytest_args = "--junitxml=reports/junit-{env:OS:UNKNOWN_OS}-{envname}.xml --junit-prefix={env:OS:UNKNOWN_OS}  --basetemp={envtmpdir}"
    }
    parameters {
        booleanParam(name: "FRESH_WORKSPACE", defaultValue: false, description: "Purge workspace before staring and checking out source")
        string(name: "PROJECT_NAME", defaultValue: "Package Qc", description: "Name given to the project")
        booleanParam(name: "UNIT_TESTS", defaultValue: true, description: "Run Automated Unit Tests")
        booleanParam(name: "ADDITIONAL_TESTS", defaultValue: true, description: "Run additional tests")
        booleanParam(name: "PACKAGE", defaultValue: true, description: "Create a Packages")
        booleanParam(name: "DEPLOY", defaultValue: false, description: "Deploy to SCCM")
        booleanParam(name: "UPDATE_DOCS", defaultValue: false, description: "Update the documentation")
        string(name: 'URL_SUBFOLDER', defaultValue: "package_qc", description: 'The directory that the docs should be saved under')


    }

    stages {
        stage("Configure") {
            stages{
                stage("Purge all existing data in workspace"){
                    when{
                        equals expected: true, actual: params.FRESH_WORKSPACE
                    }
                    steps{
                        deleteDir()
                        dir("source"){
                            checkout scm
                        }
                    }
                    post{
                        success{
                            bat "dir /s /B"
                        }
                    }
                }
                stage("Cleanup"){
                    steps {


                        dir("logs"){
                            deleteDir()
                            echo "Cleaned out logs directory"
                            bat "dir"
                        }

                        dir("build"){
                            deleteDir()
                            echo "Cleaned out build directory"
                            bat "dir"
                        }
                        dir("dist"){
                            deleteDir()
                            echo "Cleaned out dist directory"
                            bat "dir"
                        }

                        dir("reports"){
                            deleteDir()
                            echo "Cleaned out reports directory"
                            bat "dir"
                        }
                    }
                    post{
                        failure {
                            deleteDir()
                        }
                    }
                }
                stage("Installing required system level dependencies"){
                    steps{
                        lock("system_python"){
                            bat "${tool 'CPython-3.6'} -m pip install --upgrade pip --quiet"
                        }
                        tee("logs/pippackages_system_${NODE_NAME}.log") {
                            bat "${tool 'CPython-3.6'} -m pip list"
                        }
                    }
                    post{
                        always{
                            dir("logs"){
                                script{
                                    def log_files = findFiles glob: '**/pippackages_system_*.log'
                                    log_files.each { log_file ->
                                        echo "Found ${log_file}"
                                        archiveArtifacts artifacts: "${log_file}"
                                        bat "del ${log_file}"
                                    }
                                }
                            }
                        }
                        failure {
                            deleteDir()
                        }
                    }

                }
                stage("Creating virtualenv for building"){
                    steps {
                        bat "${tool 'CPython-3.6'} -m venv venv"

                        script {
                            try {
                                bat "call venv\\Scripts\\python.exe -m pip install -U pip"
                            }
                            catch (exc) {
                                bat "${tool 'CPython-3.6'} -m venv venv"
                                bat "call venv\\Scripts\\python.exe -m pip install -U pip --no-cache-dir"
                            }
                        }

                        bat "venv\\Scripts\\pip.exe install -r source\\requirements.txt -r --upgrade-strategy only-if-needed"
                        bat "venv\\Scripts\\pip.exe install devpi-client lxml pytest-cov --upgrade-strategy only-if-needed"



                        tee("logs/pippackages_venv_${NODE_NAME}.log") {
                            bat "venv\\Scripts\\pip.exe list"
                        }
                    }
                    post{
                        always{
                            dir("logs"){
                                script{
                                    def log_files = findFiles glob: '**/pippackages_venv_*.log'
                                    log_files.each { log_file ->
                                        echo "Found ${log_file}"
                                        archiveArtifacts artifacts: "${log_file}"
                                        bat "del ${log_file}"
                                    }
                                }
                            }
                        }
                        failure {
                            deleteDir()
                        }
                    }
                }
                stage("Setting variables used by the rest of the build"){
                    steps{

                        script {
                            // Set up the reports directory variable
                            REPORT_DIR = "${WORKSPACE}\\reports"
                            dir("source"){
                                PKG_NAME = bat(returnStdout: true, script: "@${tool 'CPython-3.6'}  setup.py --name").trim()
                                PKG_VERSION = bat(returnStdout: true, script: "@${tool 'CPython-3.6'} setup.py --version").trim()
                            }
                        }

                        script{
                            DOC_ZIP_FILENAME = "${PKG_NAME}-${PKG_VERSION}.doc.zip"
                            junit_filename = "junit-${env.NODE_NAME}-${env.GIT_COMMIT.substring(0,7)}-pytest.xml"
                        }




                        script{
                            VENV_ROOT = "${WORKSPACE}\\venv\\"

                            VENV_PYTHON = "${WORKSPACE}\\venv\\Scripts\\python.exe"
                            bat "${VENV_PYTHON} --version"

                            VENV_PIP = "${WORKSPACE}\\venv\\Scripts\\pip.exe"
                            bat "${VENV_PIP} --version"
                        }


                        bat "venv\\Scripts\\devpi use https://devpi.library.illinois.edu"
                        withCredentials([usernamePassword(credentialsId: 'DS_devpi', usernameVariable: 'DEVPI_USERNAME', passwordVariable: 'DEVPI_PASSWORD')]) {
                            bat "venv\\Scripts\\devpi.exe login ${DEVPI_USERNAME} --password ${DEVPI_PASSWORD}"
                        }
                        bat "dir"
                    }
                }
            }
            post{
                always{
                    echo """Name                            = ${PKG_NAME}
Version                         = ${PKG_VERSION}
Report Directory                = ${REPORT_DIR}
documentation zip file          = ${DOC_ZIP_FILENAME}
Python virtual environment path = ${VENV_ROOT}
VirtualEnv Python executable    = ${VENV_PYTHON}
VirtualEnv Pip executable       = ${VENV_PIP}
junit_filename                  = ${junit_filename}
"""

                }

            }

        }
        stage("Building") {
            stages{
                stage("Building Python Package"){
                    steps {
                        tee("logs/build.log") {
                            dir("source"){
                                bat "${WORKSPACE}\\venv\\Scripts\\python.exe setup.py build -b ${WORKSPACE}\\build"
                            }

                        }
                    }
                    post{
                        always{
                            script{
                                def log_files = findFiles glob: '**/*.log'
                                log_files.each { log_file ->
                                    echo "Found ${log_file}"
                                    archiveArtifacts artifacts: "${log_file}"
                                    warnings canRunOnFailed: true, parserConfigurations: [[parserName: 'MSBuild', pattern: "${log_file}"]]
                                    bat "del ${log_file}"
                                }
                            }
                        }
                    }
                }
                stage("Building Sphinx Documentation"){
                    when {
                        equals expected: true, actual: params.BUILD_DOCS
                    }
                    steps {
                        dir("build/docs/html"){
                            deleteDir()
                            echo "Cleaned out build/docs/html dirctory"

                        }
                        script{
                            // Add a line to config file so auto docs look in the build folder
                            def sphinx_config_file = 'source/docs/source/conf.py'
                            def extra_line = "sys.path.insert(0, os.path.abspath('${WORKSPACE}/build/lib'))"
                            def readContent = readFile "${sphinx_config_file}"
                            echo "Adding \"${extra_line}\" to ${sphinx_config_file}."
                            writeFile file: "${sphinx_config_file}", text: readContent+"\r\n${extra_line}\r\n"


                        }
                        echo "Building docs on ${env.NODE_NAME}"
                        tee("logs/build_sphinx.log") {
                            dir("build/lib"){
                                bat "${WORKSPACE}\\venv\\Scripts\\sphinx-build.exe -b html ${WORKSPACE}\\source\\docs\\source ${WORKSPACE}\\build\\docs\\html -d ${WORKSPACE}\\build\\docs\\doctrees"
                            }
                        }
                    }
                    post{
                        always {
                            dir("logs"){
                                script{
                                    def log_files = findFiles glob: '**/*.log'
                                    log_files.each { log_file ->
                                        echo "Found ${log_file}"
                                        archiveArtifacts artifacts: "${log_file}"
                                        bat "del ${log_file}"
                                    }
                                }
                            }
                        }
                        success{
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            dir("${WORKSPACE}/dist"){
                                zip archive: true, dir: "${WORKSPACE}/build/docs/html", glob: '', zipFile: "${DOC_ZIP_FILENAME}"
                            }
                        }
                    }

                }
            }
        }
//         stage("Cloning source") {
//             agent any

//             steps {
//                 echo "Cloning source"
//                 stash includes: "**", name: "Source", useDefaultExcludes: false
// //                stash includes: 'deployment.yml', name: "Deployment"
//             }
//         }
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
                                runner.p ost = {
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
                                runner.windows = true
                                runner.stash = "Source"
                                runner.label = "Windows"
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
                                runner.windows = true
                                runner.stash = "Source"
                                runner.label = "Windows"
                                runner.post = {
                                    junit 'mypy.xml'
                                }
                                runner.run()

                            }
                        }
                )
            }

        }

        stage("Packaging") {
            agent any
            when {
                expression { params.PACKAGE == true || params.DEPLOY == true }
            }
            steps {
                parallel(
                        "Source Package": {
                            createSourceRelease(env.PYTHON3, "Source")
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

        stage("Deploy - Staging") {
            agent any
            when {
                expression { params.DEPLOY == true }
            }
            steps {
                deployStash("msi", "${env.SCCM_STAGING_FOLDER}/${params.PROJECT_NAME}/")
                input("Deploy to production?")
            }
        }

        stage("Deploy - SCCM upload") {
            agent any
            when {
                expression { params.DEPLOY == true}
            }
            steps {
                deployStash("msi", "${env.SCCM_UPLOAD_FOLDER}")
            }
            post {
                success {
                    script{
                        unstash "Source"
                        def  deployment_request = requestDeploy this, "deployment.yml"
                        echo deployment_request
                        writeFile file: "deployment_request.txt", text: deployment_request
                        archiveArtifacts artifacts: "deployment_request.txt"
                    }

                }
            }
        }
        stage("Update online documentation") {
            agent any
            when {
                expression { params.UPDATE_DOCS == true}
            }

            steps {
                updateOnlineDocs url_subdomain: params.URL_SUBFOLDER, stash_name: "HTML Documentation"

            }
        }
    }
}
