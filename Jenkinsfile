#!/usr/bin/env groovy
@Library("ds-utils")
import org.ds.*

@Library(["devpi", "PythonHelpers"]) _


def remove_from_devpi(devpiExecutable, pkgName, pkgVersion, devpiIndex, devpiUsername, devpiPassword){
    script {
            try {
                bat "${devpiExecutable} login ${devpiUsername} --password ${devpiPassword}"
                bat "${devpiExecutable} use ${devpiIndex}"
                bat "${devpiExecutable} remove -y ${pkgName}==${pkgVersion}"
            } catch (Exception ex) {
                echo "Failed to remove ${pkgName}==${pkgVersion} from ${devpiIndex}"
        }

    }
}

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
        PATH = "${tool 'CPython-3.6'};${tool 'CPython-3.7'};$PATH"
        PKG_NAME = pythonPackageName(toolName: "CPython-3.6")
        PKG_VERSION = pythonPackageVersion(toolName: "CPython-3.6")
        DOC_ZIP_FILENAME = "${env.PKG_NAME}-${env.PKG_VERSION}.doc.zip"
        DEVPI = credentials("DS_devpi")
        mypy_args = "--junit-xml=mypy.xml"
        pytest_args = "--junitxml=reports/junit-{env:OS:UNKNOWN_OS}-{envname}.xml --junit-prefix={env:OS:UNKNOWN_OS}  --basetemp={envtmpdir}"
    }
    parameters {
        booleanParam(name: "FRESH_WORKSPACE", defaultValue: false, description: "Purge workspace before staring and checking out source")
        booleanParam(name: "TEST_RUN_DOCTEST", defaultValue: true, description: "Test documentation")
        booleanParam(name: "TEST_RUN_PYTEST", defaultValue: true, description: "Run unit tests with PyTest")
        booleanParam(name: "TEST_RUN_MYPY", defaultValue: true, description: "Run MyPy static analysis")
        booleanParam(name: "TEST_RUN_FLAKE8", defaultValue: true, description: "Run Flake8 static analysis")
        booleanParam(name: "TEST_RUN_TOX", defaultValue: true, description: "Run Tox Tests")
        booleanParam(name: "PACKAGE_PYTHON_FORMATS", defaultValue: true, description: "Create native Python packages")
        booleanParam(name: "PACKAGE_CX_FREEZE", defaultValue: false, description: "Create standalone install with CX_Freeze")
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: true, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
        booleanParam(name: "UPDATE_DOCS", defaultValue: false, description: "Update the documentation")
        string(name: 'URL_SUBFOLDER', defaultValue: "package_qc", description: 'The directory that the docs should be saved under')
    }
    triggers {
        cron('@daily')
    }
    stages {
        stage("Configure") {
            stages{
                stage("Purge all existing data in workspace"){
                    when{
                        anyOf{
                            equals expected: true, actual: params.FRESH_WORKSPACE
                            triggeredBy "TimerTriggerCause"
                        }
                    }
                    steps{
                        deleteDir()
                        dir("source"){
                            checkout scm
                        }
                    }
                }
                stage("Install Python system dependencies"){
                    steps{

                        lock("system_python_${env.NODE_NAME}"){
                            bat "python -m pip install pip --upgrade --quiet"
                            bat "(if not exist logs mkdir logs) && python -m pip list > logs/pippackages_system_${env.NODE_NAME}.log"
                        }
                    }
                    post{
                        always{
                            archiveArtifacts artifacts: "logs/pippackages_system_${env.NODE_NAME}.log"
                        }
                        failure {
                            deleteDir()
                        }
                        cleanup{
                            cleanWs(patterns: [[pattern: "logs/pippackages_system_*.log", type: 'INCLUDE']])
                        }
                    }
                }
                stage("Creating virtualenv for building"){
                    steps {
                        bat "${tool 'CPython-3.6'}\\python -m venv venv"
                        script {
                            try {
//                                bat "call venv\\Scripts\\python.exe -m pip install -U pip"
                                bat "venv\\Scripts\\python.exe -m pip install -U pip>=18.1"
                            }
                            catch (exc) {
                                bat "${tool 'CPython-3.6'}\\python -m venv venv"
                                bat "venv\\Scripts\\python.exe -m pip install -U pip>=18.1 --no-cache-dir"
                            }
                        }

                        bat "venv\\Scripts\\pip.exe install -r source\\requirements.txt --upgrade-strategy only-if-needed"
                        bat "venv\\Scripts\\pip.exe install lxml pytest-cov mypy coverage flake8 tox --upgrade-strategy only-if-needed"
                        bat "venv\\Scripts\\pip.exe list > ${WORKSPACE}/logs/pippackages_venv_${NODE_NAME}.log"
                    }
                    post{
                        success{
                            archiveArtifacts artifacts: "logs/pippackages_venv_${NODE_NAME}.log"
                        }
                        failure {
                            deleteDir()
                        }
                        cleanup{
                            cleanWs(patterns: [[pattern: 'logs/pippackages_venv_*.log', type: 'INCLUDE']])
                        }
                    }
                }
            }
            post{
                success{
                    echo "Configured ${env.PKG_NAME}, version ${env.PKG_VERSION}, for testing."
                }

            }

        }
        stage("Building") {
            stages{
                stage("Building Python Package"){
                    steps {
                        dir("source"){
                            powershell "& ${WORKSPACE}\\venv\\Scripts\\python.exe setup.py build -b ${WORKSPACE}\\build | tee ${WORKSPACE}\\logs\\build.log"
                        }
                    }
                    post{
                        always{
                            archiveArtifacts artifacts: "logs/build.log"
                            recordIssues(tools: [
                                        pyLint(name: 'Setuptools Build: PyLint', pattern: 'logs/build.log'),
                                        msBuild(name: 'Setuptools Build: MSBuild', pattern: 'logs/build.log')
                                    ]
                                )
//                            warnings canRunOnFailed: true, parserConfigurations: [[parserName: 'Pep8', pattern: 'logs/build.log']]
                        }
                        cleanup{
                            cleanWs(patterns: [[pattern: 'logs/build.log', type: 'INCLUDE']])
                        }
                    }
                }
                stage("Building Sphinx Documentation"){
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
                        dir("source"){
                            powershell "& ${WORKSPACE}\\venv\\Scripts\\python.exe setup.py build_sphinx --build-dir ${WORKSPACE}\\build\\docs | tee ${WORKSPACE}\\logs\\build_sphinx.log"
                        }
                    }
                    post{
                        always {
                            recordIssues(tools: [sphinxBuild(name: 'Sphinx Documentation Build', pattern: 'logs/build_sphinx.log', id: 'sphinx_build')])
//                            warnings canRunOnFailed: true, parserConfigurations: [[parserName: 'Pep8', pattern: 'logs/build_sphinx.log']]
                            archiveArtifacts artifacts: 'logs/build_sphinx.log'
                        }
                        success{
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            zip archive: true, dir: "${WORKSPACE}/build/docs/html", glob: '', zipFile: "dist/${DOC_ZIP_FILENAME}"
                            stash includes: "dist/${DOC_ZIP_FILENAME},build/docs/html/**", name: 'DOCS_ARCHIVE'

                        }
                        cleanup{
                            cleanWs(patterns: [[pattern: 'logs/build_sphinx.log', type: 'INCLUDE']])
                            cleanWs(patterns: [[pattern: "dist/${DOC_ZIP_FILENAME}", type: 'INCLUDE']])
                        }
                    }
                }
            }
        }
        stage("Tests") {
            parallel {
                stage("PyTest"){
                    when {
                        equals expected: true, actual: params.TEST_RUN_PYTEST
                    }
                    steps{
                        dir("source"){
                            bat "${WORKSPACE}\\venv\\Scripts\\coverage run --parallel-mode --source=dcc_qc -m pytest --junitxml=${WORKSPACE}/reports/pytest/junit-${env.NODE_NAME}-pytest.xml --junit-prefix=${env.NODE_NAME}-pytest" //  --basetemp={envtmpdir}"
                        }

                    }
                    post {
                        always{
                            junit "reports/pytest/junit-*.xml"
                        }
                        cleanup{
                            cleanWs(patterns: [[pattern: 'reports/pytest/junit-*.xml', type: 'INCLUDE']])
                        }
                    }
                }
                stage("Documentation"){
                    when{
                        equals expected: true, actual: params.TEST_RUN_DOCTEST
                    }
                    steps{
                        dir("source"){
                            bat "${WORKSPACE}\\venv\\Scripts\\sphinx-build.exe -b doctest docs\\source ${WORKSPACE}\\build\\docs -d ${WORKSPACE}\\build\\docs\\doctrees -v"
                        }
                    }

                }
                stage("MyPy"){
                    when{
                        equals expected: true, actual: params.TEST_RUN_MYPY
                    }
                    steps{
                        dir("source"){
                            powershell returnStatus: true, script: "& ${WORKSPACE}\\venv\\Scripts\\mypy.exe -p dcc_qc | tee ${WORKSPACE}\\logs\\mypy.log"
                            powershell returnStatus: true, script: "& ${WORKSPACE}\\venv\\Scripts\\mypy.exe -p dcc_qc --html-report ${WORKSPACE}\\reports\\mypy\\html"
                        }
                    }
                    post{
                        always {
                            archiveArtifacts "logs\\mypy.log"
                            recordIssues(tools: [myPy(name: 'MyPy', pattern: 'logs/mypy.log')])
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy/html', reportFiles: 'index.html', reportName: 'MyPy', reportTitles: ''])
                        }
                        cleanup{
                            cleanWs(patterns: [[pattern: 'logs/mypy.log', type: 'INCLUDE']])
                        }
                    }
                }
                stage("Run Flake8 Static Analysis") {
                    when {
                        equals expected: true, actual: params.TEST_RUN_FLAKE8
                    }
                    steps{
                        dir("logs"){
                            bat "dir"
                        }
                        script{
                            dir("source"){
                                bat returnStatus: true, script: "${WORKSPACE}\\venv\\Scripts\\flake8.exe dcc_qc --format=pylint --tee --output-file=${WORKSPACE}\\logs\\flake8.log"
                            }
                        }
                    }
                    post {
                        always {
                            recordIssues(tools: [flake8(name: 'Flake8', pattern: 'logs/flake8.log')])
                            archiveArtifacts "logs/flake8.log"
                        }
                        cleanup{
                            cleanWs(patterns: [[pattern: 'logs/flake8.log', type: 'INCLUDE']])
                        }
                    }
                }
            }
            post{
                always{
                    dir("source"){
                        bat "${WORKSPACE}\\venv\\Scripts\\coverage.exe combine"
                        bat "${WORKSPACE}\\venv\\Scripts\\coverage.exe xml -o ${WORKSPACE}\\reports\\coverage.xml"
                        bat "${WORKSPACE}\\venv\\Scripts\\coverage.exe html -d ${WORKSPACE}\\reports\\coverage"
                    }
                    publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: "reports/coverage", reportFiles: 'index.html', reportName: 'Coverage', reportTitles: ''])
                    publishCoverage adapters: [
                                    coberturaAdapter('reports/coverage.xml')
                                    ],
                                sourceFileResolver: sourceFiles('STORE_ALL_BUILD')

                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/coverage', reportFiles: 'index.html', reportName: 'Coverage', reportTitles: ''])
                }
                cleanup{
                    cleanWs(patterns:
                        [
                            [pattern: 'reports/coverage.xml', type: 'INCLUDE'],
                            [pattern: 'reports/coverage', type: 'INCLUDE'],
                            [pattern: 'source/.coverage', type: 'INCLUDE']
                        ]
                    )

                }
            }
        }
        stage("Packaging") {
            failFast true
            parallel {
                stage("Source and Wheel formats"){
                    when {
                        equals expected: true, actual: params.PACKAGE_PYTHON_FORMATS
                    }
                    stages{

                        stage("Packaging sdist and wheel"){

                            steps{
                                dir("source"){
                                    bat script: "${WORKSPACE}\\venv\\scripts\\python.exe setup.py sdist -d ${WORKSPACE}\\dist --format=zip bdist_wheel -d ${WORKSPACE}\\dist"
                                }
                            }
                            post {
                                success {
                                    archiveArtifacts artifacts: "dist/*.whl,dist/*.tar.gz,dist/*.zip", fingerprint: true
                                    stash includes: "dist/*.whl,dist/*.tar.gz,dist/*.zip", name: 'PYTHON_PACKAGES'
                                }
                                cleanup{
                                    cleanWs deleteDirs: true, patterns: [[pattern: 'dist/*.whl,dist/*.tar.gz,dist/*.zip', type: 'INCLUDE']]
                                }
                            }
                        }
                    }
                }

                stage("Windows CX_Freeze MSI"){
                    agent{
                        node {
                            label "Windows"
                        }
                    }
                    when {
                        equals expected: true, actual: params.PACKAGE_CX_FREEZE
                    }
                    options {
                        skipDefaultCheckout true
                    }
                    steps{
                        bat "dir"
                        deleteDir()
                        bat "dir"
                        checkout scm
                        bat "dir /s / B"
                        bat "${tool 'CPython-3.6'}\\python -m venv venv"
                        bat "venv\\Scripts\\python.exe -m pip install -U pip>=18.1"
                        bat "venv\\Scripts\\pip.exe install -U setuptools"
                        bat "venv\\Scripts\\pip.exe install -r requirements.txt"
                        bat "venv\\Scripts\\pip.exe install appdirs cx_Freeze"

                        bat "venv\\Scripts\\python.exe cx_setup.py bdist_msi --add-to-path=true -k --bdist-dir build/msi"                        // bat "make freeze"
                    }
                    post{
                        success{
                            dir("dist") {
                                stash includes: "*.msi", name: "msi"
                                archiveArtifacts artifacts: "*.msi", fingerprint: true
                            }
                        }
                        cleanup{
                            bat "dir"
                            deleteDir()
                            bat "dir"
                        }
                    }
                }
            }
        }

        stage("Deploying to DevPi") {
            when {
                allOf{
                    anyOf{
                        equals expected: true, actual: params.DEPLOY_DEVPI
                        triggeredBy "TimerTriggerCause"
                    }
                    anyOf {
                        equals expected: "master", actual: env.BRANCH_NAME
                        equals expected: "dev", actual: env.BRANCH_NAME
                    }
                }
            }
            environment{
                PATH = "${WORKSPACE}\\venv\\Scripts;${tool 'CPython-3.6'};${tool 'CPython-3.6'}\\Scripts;${PATH}"
            }
            stages{
                stage("Upload to Devpi staging") {

                    steps {
                        bat "${WORKSPACE}\\venv\\Scripts\\pip install devpi-client"
                        unstash 'DOCS_ARCHIVE'
                        unstash 'PYTHON_PACKAGES'
                        bat "devpi use https://devpi.library.illinois.edu && devpi login ${env.DEVPI_USR} --password ${env.DEVPI_PSW} && devpi use /${env.DEVPI_USR}/${env.BRANCH_NAME}_staging && devpi upload --from-dir dist"
                    }
                }
                stage("Test Devpi packages") {
                    parallel {
                        stage("Source Distribution") {
                            environment {
                                PATH = "${tool 'CPython-3.7'};${tool 'CPython-3.6'};$PATH"
                            }
                            agent {
                                node {
                                    label "Windows && Python3 && VS2015"
                                }
                            }
                            options {
                                skipDefaultCheckout(true)

                            }
                            stages{
                                stage("Creating venv to test sdist DevPi package"){
                                    steps {
                                        lock("system_python_${NODE_NAME}"){
                                            bat "python -m venv venv\\venv36"
                                        }
                                        bat "venv\\36\\Scripts\\python.exe -m pip install pip --upgrade && venv\\venv36\\Scripts\\pip.exe install setuptools --upgrade && venv\\venv36\\Scripts\\pip.exe install tox devpi-client"
                                    }
                                }
                                stage("Testing DevPi zip Package"){
                                    environment {
                                        PATH = "${WORKSPACE}\\venv\\36\\Scripts;${tool 'CPython-3.6'};${tool 'CPython-3.7'};$PATH"
                                    }
                                    options{
                                        timeout(10)
                                    }
                                    steps {
                                        bat "devpi.exe use https://devpi.library.illinois.edu/${env.BRANCH_NAME}_staging"
                                        devpiTest(
                                            devpiExecutable: "${powershell(script: '(Get-Command devpi).path', returnStdout: true).trim()}",
                                            url: "https://devpi.library.illinois.edu",
                                            index: "${env.BRANCH_NAME}_staging",
                                            pkgName: "${env.PKG_NAME}",
                                            pkgVersion: "${env.PKG_VERSION}",
                                            pkgRegex: "zip"
                                        )
//                                        }
                                    }
                                    post{
                                        cleanup{
                                            cleanWs deleteDirs: true, patterns: [
                                                [pattern: 'certs', type: 'INCLUDE'],
                                                [pattern: '*@tmp', type: 'INCLUDE']
                                            ]
                                        }
                                    }
                                }
                            }
                        }
                        stage("Built Distribution: .whl") {
                            agent {
                                node {
                                    label "Windows && Python3"
                                }
                            }
                            options {
                                skipDefaultCheckout()
                            }
                            stages{
                                stage("Creating venv to test wheel"){
                                    steps {
                                        lock("system_python_${NODE_NAME}"){
                                            bat "python -m venv venv\\venv36"
                                        }
                                        bat "venv\\36\\Scripts\\python.exe -m pip install pip --upgrade && venv\\36\\Scripts\\pip.exe install setuptools --upgrade && venv\\36\\Scripts\\pip.exe install tox"
                                    }
                                }
                                stage("Testing DevPi Whl Package"){
                                    options{
                                        timeout(10)

                                    }
                                    environment {
                                        PATH = "${WORKSPACE}\\venv\\36\\Scripts;${tool 'CPython-3.6'};${tool 'CPython-3.7'};$PATH"
                                    }
                                    steps{
                                        devpiTest(
                                            devpiExecutable: "${powershell(script: '(Get-Command devpi).path', returnStdout: true).trim()}",
                                            url: "https://devpi.library.illinois.edu",
                                            index: "${env.BRANCH_NAME}_staging",
                                            pkgName: "${env.PKG_NAME}",
                                            pkgVersion: "${env.PKG_VERSION}",
                                            pkgRegex: "whl"
                                        )
                                    }

                                }
                            }
                            post{
                                cleanup{
                                    cleanWs deleteDirs: true, patterns: [
                                        [pattern: 'certs', type: 'INCLUDE'],
                                        [pattern: '*@tmp', type: 'INCLUDE']
                                    ]
                                }
                            }
                        }
                    }
                }
                stage("Deploy to DevPi Production") {
                    when {
                        allOf{
                            equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                            branch "master"
                        }
                    }
                    steps {
                        script {
                            input "Release ${env.PKG_NAME} ${env.PKG_VERSION} to DevPi Production?"
                            bat "venv\\Scripts\\devpi.exe login ${env.DEVPI_USR} --password ${env.DEVPI_PSW}"

                            bat "venv\\Scripts\\devpi.exe use /DS_Jenkins/${env.BRANCH_NAME}_staging"
                            bat "venv\\Scripts\\devpi.exe push ${env.PKG_NAME}==${env.PKG_VERSION} production/release"
                        }
                    }
                }
            }

            post {
                success {
                    echo "it Worked. Pushing file to ${env.BRANCH_NAME} index"
                    bat "venv\\Scripts\\devpi.exe login ${env.DEVPI_USR} --password ${env.DEVPI_PSW}"
                    bat "venv\\Scripts\\devpi.exe use /${env.DEVPI_USR}/${env.BRANCH_NAME}_staging"
                    bat "venv\\Scripts\\devpi.exe push ${env.PKG_NAME}==${env.PKG_VERSION} ${env.DEVPI_USR}/${env.BRANCH_NAME}"
                }
                cleanup{
                    remove_from_devpi("venv\\Scripts\\devpi.exe", "${env.PKG_NAME}", "${env.PKG_VERSION}", "/${env.DEVPI_USR}/${env.BRANCH_NAME}_staging", "${env.DEVPI_USR}", "${env.DEVPI_PSW}")
                }
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
                expression { params.UPDATE_DOCS == true }
            }
            steps {
                dir("build/docs/html/"){
                    bat "dir /s /B"
                    sshPublisher(
                        publishers: [
                            sshPublisherDesc(
                                configName: 'apache-ns - lib-dccuser-updater',
                                sshLabel: [label: 'Linux'],
                                transfers: [sshTransfer(excludes: '',
                                execCommand: '',
                                execTimeout: 120000,
                                flatten: false,
                                makeEmptyDirs: false,
                                noDefaultExcludes: false,
                                patternSeparator: '[, ]+',
                                remoteDirectory: "${params.URL_SUBFOLDER}",
                                remoteDirectorySDF: false,
                                removePrefix: '',
                                sourceFiles: '**')],
                            usePromotionTimestamp: false,
                            useWorkspaceInPromotion: false,
                            verbose: true
                            )
                        ]
                    )
                }
            }
        }
    }
    post{
        cleanup{

            script {
                if(fileExists('source/setup.py')){
                    dir("source"){
                        try{
                            retry(3) {
                                bat "${WORKSPACE}\\venv\\Scripts\\python.exe setup.py clean --all"
                            }
                        } catch (Exception ex) {
                            echo "Unable to successfully run clean. Purging source directory."
                            deleteDir()
                        }
                    }
                }
            }
            cleanWs deleteDirs: true, patterns: [
                [pattern: 'certs', type: 'INCLUDE'],
//                [pattern: 'build', type: 'INCLUDE'],
                [pattern: 'dist', type: 'INCLUDE'],
                [pattern: 'reports', type: 'INCLUDE'],
                [pattern: 'logs', type: 'INCLUDE'],
                [pattern: '*@tmp', type: 'INCLUDE']
                ]
        }
    }
}
