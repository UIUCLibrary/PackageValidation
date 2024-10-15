library identifier: 'JenkinsPythonHelperLibrary@2024.2.0', retriever: modernSCM(
  [$class: 'GitSCMSource',
   remote: 'https://github.com/UIUCLibrary/JenkinsPythonHelperLibrary.git',
   ])

SUPPORTED_MAC_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']
SUPPORTED_LINUX_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']
SUPPORTED_WINDOWS_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']

def DEFAULT_AGENT_DOCKERFILE = 'ci/docker/python/linux/jenkins/Dockerfile'
def DEFAULT_AGENT_LABEL = 'linux && docker && x86'
def DEFAULT_AGENT_DOCKER_BUILD_ARGS =  '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL'

def startup(){
    node('linux && docker && x86') {
        timeout(2){
            ws{
                checkout scm

                try{
                    docker.image('python').inside {
                        stage('Getting Distribution Info'){
                            sh(
                               label: 'Running setup.py with dist_info',
                               script: 'PIP_NO_CACHE_DIR=off python setup.py dist_info'
                            )
                            stash includes: "*.dist-info/**", name: 'DIST-INFO'
                            archiveArtifacts artifacts: "*.dist-info/**"
                        }
                    }
                } finally{
                    deleteDir()
                }
            }
        }
    }
}

def get_props(){
    stage('Reading Package Metadata'){
        node() {
            try{
                def packaging
                dir("${env.WORKSPACE_TMP}/jenkins_helper_scripts") {
                    git branch: 'main', url: 'https://github.com/UIUCLibrary/jenkins_helper_scripts.git'
                    packaging = load 'packaging.groovy'
                }
                unstash 'DIST-INFO'
                return packaging.getProjectMetadataFromDistInfo()
            } finally {
                cleanWs(deleteDirs: true, patterns: [[pattern: "${env.WORKSPACE_TMP}/jenkins_helper_scripts", type: 'INCLUDE']])
                deleteDir()
            }
        }
    }
}
startup()
props = get_props()

