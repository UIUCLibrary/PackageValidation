library identifier: 'JenkinsPythonHelperLibrary@2024.1.1', retriever: modernSCM(
  [$class: 'GitSCMSource',
   remote: 'https://github.com/UIUCLibrary/JenkinsPythonHelperLibrary.git',
   ])

def getDevPiStagingIndex(){

    if (env.TAG_NAME?.trim()){
        return 'tag_staging'
    } else{
        return "${env.BRANCH_NAME}_staging"
    }
}
SUPPORTED_MAC_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']
SUPPORTED_LINUX_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']
SUPPORTED_WINDOWS_VERSIONS = ['3.8', '3.9', '3.10', '3.11', '3.12']


def getDevpiConfig() {
    node(){
        configFileProvider([configFile(fileId: 'devpi_config', variable: 'CONFIG_FILE')]) {
            def configProperties = readProperties(file: CONFIG_FILE)
            configProperties.stagingIndex = {
                if (env.TAG_NAME?.trim()){
                    return 'tag_staging'
                } else{
                    return "${env.BRANCH_NAME}_staging"
                }
            }()
            return configProperties
        }
    }
}
def DEVPI_CONFIG = getDevpiConfig()


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
    def packaging = fileLoader.fromGit(
        'packaging',
        'https://github.com/UIUCLibrary/jenkins_helper_scripts.git',
        '7',
        null,
        ''
    )
    stage('Reading Package Metadata'){
        node() {
            try{
                unstash 'DIST-INFO'
                return packaging.getProjectMetadataFromDistInfo()
            } finally {
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
        booleanParam(name: 'DEPLOY_DEVPI', defaultValue: false, description: "Deploy to devpi on http://devpy.library.illinois.edu/DS_Jenkins/${env.BRANCH_NAME}")
        booleanParam(name: 'DEPLOY_DEVPI_PRODUCTION', defaultValue: false, description: 'Deploy to https://devpi.library.illinois.edu/production/release')
        booleanParam(name: 'DEPLOY_DOCS', defaultValue: false, description: 'Update the documentation')
    }
    stages {
        stage('Building and Testing'){
            when{
                anyOf{
                    equals expected: true, actual: params.RUN_CHECKS
                    equals expected: true, actual: params.TEST_RUN_TOX
                    equals expected: true, actual: params.DEPLOY_DEVPI
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
                    steps {
                        script{
                            def windowsJobs = [:]
                            def linuxJobs = [:]

                            stage('Scanning Tox Environments'){
                                parallel(
                                    'Linux':{
                                        linuxJobs = getToxTestsParallel(
                                                envNamePrefix: 'Tox Linux',
                                                label: 'linux && docker && x86',
                                                dockerfile: 'ci/docker/python/linux/tox/Dockerfile',
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                                dockerRunArgs: '-v pipcache_packagevalidate:/.cache/pip',
                                                retry: 2
                                            )
                                    },
                                    'Windows':{
                                        windowsJobs = getToxTestsParallel(
                                                envNamePrefix: 'Tox Windows',
                                                label: 'windows && docker && x86',
                                                dockerfile: 'ci/docker/python/windows/tox/Dockerfile',
                                                dockerArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE --build-arg PIP_DOWNLOAD_CACHE=c:/users/containeradministrator/appdata/local/pip',
                                                dockerRunArgs: '-v pipcache_packagevalidate:c:/users/containeradministrator/appdata/local/pip',
                                                retry: 2
                                            )
                                    },
                                    failFast: true
                                )
                            }
                            stage('Running Tox'){
                                parallel(windowsJobs + linuxJobs)
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
                    equals expected: true, actual: params.DEPLOY_DEVPI
                    equals expected: true, actual: params.DEPLOY_DEVPI_PRODUCTION
                }
                beforeAgent true
            }
            stages{
                stage('Source and Wheel formats'){
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
        stage('Deploying to DevPi') {
            when {
                allOf{
                    anyOf{
                        equals expected: true, actual: params.DEPLOY_DEVPI
                    }
                    anyOf {
                        equals expected: 'master', actual: env.BRANCH_NAME
                        equals expected: 'dev', actual: env.BRANCH_NAME
                    }
                }
                beforeAgent true
            }
            agent none
            options{
                lock('dcc_qc-devpi')
            }
            stages{
                stage('Deploy to Devpi Staging') {
                    agent {
                        dockerfile {
                            filename 'ci/docker/python/linux/tox/Dockerfile'
                            label 'linux && docker && devpi-access'
                            additionalBuildArgs '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip'
                          }
                    }
                    steps {
                        unstash 'DOCS_ARCHIVE'
                        unstash 'PYTHON_PACKAGES'
                        script{
                            load('ci/jenkins/scripts/devpi.groovy').upload(
                                    server: DEVPI_CONFIG.server,
                                    credentialsId: DEVPI_CONFIG.credentialsId,
                                    index: getDevPiStagingIndex(),
                                    clientDir: './devpi'
                                )
                        }
                    }
                }
                stage('Test DevPi packages') {
                    steps{
                        script{
                            def devpi
                            node(){
                                checkout scm
                                devpi = load('ci/jenkins/scripts/devpi.groovy')
                            }
                            def macPackages = [:]
                            SUPPORTED_MAC_VERSIONS.each{pythonVersion ->
                                def macArchitectures = []
                                if(params.INCLUDE_MACOS_X86_64 == true){
                                    macArchitectures.add('x86_64')
                                }
                                if(params.INCLUDE_MACOS_ARM == true){
                                    macArchitectures.add('m1')
                                }
                                macArchitectures.each{ processorArchitecture ->
                                    if (nodesByLabel("mac && ${processorArchitecture} && python${pythonVersion}").size() > 0){
                                        macPackages["Mac ${processorArchitecture} - Python ${pythonVersion}: wheel"] = {
                                            withEnv(['PATH+EXTRA=./venv/bin']) {
                                                devpi.testDevpiPackage(
                                                    agent: [
                                                        label: "mac && python${pythonVersion} && devpi-access"
                                                    ],
                                                    devpi: [
                                                        index: DEVPI_CONFIG.stagingIndex,
                                                        server: DEVPI_CONFIG.server,
                                                        credentialsId: DEVPI_CONFIG.credentialsId,
                                                        devpiExec: 'venv/bin/devpi'
                                                    ],
                                                    package:[
                                                        name: props.Name,
                                                        version: props.Version,
                                                        selector: 'whl',
                                                    ],
                                                    test:[
                                                        setup: {
                                                            checkout scm
                                                            sh(
                                                                label:'Installing Devpi client',
                                                                script: '''python3 -m venv venv
                                                                           venv/bin/python -m pip install pip --upgrade
                                                                           venv/bin/python -m pip install 'devpi-client<7.0' -r requirements/requirements_tox.txt
                                                                        '''
                                                            )
                                                        },
                                                        toxEnv: "py${pythonVersion}".replace('.',''),
                                                        teardown: {
                                                            sh( label: 'Remove Devpi client', script: 'rm -r venv')
                                                        }
                                                    ]
                                                )
                                            }
                                        }
                                        macPackages["Mac ${processorArchitecture} - Python ${pythonVersion}: sdist"]= {
                                            withEnv(['PATH+EXTRA=./venv/bin']) {
                                                devpi.testDevpiPackage(
                                                    agent: [
                                                        label: "mac && python${pythonVersion}"
                                                    ],
                                                    devpi: [
                                                        index: DEVPI_CONFIG.stagingIndex,
                                                        server: DEVPI_CONFIG.server,
                                                        credentialsId: DEVPI_CONFIG.credentialsId,
                                                        devpiExec: 'venv/bin/devpi'
                                                    ],
                                                    package:[
                                                        name: props.Name,
                                                        version: props.Version,
                                                        selector: 'tar.gz'
                                                    ],
                                                    test:[
                                                        setup: {
                                                            checkout scm
                                                            sh(
                                                                label:'Installing Devpi client',
                                                                script: '''python3 -m venv venv
                                                                           venv/bin/python -m pip install pip --upgrade
                                                                           venv/bin/python -m pip install 'devpi-client<7.0' -r requirements/requirements_tox.txt
                                                                        '''
                                                            )
                                                        },
                                                        toxEnv: "py${pythonVersion}".replace('.',''),
                                                        teardown: {
                                                            sh( label: 'Remove Devpi client', script: 'rm -r venv')
                                                        }
                                                    ]
                                                )
                                            }
                                        }
                                    }
                                }
                            }
                            def windowsPackages = [:]
                            if(params.INCLUDE_WINDOWS_X86_64 == true){
                                SUPPORTED_WINDOWS_VERSIONS.each{pythonVersion ->
                                    windowsPackages["Windows - Python ${pythonVersion}: sdist"] = {
                                        devpi.testDevpiPackage(
                                            agent: [
                                                dockerfile: [
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE --build-arg PIP_DOWNLOAD_CACHE=c:/users/containeradministrator/appdata/local/pip',
                                                    args: '-v pipcache_packagevalidate:c:/users/containeradministrator/appdata/local/pip',
                                                    label: 'windows && docker && x86'
                                                ]
                                            ],
                                            dockerImageName:  "${currentBuild.fullProjectName}".replaceAll('-', '_').replaceAll('/', '_').replaceAll(' ', '').toLowerCase(),
                                            devpi: [
                                                index: DEVPI_CONFIG.stagingIndex,
                                                server: DEVPI_CONFIG.server,
                                                credentialsId: DEVPI_CONFIG.credentialsId,
                                            ],
                                            package:[
                                                name: props.Name,
                                                version: props.Version,
                                                selector: 'tar.gz'
                                            ],
                                            test:[
                                                toxEnv: "py${pythonVersion}".replace('.',''),
                                            ]
                                        )
                                    }
                                    windowsPackages["Windows - Python ${pythonVersion}: wheel"] = {
                                        devpi.testDevpiPackage(
                                            agent: [
                                                dockerfile: [
                                                    filename: 'ci/docker/python/windows/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg CHOCOLATEY_SOURCE --build-arg PIP_DOWNLOAD_CACHE=c:/users/containeradministrator/appdata/local/pip',
                                                    args: '-v pipcache_packagevalidate:c:/users/containeradministrator/appdata/local/pip',
                                                    label: 'windows && docker && x86 && devpi-access'
                                                ]
                                            ],
                                            devpi: [
                                                index: DEVPI_CONFIG.stagingIndex,
                                                server: DEVPI_CONFIG.server,
                                                credentialsId: DEVPI_CONFIG.credentialsId,
                                            ],
                                            dockerImageName:  "${currentBuild.fullProjectName}_devpi".replaceAll('-', '_').replaceAll('/', '_').replaceAll(' ', '').toLowerCase(),
                                            package:[
                                                name: props.Name,
                                                version: props.Version,
                                                selector: 'whl'
                                            ],
                                            test:[
                                                toxEnv: "py${pythonVersion}".replace('.',''),
                                            ]
                                        )
                                    }
                                }
                            }
                            def linuxPackages = [:]
                            SUPPORTED_LINUX_VERSIONS.each{pythonVersion ->
                                if(params.INCLUDE_LINUX_X86_64 == true){
                                    linuxPackages["Linux x86_64 - Python ${pythonVersion}: sdist"] = {
                                        devpi.testDevpiPackage(
                                            agent: [
                                                dockerfile: [
                                                    filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                                    args: '-v pipcache_packagevalidate:/.cache/pip',
                                                    label: 'linux && docker && x86_64 && devpi-access'
                                                ]
                                            ],
                                            devpi: [
                                                index: DEVPI_CONFIG.stagingIndex,
                                                server: DEVPI_CONFIG.server,
                                                credentialsId: DEVPI_CONFIG.credentialsId,
                                            ],
                                            package:[
                                                name: props.Name,
                                                version: props.Version,
                                                selector: 'tar.gz'
                                            ],
                                            test:[
                                                toxEnv: "py${pythonVersion}".replace('.',''),
                                            ]
                                        )
                                    }
                                    linuxPackages["Linux x86_64 - Python ${pythonVersion}: wheel"] = {
                                        devpi.testDevpiPackage(
                                            agent: [
                                                dockerfile: [
                                                    filename: 'ci/docker/python/linux/tox/Dockerfile',
                                                    additionalBuildArgs: '--build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip',
                                                    args: '-v pipcache_packagevalidate:/.cache/pip',
                                                    label: 'linux && docker && x86_64 && devpi-access'
                                                ]
                                            ],
                                            devpi: [
                                                index: DEVPI_CONFIG.stagingIndex,
                                                server: DEVPI_CONFIG.server,
                                                credentialsId: DEVPI_CONFIG.credentialsId,
                                            ],
                                            package:[
                                                name: props.Name,
                                                version: props.Version,
                                                selector: 'whl'
                                            ],
                                            test:[
                                                toxEnv: "py${pythonVersion}".replace('.',''),
                                            ]
                                        )
                                    }
                                }
                            }
                            parallel(windowsPackages + linuxPackages + macPackages)
                        }
                    }
                }
            }
            post{
                success{
                    node('linux && docker && devpi-access') {
                        script{
                            if (!env.TAG_NAME?.trim()){
                                checkout scm
                                def dockerImage = docker.build('dcc_qc:devpi','-f ./ci/docker/python/linux/tox/Dockerfile --build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip .')
                                dockerImage.inside{
                                    load('ci/jenkins/scripts/devpi.groovy').pushPackageToIndex(
                                        pkgName: props.Name,
                                        pkgVersion: props.Version,
                                        server: DEVPI_CONFIG.server,
                                        credentialsId: DEVPI_CONFIG.credentialsId,
                                        indexSource: "DS_Jenkins/${getDevPiStagingIndex()}",
                                        indexDestination: "DS_Jenkins/${env.BRANCH_NAME}",
                                    )
                                }
                                sh script: "docker image rm --no-prune ${dockerImage.imageName()}"
                            }
                        }
                    }
                }
                cleanup{
                    node('linux && docker && devpi-access') {
                        script{
                            checkout scm
                            def dockerImage = docker.build('dcc_qc:devpi','-f ./ci/docker/python/linux/tox/Dockerfile --build-arg PIP_EXTRA_INDEX_URL --build-arg PIP_INDEX_URL --build-arg PIP_DOWNLOAD_CACHE=/.cache/pip .')
                            dockerImage.inside{
                                load('ci/jenkins/scripts/devpi.groovy').removePackage(
                                    pkgName: props.Name,
                                    pkgVersion: props.Version,
                                    index: "DS_Jenkins/${getDevPiStagingIndex()}",
                                    server: DEVPI_CONFIG.server,
                                    credentialsId: DEVPI_CONFIG.credentialsId,
                                )
                            }
                            sh script: "docker image rm --no-prune ${dockerImage.imageName()}"
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
