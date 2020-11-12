#!/usr/bin/env groovy
@Library("ds-utils")
import org.ds.*

@Library(["devpi", "PythonHelpers"]) _
CONFIGURATIONS = [
    '3.6': [
        test_docker_image: "python:3.6-windowsservercore",
        tox_env: "py36"
        ],
    "3.7": [
        test_docker_image: "python:3.7",
        tox_env: "py37"
        ]
]

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
def DEFAULT_AGENT_DOCKERFILE = 'ci/docker/python/linux/jenkins/Dockerfile'
def DEFAULT_AGENT_LABEL = 'linux && docker'
def DEFAULT_AGENT_DOCKER_BUILD_ARGS =  '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
pipeline {
    agent none
    environment {
        mypy_args = "--junit-xml=mypy.xml"
        pytest_args = "--junitxml=reports/junit-{env:OS:UNKNOWN_OS}-{envname}.xml --junit-prefix={env:OS:UNKNOWN_OS}  --basetemp={envtmpdir}"
    }
    parameters {
        booleanParam(name: "TEST_RUN_TOX", defaultValue: false, description: "Run Tox Tests")
        booleanParam(name: "PACKAGE_CX_FREEZE", defaultValue: false, description: "Create standalone install with CX_Freeze")
        booleanParam(name: "DEPLOY_DEVPI", defaultValue: true, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: "DEPLOY_DEVPI_PRODUCTION", defaultValue: false, description: "Deploy to https://devpi.library.illinois.edu/production/release")
        booleanParam(name: "UPDATE_DOCS", defaultValue: false, description: "Update the documentation")
        string(name: 'URL_SUBFOLDER', defaultValue: "package_qc", description: 'The directory that the docs should be saved under')
    }
    stages {
        stage("Getting Distribution Info"){
            agent {
                dockerfile {
                    filename DEFAULT_AGENT_DOCKERFILE
                    label DEFAULT_AGENT_LABEL
                    additionalBuildArgs DEFAULT_AGENT_DOCKER_BUILD_ARGS
                }
            }
            steps{
                sh "python setup.py dist_info"
            }
            post{
                success{
                    stash includes: "dcc_qc.dist-info/**", name: 'DIST-INFO'
                    archiveArtifacts artifacts: "dcc_qc.dist-info/**"
                }
                cleanup{
                    cleanWs(
                        deleteDirs: true,
                        patterns: [
                            [pattern: "dcc_qc.dist-info/", type: 'INCLUDE'],
                            [pattern: "dcc_qc.egg-info/", type: 'INCLUDE'],
                        ]
                    )
                }
            }
        }
        stage("Building Sphinx Documentation"){
            agent {
                dockerfile {
                    filename DEFAULT_AGENT_DOCKERFILE
                    label DEFAULT_AGENT_LABEL
                    additionalBuildArgs DEFAULT_AGENT_DOCKER_BUILD_ARGS
                }
            }
            steps {
                sh (
                    label: "Building docs on ${env.NODE_NAME}",
                    script: """mkdir -p logs
                               python -m sphinx docs/source build/docs/html -d build/docs/.doctrees -v -w logs/build_sphinx.log
                               """
                )
            }
            post{
                always {
                    recordIssues(tools: [sphinxBuild(name: 'Sphinx Documentation Build', pattern: 'logs/build_sphinx.log', id: 'sphinx_build')])
                    archiveArtifacts artifacts: 'logs/build_sphinx.log'
                }
                success{
                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                    stash includes: "build/docs/html/**", name: 'DOCS_ARCHIVE'
//                     script{
//                         def DOC_ZIP_FILENAME = "${env.PKG_NAME}-${env.PKG_VERSION}.doc.zip"
//                     zip archive: true, dir: "build/docs/html", glob: '', zipFile: "dist/${DOC_ZIP_FILENAME}"
//                     }
                }
                failure{
                    echo "Failed to build Python package"
                }
            }
        }
//         stage("Building") {
//             agent {
//                 dockerfile {
//                     filename DEFAULT_AGENT_DOCKERFILE
//                     label DEFAULT_AGENT_LABEL
//                     additionalBuildArgs DEFAULT_AGENT_DOCKER_BUILD_ARGS
//                 }
//             }
//             stages{
//                 stage("Building Sphinx Documentation"){
//                     steps {
//                         script{
//                             // Add a line to config file so auto docs look in the build folder
//                             def sphinx_config_file = 'docs/source/conf.py'
//                             def extra_line = "sys.path.insert(0, os.path.abspath('${WORKSPACE}/build/lib'))"
//                             def readContent = readFile "${sphinx_config_file}"
//                             echo "Adding \"${extra_line}\" to ${sphinx_config_file}."
//                             writeFile file: "${sphinx_config_file}", text: readContent+"\r\n${extra_line}\r\n"
//
//
//                         }
//
// //                         bat "if not exist logs mkdir logs"
// //                         powershell(
// //                             label: "Building docs on ${env.NODE_NAME}",
// //                             script: "& python setup.py build_sphinx --build-dir ${WORKSPACE}\\build\\docs | tee ${WORKSPACE}\\logs\\build_sphinx.log"
// //                         )
//                     }
//                     post{
//                         always {
//                             recordIssues(tools: [sphinxBuild(name: 'Sphinx Documentation Build', pattern: 'logs/build_sphinx.log', id: 'sphinx_build')])
//                             archiveArtifacts artifacts: 'logs/build_sphinx.log'
//                         }
//                         success{
//                             unstash "DIST-INFO"
//                             script{
//                                 def props = readProperties interpolate: true, file: 'dcc_qc.dist-info/METADATA'
//                                 def DOC_ZIP_FILENAME = "${props.Name}-${props.Version}.doc.zip"
//                                 publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
//                                 zip archive: true, dir: "${WORKSPACE}/build/docs/html", glob: '', zipFile: "dist/${DOC_ZIP_FILENAME}"
//                                 stash includes: "dist/${DOC_ZIP_FILENAME},build/docs/html/**", name: 'DOCS_ARCHIVE'
//                             }
//
//                         }
//                     }
//                 }
//             }
//             post{
//                 cleanup{
//                     cleanWs(
//                         patterns: [
//                             [pattern: 'build/', type: 'INCLUDE'],
//                             ],
//                         deleteDirs: true,
//                     )
//                 }
//             }
//         }
        stage("Tests") {
            agent {
                dockerfile {
                    filename DEFAULT_AGENT_DOCKERFILE
                    label DEFAULT_AGENT_LABEL
                    additionalBuildArgs DEFAULT_AGENT_DOCKER_BUILD_ARGS
                }
            }
            stages{
                stage("Run Tests"){
                    parallel {
                        stage("PyTest"){
                            steps{
                                sh "python -m pytest --junitxml=reports/junit-${env.NODE_NAME}-pytest.xml --junit-prefix=${env.NODE_NAME}-pytest --cov-report html:reports/coverage/ --cov=MedusaPackager" //  --basetemp={envtmpdir}"
                            }
                            post {
                                always{
                                    junit "reports/junit-${env.NODE_NAME}-pytest.xml"
                                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/coverage', reportFiles: 'index.html', reportName: 'Coverage', reportTitles: ''])
                                }
                            }
                        }
//                             steps{
// //                                 bat(
// //                                     label: "Run PyTest",
// //                                     script: "coverage run --parallel-mode --source=dcc_qc -m pytest --junitxml=${WORKSPACE}/reports/pytest/junit-${env.NODE_NAME}-pytest.xml --junit-prefix=${env.NODE_NAME}-pytest" //  --basetemp={envtmpdir}"
// //                                 )
//
//                             }
//                             post {
//                                 always{
//                                     junit "reports/pytest/junit-*.xml"
//                                 }
//                                 cleanup{
//                                     cleanWs(
//                                         patterns: [
//                                             [pattern: 'reports/pytest/junit-*.xml', type: 'INCLUDE'],
//                                             [pattern: '.pytest_cache/', type: 'INCLUDE'],
//                                         ],
//                                         deleteDirs: true,
//                                     )
//                                 }
//                             }
//                         }
//                         stage("Documentation"){
//                             steps{
//                                 bat "python -m sphinx -b doctest docs\\source ${WORKSPACE}\\build\\docs -d ${WORKSPACE}\\build\\docs\\doctrees -v"
//                             }
//
//                         }
                        stage("Documentation"){
                            steps{
                                    sh """mkdir -p logs
                                          python -m sphinx -b doctest docs/source build/docs -d build/docs/doctrees -v -w logs/doctest.log --no-color
                                          """
                            }
                            post{
                                always {
                                    recordIssues(tools: [sphinxBuild(pattern: 'logs/doctest.log')])

                                }
                            }
                        }
//                         stage("MyPy"){
//                             steps{
//                                 powershell returnStatus: true, script: "& mypy -p dcc_qc | tee ${WORKSPACE}\\logs\\mypy.log"
//                                 powershell returnStatus: true, script: "& mypy -p dcc_qc --html-report ${WORKSPACE}\\reports\\mypy\\html"
//                             }
//                             post{
//                                 always {
//                                     archiveArtifacts "logs\\mypy.log"
//                                     recordIssues(tools: [myPy(name: 'MyPy', pattern: 'logs/mypy.log')])
//                                     publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy/html', reportFiles: 'index.html', reportName: 'MyPy', reportTitles: ''])
//                                 }
//                                 cleanup{
//                                     cleanWs(
//                                         patterns: [
//                                             [pattern: 'logs/mypy.log', type: 'INCLUDE'],
//                                             [pattern: '.mypy_cache/', type: 'INCLUDE'],
//                                             ],
//                                         deleteDirs: true,
//                                     )
//                                 }
//                             }
//                         }
                        stage("MyPy"){
                            steps{
                                sh "mypy -p dcc_qc --junit-xml=junit-${env.NODE_NAME}-mypy.xml --html-report reports/mypy_html"
                            }
                            post{
                                always {
                                    junit "junit-${env.NODE_NAME}-mypy.xml"
                                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy_html', reportFiles: 'index.html', reportName: 'MyPy', reportTitles: ''])
                                }
                            }
                        }
//                         stage("Run Flake8 Static Analysis") {
//                             steps{
//                                 script{
//                                     bat(
//                                         label: "Run Flake8",
//                                         returnStatus: true,
//                                         script: "flake8 dcc_qc --tee --output-file=${WORKSPACE}/logs/flake8.log"
//                                     )
//                                 }
//                             }
//                             post {
//                                 always {
//                                     archiveArtifacts "logs/flake8.log"
//                                     stash includes: "logs/flake8.log", name: 'FLAKE8_LOGS'
//                                     unstash "FLAKE8_LOGS"
//                                     recordIssues(tools: [flake8(name: 'Flake8', pattern: 'logs/flake8.log')])
//                                 }
//                             }
//                         }
                        stage("Run Flake8 Static Analysis") {
                            steps{
                                catchError(buildResult: "SUCCESS", message: 'Flake8 found issues', stageResult: "UNSTABLE") {
                                    sh '''mkdir -p logs
                                          flake8 uiucprescon --format=pylint --tee --output-file=logs/flake8.log
                                          '''
                                }
                            }
                            post {
                                always {
                                    recordIssues(tools: [flake8(name: 'Flake8', pattern: 'logs/flake8.log')])
                                    stash includes: "logs/flake8.log", name: "FLAKE8_REPORT"
                                }
                            }
                        }
//                         stage("Run Tox test") {
//                             when {
//                                equals expected: true, actual: params.TEST_RUN_TOX
//                             }
//
//                             options{
//                                 timeout(15)
//                             }
//                             steps {
//                                 bat (
//                                     label: "Run Tox",
//                                     script: "tox --workdir ${WORKSPACE}\\.tox -e py -v"
//                                 )
//                             }
//                             post{
//                                 always{
//                                     archiveArtifacts allowEmptyArchive: true, artifacts: '.tox/py*/log/*.log,.tox/log/*.log,logs/tox_report.json'
//                                 }
//                                 cleanup{
//                                     cleanWs(
//                                         deleteDirs: true,
//                                         patterns: [
//                                             [pattern: '.tox/py*/log/*.log', type: 'INCLUDE'],
//                                             [pattern: '.tox/log/*.log', type: 'INCLUDE'],
//                                             [pattern: 'logs/rox_report.json', type: 'INCLUDE']
//                                         ]
//                                     )
//                                 }
//                             }
//                         }
                    }
                    post{
                        always{
                            bat "coverage combine"
                            bat "coverage xml -o ${WORKSPACE}\\reports\\coverage.xml"
                            bat "coverage html -d ${WORKSPACE}\\reports\\coverage"
                            publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: "reports/coverage", reportFiles: 'index.html', reportName: 'Coverage', reportTitles: ''])
                            publishCoverage adapters: [
                                            coberturaAdapter('reports/coverage.xml')
                                            ],
                                        sourceFileResolver: sourceFiles('STORE_ALL_BUILD')

                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/coverage', reportFiles: 'index.html', reportName: 'Coverage', reportTitles: ''])
                        }
                        cleanup{
                            cleanWs(
                                patterns: [
                                    [pattern: 'build/', type: 'INCLUDE'],
                                    [pattern: 'logs/', type: 'INCLUDE'],
                                    [pattern: 'reports/', type: 'INCLUDE'],
                                    [pattern: 'reports/coverage', type: 'INCLUDE'],
                                ],
                                deleteDirs: true,
                            )
                        }
                    }

                }
            }
        }
        stage("Packaging") {
            failFast true
            parallel {
                stage("Source and Wheel formats"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python37/windows/build/msvc/Dockerfile'
                            label "windows && docker"
                        }
                    }
                    stages{
                        stage("Packaging sdist and wheel"){
                            steps{
                                bat script: "python setup.py sdist -d dist --format=zip bdist_wheel -d dist"
                            }
                            post {
                                success {
                                    archiveArtifacts(
                                        artifacts: "dist/*.whl,dist/*.tar.gz,dist/*.zip",
                                        fingerprint: true
                                    )
                                    stash includes: "dist/*.whl,dist/*.tar.gz,dist/*.zip", name: 'PYTHON_PACKAGES'
                                }
                                cleanup{
                                    cleanWs(
                                        deleteDirs: true,
                                        patterns: [
                                            [pattern: 'dist/*.whl,dist/*.tar.gz,dist/*.zip', type: 'INCLUDE']
                                        ]
                                    )
                                }
                            }
                        }
                    }
                }
                stage("Windows CX_Freeze MSI"){
                    agent {
                        dockerfile {
                            filename 'ci/docker/python37/windows/build/msvc/Dockerfile'
                            label "windows && docker"
                        }
                    }
                    when {
                        equals expected: true, actual: params.PACKAGE_CX_FREEZE
                        beforeAgent true
                    }
                    steps{
                        bat "python cx_setup.py bdist_msi --add-to-path=true -k --bdist-dir build/msi"
                    }
                    post{
                        success{
                            stash includes: "dist/*.msi", name: "msi"
                            archiveArtifacts artifacts: "dist/*.msi", fingerprint: true
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
                beforeAgent true
            }
            agent none
            environment{
                DEVPI = credentials("DS_devpi")
            }
            stages{
                stage("Deploy to Devpi Staging") {
                    agent {
                        dockerfile {
                            filename 'ci/docker/deploy/devpi/deploy/Dockerfile'
                            label 'linux&&docker'
                            additionalBuildArgs '--build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)'
                          }
                    }
                    steps {
                        unstash 'DOCS_ARCHIVE'
                        unstash 'PYTHON_PACKAGES'
                        sh(
                                label: "Connecting to DevPi Server",
                                script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                            )
                        sh(
                            label: "Uploading to DevPi Staging",
                            script: """devpi use /${env.DEVPI_USR}/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi
devpi upload --from-dir dist --clientdir ${WORKSPACE}/devpi"""
                        )
                    }
                }
                stage("Test DevPi packages") {
                    matrix {
                        axes {
                            axis {
                                name 'FORMAT'
                                values 'zip', "whl"
                            }
                            axis {
                                name 'PYTHON_VERSION'
                                values '3.6', "3.7"
                            }
                        }
                        agent {
                          dockerfile {
                            additionalBuildArgs "--build-arg PYTHON_DOCKER_IMAGE_BASE=${CONFIGURATIONS[PYTHON_VERSION].test_docker_image}"
                            filename 'ci/docker/deploy/devpi/test/windows/Dockerfile'
                            label 'windows && docker'
                          }
                        }
                        stages{
                            stage("Testing DevPi Package"){
                                options{
                                    timeout(10)
                                }
                                steps{
                                    script{
                                        unstash "DIST-INFO"
                                        def props = readProperties interpolate: true, file: 'dcc_qc.dist-info/METADATA'
                                        bat(
                                            label: "Connecting to Devpi Server",
                                            script: "devpi use https://devpi.library.illinois.edu --clientdir certs\\ && devpi login %DEVPI_USR% --password %DEVPI_PSW% --clientdir certs\\ && devpi use ${env.BRANCH_NAME}_staging --clientdir certs\\"
                                        )
                                        bat(
                                            label: "Testing package stored on DevPi",
                                            script: "devpi test --index ${env.BRANCH_NAME}_staging ${props.Name}==${props.Version} -s ${FORMAT} --clientdir certs\\ -e ${CONFIGURATIONS[PYTHON_VERSION].tox_env} -v"
                                        )
                                    }
                                }
                                post{
                                    cleanup{
                                        cleanWs(
                                            deleteDirs: true,
                                            patterns: [
                                                [pattern: "dist/", type: 'INCLUDE'],
                                                [pattern: "certs/", type: 'INCLUDE'],
                                                [pattern: "dcc_qc.dist-info/", type: 'INCLUDE'],
                                                [pattern: 'build/', type: 'INCLUDE']
                                            ]
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
            post{
                success{
                    node('linux && docker') {
                       script{
                            docker.build("dcc_qc:devpi",'-f ./ci/docker/deploy/devpi/deploy/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                unstash "DIST-INFO"
                                def props = readProperties interpolate: true, file: 'dcc_qc.dist-info/METADATA'
                                sh(
                                    label: "Connecting to DevPi Server",
                                    script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                                )
                                sh(
                                    label: "Selecting to DevPi index",
                                    script: "devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi"
                                )
                                sh(
                                    label: "Pushing package to DevPi index",
                                    script:  "devpi push ${props.Name}==${props.Version} DS_Jenkins/${env.BRANCH_NAME} --clientdir ${WORKSPACE}/devpi"
                                )
                            }
                       }
                    }
                }
                cleanup{
                    node('linux && docker') {
                       script{
                            docker.build("dcc_qc:devpi",'-f ./ci/docker/deploy/devpi/deploy/Dockerfile --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .').inside{
                                unstash "DIST-INFO"
                                def props = readProperties interpolate: true, file: 'dcc_qc.dist-info/METADATA'
                                sh(
                                    label: "Connecting to DevPi Server",
                                    script: 'devpi use https://devpi.library.illinois.edu --clientdir ${WORKSPACE}/devpi && devpi login $DEVPI_USR --password $DEVPI_PSW --clientdir ${WORKSPACE}/devpi'
                                )
                                sh(
                                    label: "Selecting to DevPi index",
                                    script: "devpi use /DS_Jenkins/${env.BRANCH_NAME}_staging --clientdir ${WORKSPACE}/devpi"
                                )
                                sh(
                                    label: "Removing package to DevPi index",
                                    script: "devpi remove -y ${props.Name}==${props.Version} --clientdir ${WORKSPACE}/devpi"
                                )
                            }
                       }
                    }
                }
            }
        }
        stage("Update online documentation") {
            agent any
            when {
                equals expected: true, actual: params.UPDATE_DOCS
            }
            options {
                skipDefaultCheckout()
            }
            steps {
                unstash "DOCS_ARCHIVE"
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
}