pipeline {
    agent none
    environment {
        mypy_args = "--junit-xml=mypy.xml"
        pytest_args = "--junitxml=reports/junit-{env:OS:UNKNOWN_OS}-{envname}.xml --junit-prefix={env:OS:UNKNOWN_OS}  --basetemp={envtmpdir}"
    }
    options {
        timeout(time: 1, unit: 'DAYS')
    }
    parameters {
        booleanParam(name: 'RUN_CHECKS', defaultValue: true, description: 'Run checks on code')
        booleanParam(name: 'TEST_RUN_TOX', defaultValue: false, description: 'Run Tox Tests')
        booleanParam(name: 'BUILD_PACKAGES', defaultValue: false, description: 'Build Python packages')
        booleanParam(name: 'INCLUDE_LINUX_ARM', defaultValue: false, description: 'Include ARM architecture for Linux')
        booleanParam(name: 'INCLUDE_LINUX_X86_64', defaultValue: true, description: 'Include x86_64 architecture for Linux')
        booleanParam(name: 'INCLUDE_MACOS_ARM', defaultValue: false, description: 'Include ARM(m1) architecture for Mac')
        booleanParam(name: 'INCLUDE_MACOS_X86_64', defaultValue: false, description: 'Include x86_64 architecture for Mac')
        booleanParam(name: 'INCLUDE_WINDOWS_X86_64', defaultValue: true, description: 'Include x86_64 architecture for Windows')
        booleanParam(name: 'TEST_PACKAGES', defaultValue: true, description: 'Test Python packages by installing them and running tests on the installed package')
        booleanParam(name: 'DEPLOY_DOCS', defaultValue: false, description: 'Update the documentation')
    }
    stages {
        stage('Building and Testing'){
            when{
                anyOf{
                    equals expected: true, actual: params.RUN_CHECKS
                    equals expected: true, actual: params.TEST_RUN_TOX
                    equals expected: true, actual: params.DEPLOY_DOCS
                }
            }
            stages{
                stage('Building Sphinx Documentation'){
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
                            script: '''mkdir -p logs
                                       python -m sphinx docs/source build/docs/html -d build/docs/.doctrees -v -w logs/build_sphinx.log
                                       '''
                        )
                    }
                    post{
                        always {
                            recordIssues(tools: [sphinxBuild(name: 'Sphinx Documentation Build', pattern: 'logs/build_sphinx.log', id: 'sphinx_build')])
                            archiveArtifacts artifacts: 'logs/build_sphinx.log'
                        }
                        success{
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            script{
                                def DOC_ZIP_FILENAME = "${props.Name}-${props.Version}.doc.zip"
                                zip archive: true, dir: 'build/docs/html', glob: '', zipFile: "dist/${DOC_ZIP_FILENAME}"
                            }
                            stash includes: 'build/docs/html/**,dist/*.doc.zip', name: 'DOCS_ARCHIVE'
                        }
                        failure{
                            echo 'Failed to build Python package'
                        }
                    }
                }
                stage('Checks') {
                    when{
                        equals expected: true, actual: params.RUN_CHECKS
                    }
                    stages{
                        stage('Code Quality'){
                            agent {
                                dockerfile {
                                    filename DEFAULT_AGENT_DOCKERFILE
                                    label DEFAULT_AGENT_LABEL
                                    additionalBuildArgs DEFAULT_AGENT_DOCKER_BUILD_ARGS
                                }
                            }
                            stages{
                                stage('Run Tests'){
                                    parallel {
                                        stage('PyTest'){
                                            steps{
                                                sh 'coverage run --parallel-mode --source=dcc_qc -m pytest --junitxml=reports/junit-pytest.xml'
                                            }
                                            post {
                                                always{
                                                    junit 'reports/junit-pytest.xml'
                                                }
                                            }
                                        }
                                        stage('Documentation'){
                                            steps{
                                                    sh '''mkdir -p logs
                                                          python -m sphinx -b doctest docs/source build/docs -d build/docs/doctrees -v -w logs/doctest.log --no-color
                                                          '''
                                            }
                                            post{
                                                always {
                                                    recordIssues(tools: [sphinxBuild(pattern: 'logs/doctest.log')])

                                                }
                                            }
                                        }
                                        stage('Task Scanner'){
                                            steps{
                                                recordIssues(tools: [taskScanner(highTags: 'FIXME', includePattern: 'dcc_qc/**/*.py', normalTags: 'TODO')])
                                            }
                                        }
                                        stage('MyPy'){
                                            steps{
                                                catchError(buildResult: 'SUCCESS', message: 'MyPy found issues', stageResult: 'UNSTABLE') {
                                                    tee('logs/mypy.log'){
                                                        sh 'mypy -p dcc_qc --html-report reports/mypy_html'
                                                    }
                                                }
                                            }
                                            post{
                                                always {
                                                    recordIssues(tools: [myPy(name: 'MyPy', pattern: 'logs/mypy.log')])
                                                    publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'reports/mypy_html', reportFiles: 'index.html', reportName: 'MyPy', reportTitles: ''])
                                                }
                                            }
                                        }
                                        stage('Run Flake8 Static Analysis') {
                                            steps{
                                                catchError(buildResult: 'SUCCESS', message: 'Flake8 found issues', stageResult: 'UNSTABLE') {
                                                    sh '''mkdir -p logs
                                                          flake8 dcc_qc --format=pylint --tee --output-file=logs/flake8.log
                                                          '''
                                                }
                                            }
                                            post {
                                                always {
                                                    recordIssues(tools: [flake8(name: 'Flake8', pattern: 'logs/flake8.log')])
                                                    stash includes: 'logs/flake8.log', name: 'FLAKE8_REPORT'
                                                }
                                            }
                                        }
                                    }
                                    post{
                                        always{
                                            sh 'coverage combine'
                                            sh 'coverage xml -o reports/coverage.xml'
                                            recordCoverage(tools: [[parser: 'COBERTURA', pattern: 'reports/coverage.xml']])
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
                    }
                }
                stage('Run Tox'){
                    when{
                        equals expected: true, actual: params.TEST_RUN_TOX
                    }
                    parallel{
                        stage('Linux'){
                            when{
                                expression {return nodesByLabel('linux && docker && x86').size() > 0}
                            }
                            steps{
                                script{
                                    parallel(
                                        getToxTestsParallel(
                                            envNamePrefix: 'Tox Linux',
                                            label: 'linux && docker && x86',
                                            dockerfile: 'ci/docker/python/linux/tox/Dockerfile',
                                            dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                            dockerRunArgs: '-v pipcache_packagevalidate:/.cache/pip',
                                            retry: 3
                                        )
                                    )
                                }
                            }
                        }
                        stage('Windows'){
                            when{
                                expression {return nodesByLabel('windows && docker && x86').size() > 0}
                            }
                            steps{
                                script{
                                    parallel(
                                        getToxTestsParallel(
                                            envNamePrefix: 'Tox Windows',
                                            label: 'windows && docker && x86',
                                            dockerfile: 'ci/docker/python/windows/tox/Dockerfile',
                                            dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE --build-arg PIP_DOWNLOAD_CACHE=c:/users/containeradministrator/appdata/local/pip',
                                            dockerRunArgs: '-v pipcache_packagevalidate:c:/users/containeradministrator/appdata/local/pip',
                                            retry: 3
                                        )
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
        stage('Packaging') {
            when{
                anyOf{
                    equals expected: true, actual: params.BUILD_PACKAGES
                }
                beforeAgent true
            }
            stages{
                stage('Source and Wheel formats'){
                    options{
                      retry(2)
                    }
                    agent {
                        docker {
                            image 'python'
                            label 'linux && docker'
                        }
                    }
                    steps{
                        sh(
                           label: 'Creating Python packages',
                           script: '''python -m venv venv --upgrade-deps
                                      venv/bin/pip install build
                                      venv/bin/python -m build
                                   '''
                           )
                    }
                    post {
                        success {
                            archiveArtifacts(
                                artifacts: 'dist/*.whl,dist/*.tar.gz,dist/*.zip',
                                fingerprint: true
                            )
                            stash includes: 'dist/*.whl,dist/*.tar.gz,dist/*.zip', name: 'PYTHON_PACKAGES'
                        }
                        cleanup{
                            cleanWs(
                                deleteDirs: true,
                                patterns: [
                                    [pattern: 'venv/', type: 'INCLUDE'],
                                    [pattern: 'dist/', type: 'INCLUDE'],
                                    [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                ]
                            )
                        }
                    }
                }
                stage('Testing'){
                    when{
                        equals expected: true, actual: params.TEST_PACKAGES
                    }
                    steps{
                        script{
                            def macTestStages = [:]
                            SUPPORTED_MAC_VERSIONS.each{ pythonVersion ->
                                def macArchitectures = []
                                if(params.INCLUDE_MACOS_X86_64 == true){
                                    macArchitectures.add('x86_64')
                                }
                                if(params.INCLUDE_MACOS_ARM == true){
                                    macArchitectures.add('m1')
                                }
                                macArchitectures.each{ processorArchitecture ->
                                    if (nodesByLabel("mac && ${processorArchitecture} && python${pythonVersion}").size() > 0){
                                        macTestStages["Mac ${processorArchitecture} - Python ${pythonVersion}: sdist"] = {
                                            testPythonPkg(
                                                    agent: [
                                                        label: "mac && python${pythonVersion} && ${processorArchitecture}",
                                                    ],
                                                    testSetup: {
                                                        checkout scm
                                                        unstash 'PYTHON_PACKAGES'
                                                    },
                                                    retries: 3,
                                                    testCommand: {
                                                        findFiles(glob: 'dist/*.tar.gz').each{
                                                            sh(label: 'Running Tox',
                                                               script: """python${pythonVersion} -m venv venv
                                                               ./venv/bin/python -m pip install --upgrade pip
                                                               ./venv/bin/pip install -r requirements/requirements_tox.txt
                                                               ./venv/bin/tox --installpkg ${it.path} -e py${pythonVersion.replace('.', '')}"""
                                                            )
                                                        }

                                                    },
                                                    post:[
                                                        cleanup: {
                                                            cleanWs(
                                                                patterns: [
                                                                        [pattern: 'dist/', type: 'INCLUDE'],
                                                                        [pattern: 'venv/', type: 'INCLUDE'],
                                                                        [pattern: '.tox/', type: 'INCLUDE'],
                                                                    ],
                                                                notFailBuild: true,
                                                                deleteDirs: true
                                                            )
                                                        },
                                                    ]
                                                )
                                        }
                                        macTestStages["Mac ${processorArchitecture} - Python ${pythonVersion}: wheel"] = {
                                            testPythonPkg(
                                                agent: [
                                                    label: "mac && python${pythonVersion} && ${processorArchitecture}",
                                                ],
                                                retries: 3,
                                                testCommand: {
                                                    unstash 'PYTHON_PACKAGES'
                                                    findFiles(glob: 'dist/*.whl').each{
                                                        sh(label: 'Running Tox',
                                                           script: """python${pythonVersion} -m venv venv
                                                                      . ./venv/bin/activate
                                                                      python -m pip install --upgrade pip
                                                                      pip install -r requirements/requirements_tox.txt
                                                                      tox --installpkg ${it.path} -e py${pythonVersion.replace('.', '')}
                                                                   """
                                                        )
                                                    }
                                                },
                                                post:[
                                                    cleanup: {
                                                        cleanWs(
                                                            patterns: [
                                                                    [pattern: 'dist/', type: 'INCLUDE'],
                                                                    [pattern: 'venv/', type: 'INCLUDE'],
                                                                    [pattern: '.tox/', type: 'INCLUDE'],
                                                                ],
                                                            notFailBuild: true,
                                                            deleteDirs: true
                                                        )
                                                    },
                                                    success: {
                                                         archiveArtifacts artifacts: 'dist/*.whl'
                                                    }
                                                ]
                                            )
                                        }
                                    }
                                }
                            }
                            def windowsTestStages = [:]
                            if(params.INCLUDE_WINDOWS_X86_64 == true){
                                SUPPORTED_WINDOWS_VERSIONS.each{ pythonVersion ->
                                    windowsTestStages["Windows - Python ${pythonVersion}: sdist"] = {
                                        testPythonPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: 'windows && docker && x86',
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE --build-arg PIP_DOWNLOAD_CACHE=c:/users/containeradministrator/appdata/local/pip',
                                                    args: '-v pipcache_packagevalidate:c:/users/containeradministrator/appdata/local/pip'
                                                ]
                                            ],
                                            retries: 3,
                                            testSetup: {
                                                checkout scm
                                                unstash 'PYTHON_PACKAGES'
                                            },
                                            testCommand: {
                                                findFiles(glob: 'dist/*.tar.gz').each{
                                                    bat(label: 'Running Tox', script: "tox --workdir %TEMP%\\tox --installpkg ${it.path} -e py${pythonVersion.replace('.', '')} -v")
                                                }
                                            },
                                            post:[
                                                cleanup: {
                                                    cleanWs(
                                                        patterns: [
                                                            [pattern: 'dist/', type: 'INCLUDE'],
                                                            [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                        ],
                                                        notFailBuild: true,
                                                        deleteDirs: true
                                                    )
                                                },
                                            ]
                                        )
                                    }
                                    windowsTestStages["Windows - Python ${pythonVersion}: wheel"] = {
                                        testPythonPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: 'windows && docker && x86',
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE --build-arg PIP_DOWNLOAD_CACHE=c:/users/containeradministrator/appdata/local/pip',
                                                    args: '-v pipcache_packagevalidate:c:/users/containeradministrator/appdata/local/pip'
                                                ],
                                            ],
                                            retries: 3,
                                            testSetup: {
                                                 checkout scm
                                                 unstash 'PYTHON_PACKAGES'
                                            },
                                            testCommand: {
                                                 findFiles(glob: 'dist/*.whl').each{
                                                     powershell(label: 'Running Tox', script: "tox --installpkg ${it.path} --workdir \$env:TEMP\\tox  -e py${pythonVersion.replace('.', '')}")
                                                 }

                                            },
                                            post:[
                                                cleanup: {
                                                    cleanWs(
                                                        patterns: [
                                                                [pattern: 'dist/', type: 'INCLUDE'],
                                                                [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                            ],
                                                        notFailBuild: true,
                                                        deleteDirs: true
                                                    )
                                                },
                                                success: {
                                                    archiveArtifacts artifacts: 'dist/*.whl'
                                                }
                                            ]
                                        )
                                    }
                                }
                            }
                            def linuxTestStages = [:]
                            def linuxArchitectures = []
                            if(params.INCLUDE_LINUX_X86_64 == true){
                                linuxArchitectures.add('x86_64')
                            }
                            if(params.INCLUDE_LINUX_ARM == true){
                                linuxArchitectures.add('arm64')
                            }
                            SUPPORTED_LINUX_VERSIONS.each{ pythonVersion ->
                                linuxArchitectures.each{arch ->
                                    linuxTestStages["Linux ${arch} - Python ${pythonVersion}: sdist"] = {
                                        testPythonPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: "linux && docker && ${arch}",
                                                    filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                                    args: '-v pipcache_packagevalidate:/.cache/pip',
                                                ]
                                            ],
                                            retries: 3,
                                            testSetup: {
                                                checkout scm
                                                unstash 'PYTHON_PACKAGES'
                                            },
                                            testCommand: {
                                                findFiles(glob: 'dist/*.tar.gz').each{
                                                    sh(
                                                        label: 'Running Tox',
                                                        script: "tox --installpkg ${it.path} --workdir /tmp/tox -e py${pythonVersion.replace('.', '')}"
                                                        )
                                                }
                                            },
                                            post:[
                                                cleanup: {
                                                    cleanWs(
                                                        patterns: [
                                                                [pattern: 'dist/', type: 'INCLUDE'],
                                                                [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                            ],
                                                        notFailBuild: true,
                                                        deleteDirs: true
                                                    )
                                                },
                                            ]
                                        )
                                    }
                                    linuxTestStages["Linux ${arch} - Python ${pythonVersion}: wheel"] = {
                                        testPythonPkg(
                                            agent: [
                                                dockerfile: [
                                                    label: "linux && docker && ${arch}",
                                                    filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                                    args: '-v pipcache_packagevalidate:/.cache/pip',
                                                ]
                                            ],
                                            retries: 3,
                                            testSetup: {
                                                checkout scm
                                                unstash 'PYTHON_PACKAGES'
                                            },
                                            testCommand: {
                                                findFiles(glob: 'dist/*.whl').each{
                                                    timeout(5){
                                                        sh(
                                                            label: 'Running Tox',
                                                            script: "tox --installpkg ${it.path} --workdir /tmp/tox -e py${pythonVersion.replace('.', '')}"
                                                            )
                                                    }
                                                }
                                            },
                                            post:[
                                                cleanup: {
                                                    cleanWs(
                                                        patterns: [
                                                                [pattern: 'dist/', type: 'INCLUDE'],
                                                                [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                            ],
                                                        notFailBuild: true,
                                                        deleteDirs: true
                                                    )
                                                },
                                                success: {
                                                    archiveArtifacts artifacts: 'dist/*.whl'
                                                },
                                            ]
                                        )
                                    }
                                }
                            }
                            parallel(windowsTestStages + linuxTestStages + macTestStages)
                        }
                    }
                }
            }
        }
        stage('Deploy Online Documentation') {
            when{
                equals expected: true, actual: params.DEPLOY_DOCS
                beforeAgent true
                beforeInput true
            }
            agent {
                dockerfile {
                    filename 'ci/docker/python/linux/jenkins/Dockerfile'
                    label "linux && docker && x86"
                }
            }
            options{
                timeout(time: 1, unit: 'DAYS')
            }
            input {
                message 'Update project documentation?'
            }
            steps{
                unstash 'DOCS_ARCHIVE'
                withCredentials([usernamePassword(credentialsId: 'dccdocs-server', passwordVariable: 'docsPassword', usernameVariable: 'docsUsername')]) {
                    sh 'python utils/upload_docs.py --username=$docsUsername --password=$docsPassword --subroute=package_qc build/docs/html apache-ns.library.illinois.edu'
                }
            }
            post{
                cleanup{
                    cleanWs(
                        deleteDirs: true,
                        patterns: [
                            [pattern: 'build/', type: 'INCLUDE'],
                            [pattern: 'dist/', type: 'INCLUDE'],
                        ]
                    )
                }
            }
        }
//         stage('Update online documentation') {
//             agent any
//             when {
//                 equals expected: true, actual: params.UPDATE_DOCS
//             }
//             options {
//                 skipDefaultCheckout()
//             }
//             steps {
//                 unstash 'DOCS_ARCHIVE'
//                 dir('build/docs/html/'){
//                     bat 'dir /s /B'
//                     sshPublisher(
//                         publishers: [
//                             sshPublisherDesc(
//                                 configName: 'apache-ns - lib-dccuser-updater',
//                                 sshLabel: [label: 'Linux'],
//                                 transfers: [sshTransfer(excludes: '',
//                                 execCommand: '',
//                                 execTimeout: 120000,
//                                 flatten: false,
//                                 makeEmptyDirs: false,
//                                 noDefaultExcludes: false,
//                                 patternSeparator: '[, ]+',
//                                 remoteDirectory: "${params.URL_SUBFOLDER}",
//                                 remoteDirectorySDF: false,
//                                 removePrefix: '',
//                                 sourceFiles: '**')],
//                             usePromotionTimestamp: false,
//                             useWorkspaceInPromotion: false,
//                             verbose: true
//                             )
//                         ]
//                     )
//                 }
//             }
//         }
    }
}
