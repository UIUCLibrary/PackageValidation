def createUVConfig(){
    if(isUnix()){
        def scriptFile = 'ci/scripts/create_uv_config.sh'
        if(! fileExists(scriptFile)){
            checkout scm
        }
        return sh(label: 'Setting up uv.toml config file', script: "sh ${scriptFile} " + '$UV_INDEX_URL $UV_EXTRA_INDEX_URL', returnStdout: true).trim()
    } else {
        def scriptFile = "ci\\scripts\\new-uv-global-config.ps1"
        if(! fileExists(scriptFile)){
            checkout scm
        }
        return powershell(
            label: 'Setting up uv.toml config file',
            script: "& ${scriptFile} \$env:UV_INDEX_URL \$env:UV_EXTRA_INDEX_URL",
            returnStdout: true
        ).trim()
    }
}


def call(){
    library(
        identifier: 'JenkinsPythonHelperLibrary@2024.12.0',
        retriever: modernSCM(
            [
                $class: 'GitSCMSource',
                remote: 'https://github.com/UIUCLibrary/JenkinsPythonHelperLibrary.git'
            ]
        )
    )
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
            booleanParam(name: 'INCLUDE_LINUX-ARM64', defaultValue: false, description: 'Include ARM architecture for Linux')
            booleanParam(name: 'INCLUDE_LINUX-X86_64', defaultValue: true, description: 'Include x86_64 architecture for Linux')
            booleanParam(name: 'INCLUDE_MACOS-ARM64', defaultValue: false, description: 'Include ARM(m1) architecture for Mac')
            booleanParam(name: 'INCLUDE_MACOS-X86_64', defaultValue: false, description: 'Include x86_64 architecture for Mac')
            booleanParam(name: 'INCLUDE_WINDOWS-X86_64', defaultValue: true, description: 'Include x86_64 architecture for Windows')
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
                            docker{
                                image 'ghcr.io/astral-sh/uv:debian'
                                label 'docker && linux && x86_64'
                                args '--mount source=python-tmp-packageValidation,target=/tmp --tmpfs /venv:exec -e UV_PROJECT_ENVIRONMENT=/venv'
                            }
                        }
                        environment{
                            PIP_CACHE_DIR='/tmp/pipcache'
                            UV_TOOL_DIR='/tmp/uvtools'
                            UV_PYTHON_CACHE_DIR='/tmp/uvpython'
                            UV_CACHE_DIR='/tmp/uvcache'
                            UV_CONFIG_FILE=createUVConfig()
                            UV_FROZEN=1
                        }
                        steps {
                            sh (
                                label: "Building docs on ${env.NODE_NAME}",
                                script: 'uv run --group docs --no-dev sphinx-build docs/source build/docs/html -d build/docs/.doctrees -v -w logs/build_sphinx.log'
                            )
                            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'build/docs/html', reportFiles: 'index.html', reportName: 'Documentation', reportTitles: ''])
                            script{
                                def props = readTOML( file: 'pyproject.toml')['project']
                                def DOC_ZIP_FILENAME = "${props.name}-${props.version}.doc.zip"
                                zip archive: true, dir: 'build/docs/html', glob: '', zipFile: "dist/${DOC_ZIP_FILENAME}"
                            }
                            stash includes: 'build/docs/html/**,dist/*.doc.zip', name: 'DOCS_ARCHIVE'
                        }
                        post{
                            always {
                                recordIssues(tools: [sphinxBuild(name: 'Sphinx Documentation Build', pattern: 'logs/build_sphinx.log', id: 'sphinx_build')])
                                archiveArtifacts artifacts: 'logs/build_sphinx.log'
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
                                    docker{
                                        image 'ghcr.io/astral-sh/uv:debian'
                                        label 'docker && linux && x86_64'
                                        args '--mount source=python-tmp-packageValidation,target=/tmp --tmpfs /venv:exec -e UV_PROJECT_ENVIRONMENT=/venv'
                                    }
                                }
                                environment{
                                    PIP_CACHE_DIR='/tmp/pipcache'
                                    UV_TOOL_DIR='/tmp/uvtools'
                                    UV_PYTHON_CACHE_DIR='/tmp/uvpython'
                                    UV_CACHE_DIR='/tmp/uvcache'
                                    UV_CONFIG_FILE=createUVConfig()
                                    UV_FROZEN=1
                                }
                                stages{
                                    stage('Setup Testing Environment'){
                                        steps{
                                            sh(
                                                label: 'Create virtual environment with packaging in development mode',
                                                script: 'uv sync --frozen --group ci'
                                           )
                                        }
                                    }
                                    stage('Run Tests'){
                                        parallel {
                                            stage('PyTest'){
                                                steps{
                                                    sh 'uv run coverage run --parallel-mode --source=src -m pytest --junitxml=reports/junit-pytest.xml'
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
                                                              uv run -m sphinx -b doctest docs/source build/docs -d build/docs/doctrees -v -w logs/doctest.log --no-color
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
                                                    recordIssues(tools: [taskScanner(highTags: 'FIXME', includePattern: 'src/**/*.py', normalTags: 'TODO')])
                                                }
                                            }
                                            stage('Audit Lockfile Dependencies'){
                                                steps{
                                                    catchError(buildResult: 'UNSTABLE', message: 'uv-secure found issues', stageResult: 'UNSTABLE') {
                                                        sh 'uv run uv-secure --disable-cache uv.lock'
                                                    }
                                                }
                                            }
                                            stage('MyPy'){
                                                steps{
                                                    catchError(buildResult: 'SUCCESS', message: 'MyPy found issues', stageResult: 'UNSTABLE') {
                                                        tee('logs/mypy.log'){
                                                            sh 'uv run mypy -p dcc_qc --html-report reports/mypy_html'
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
                                                              uv run flake8 src --format=pylint --tee --output-file=logs/flake8.log
                                                           '''
                                                    }
                                                }
                                                post {
                                                    always {
                                                        recordIssues(tools: [flake8(name: 'Flake8', pattern: 'logs/flake8.log')])
                                                    }
                                                }
                                            }
                                        }
                                        post{
                                            always{
                                                sh '''uv run coverage combine
                                                      uv run coverage xml -o reports/coverage.xml
                                                   '''
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
                                 environment{
                                     PIP_CACHE_DIR='/tmp/pipcache'
                                     UV_TOOL_DIR='/tmp/uvtools'
                                     UV_PYTHON_CACHE_DIR='/tmp/uvpython'
                                     UV_CACHE_DIR='/tmp/uvcache'
                                 }
                                 steps{
                                     script{
                                         def envs = []
                                         retry(2){
                                             node('docker && linux'){
                                                 checkout scm
                                                 try{
                                                     docker.image('ghcr.io/astral-sh/uv:debian').inside('--mount source=python-tmp-packageValidation,target=/tmp --tmpfs /ci_tmp:exec -e TOX_WORK_DIR=/ci_tmp/tox'){
                                                        withEnv(["UV_CONFIG_FILE=${createUVConfig()}"]){
                                                            retry(2){
                                                                try{
                                                                    envs = sh(
                                                                         label: 'Get tox environments',
                                                                         script: 'uv run --only-group=tox --isolated --frozen --quiet tox list -d --no-desc',
                                                                         returnStdout: true,
                                                                    ).trim().split('\n')
                                                                } catch (e){
                                                                    cleanWs(
                                                                        patterns: [
                                                                            [pattern: 'venv/', type: 'INCLUDE'],
                                                                            [pattern: '.tox', type: 'INCLUDE'],
                                                                            [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                                        ]
                                                                    )
                                                                    throw e
                                                                }
                                                            }
                                                        }
                                                    }
                                                 } finally {
                                                    sh "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                 }
                                             }
                                         }
                                         parallel(
                                             envs.collectEntries{toxEnv ->
                                                 def version = toxEnv.replaceAll(/py(\d)(\d+)/, '$1.$2')
                                                 [
                                                     "Tox Environment: ${toxEnv}",
                                                     {
                                                         node('docker && linux'){
                                                            checkout scm
                                                            try{
                                                                docker.image('ghcr.io/astral-sh/uv:debian').inside('--mount source=python-tmp-packageValidation,target=/tmp --tmpfs /.local/share:exec --tmpfs /.local/bin:exec --tmpfs /ci_tmp:exec -e TOX_WORK_DIR=/ci_tmp/tox -e UV_PROJECT_ENVIRONMENT=/ci_tmp/venv'){
                                                                    withEnv(["UV_CONFIG_FILE=${createUVConfig()}"]){
                                                                        try{
                                                                            sh( label: 'Running Tox',
                                                                                script: """uv python install cpython-${version}
                                                                                           uv run --only-group=tox-uv tox run --runner uv-venv-lock-runner -e ${toxEnv}
                                                                                        """
                                                                             )
                                                                        } catch(e) {
                                                                            cleanWs(
                                                                                patterns: [
                                                                                    [pattern: 'venv/', type: 'INCLUDE'],
                                                                                    [pattern: '.tox', type: 'INCLUDE'],
                                                                                    [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                                                ]
                                                                            )
                                                                            throw e
                                                                        }
                                                                    }
                                                                }
                                                            } finally{
                                                                sh "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                            }
                                                         }
                                                     }
                                                 ]
                                             }
                                         )
                                     }
                                 }
                             }
                            stage('Windows'){
                                when{
                                    expression {return nodesByLabel('windows && docker && x86').size() > 0}
                                }
                                environment{
                                    PIP_CACHE_DIR='C:\\Users\\ContainerUser\\Documents\\pipcache'
                                    UV_TOOL_DIR='C:\\Users\\ContainerUser\\Documents\\uvtools'
                                    UV_PYTHON_CACHE_DIR='C:\\Users\\ContainerUser\\Documents\\uvpython'
                                    UV_CACHE_DIR='C:\\Users\\ContainerUser\\Documents\\uvcache'
                                }
                                steps{
                                    script{
                                        def envs = []
                                        node('docker && windows'){
                                            checkout scm
                                            try{
                                                docker.image(
                                                    env.DEFAULT_PYTHON_DOCKER_IMAGE ? env.DEFAULT_PYTHON_DOCKER_IMAGE: 'python'
                                                ).inside(
                                                    "--mount type=volume,source=uv_python_cache_dir,target=${env.UV_PYTHON_CACHE_DIR}"
                                                    + " --mount type=volume,source=uv_cache_dir,target=${env.UV_CACHE_DIR}"

                                                ){
                                                    withEnv(["UV_CONFIG_FILE=${createUVConfig()}"]){
                                                        bat(script: 'python -m venv venv && venv\\Scripts\\pip install --disable-pip-version-check uv')
                                                        envs = bat(
                                                            label: 'Get tox environments',
                                                            script: '@.\\venv\\Scripts\\uv run --only-group=tox --isolated --frozen --quiet tox list -d --no-desc',
                                                            returnStdout: true,
                                                        ).trim().split('\r\n')
                                                    }
                                                }
                                            } finally{
                                                bat "${tool(name: 'Default', type: 'git')} clean -dfx"
                                            }
                                        }
                                        parallel(
                                            envs.collectEntries{toxEnv ->
                                                def version = toxEnv.replaceAll(/py(\d)(\d+)/, '$1.$2')
                                                [
                                                    "Tox Environment: ${toxEnv}",
                                                    {
                                                        node('docker && windows'){
                                                            checkout scm
                                                            try{
                                                                docker.image(
                                                                    env.DEFAULT_PYTHON_DOCKER_IMAGE ? env.DEFAULT_PYTHON_DOCKER_IMAGE: 'python'
                                                                ).inside(
                                                                    "--mount type=volume,source=uv_python_cache_dir,target=${env.UV_PYTHON_CACHE_DIR}"
                                                                    + " --mount type=volume,source=uv_cache_dir,target=${env.UV_CACHE_DIR}"
                                                                ){
                                                                    withEnv([
                                                                        "TOX_UV_PATH=${WORKSPACE}\\venv\\Scripts\\uv.exe",
                                                                        "UV_CONFIG_FILE=${createUVConfig()}"
                                                                    ]){
                                                                        bat(label: 'Install uv',
                                                                            script: 'python -m venv venv && venv\\Scripts\\pip install --disable-pip-version-check uv'
                                                                        )
                                                                        retry(3){
                                                                            try{
                                                                                bat(label: 'Running Tox',
                                                                                    script: """venv\\Scripts\\uv python install cpython-${version}
                                                                                               venv\\Scripts\\uv run --only-group=tox-uv tox run --runner uv-venv-lock-runner -e ${toxEnv}
                                                                                            """
                                                                                )
                                                                            } catch(e) {
                                                                                cleanWs(
                                                                                    patterns: [
                                                                                        [pattern: '.tox', type: 'INCLUDE'],
                                                                                        [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                                                    ]
                                                                                )
                                                                                throw e
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            } finally {
                                                                bat "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                            }
                                                        }
                                                    }
                                                ]
                                            }
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
                        agent {
                            docker{
                                image 'ghcr.io/astral-sh/uv:debian'
                                label 'linux && docker'
                                args '--mount source=python-tmp-packageValidation,target=/tmp'
                            }
                        }
                        environment{
                            PIP_CACHE_DIR='/tmp/pipcache'
                            UV_CACHE_DIR='/tmp/uvcache'
                        }
                        options {
                            retry(2)
                        }
                        steps{
                            timeout(5){
                                sh(
                                    label: 'Package',
                                    script: 'uv build'
                                )
                            }
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
                    stage('Testing Packages'){
                        when{
                            equals expected: true, actual: params.TEST_PACKAGES
                        }
                        steps{
                            customMatrix(
                                axes: [
                                    [
                                        name: 'PYTHON_VERSION',
                                        values: ['3.10', '3.11', '3.12', '3.13', '3.14', '3.14t']
                                    ],
                                    [
                                        name: 'OS',
                                        values: ['linux','macos','windows']
                                    ],
                                    [
                                        name: 'ARCHITECTURE',
                                        values: ['x86_64', 'arm64']
                                    ],
                                    [
                                        name: 'PACKAGE_TYPE',
                                        values: ['wheel', 'sdist'],
                                    ]
                                ],
                                excludes: [
                                    [
                                        [
                                            name: 'OS',
                                            values: 'windows'
                                        ],
                                        [
                                            name: 'ARCHITECTURE',
                                            values: 'arm64',
                                        ]
                                    ]
                                ],
                                when: {entry -> "INCLUDE_${entry.OS}-${entry.ARCHITECTURE}".toUpperCase() && params["INCLUDE_${entry.OS}-${entry.ARCHITECTURE}".toUpperCase()]},
                                stages: [
                                    { entry ->
                                        stage('Test Package') {
                                            node("${entry.OS} && ${entry.ARCHITECTURE} ${['linux', 'windows'].contains(entry.OS) ? '&& docker': ''}"){
                                                try{
                                                    checkout scm
                                                    unstash 'PYTHON_PACKAGES'
                                                    if(['linux', 'windows'].contains(entry.OS) && params.containsKey("INCLUDE_${entry.OS}-${entry.ARCHITECTURE}".toUpperCase()) && params["INCLUDE_${entry.OS}-${entry.ARCHITECTURE}".toUpperCase()]){
                                                        docker.image(isUnix() ? 'ghcr.io/astral-sh/uv:debian': 'python')
                                                            .inside(
                                                                isUnix() ?
                                                                    '--mount source=python-tmp-packageValidation,target=/tmp' +
                                                                    ' --tmpfs /.local/bin:exec' +
                                                                    ' --tmpfs /.local/share:exec'
                                                                :
                                                                    "--mount type=volume,source=uv_python_cache_dir,target=C:\\Users\\ContainerUser\\Documents\\uvpython" +
                                                                    ' --mount type=volume,source=uv_cache_dir,target=C:\\Users\\ContainerUser\\Documents\\cache\\uvcache'
                                                            ){
                                                             if(isUnix()){
                                                                withEnv([
                                                                    'PIP_CACHE_DIR=/tmp/pipcache',
                                                                    'UV_TOOL_DIR=/tmp/uvtools',
                                                                    'UV_PYTHON_CACHE_DIR=/tmp/uvpython',
                                                                    'UV_CACHE_DIR=/tmp/uvcache',
                                                                    "UV_CONFIG_FILE=${createUVConfig()}",
                                                                ]){
                                                                     sh(
                                                                        label: 'Testing with tox',
                                                                        script: """uv python install cpython-${entry.PYTHON_VERSION}
                                                                                   uv run --only-group=tox-uv --frozen tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                                """
                                                                    )
                                                                }
                                                             } else {
                                                                withEnv([
                                                                    'PIP_CACHE_DIR=C:\\Users\\ContainerUser\\Documents\\pipcache',
                                                                    'UV_TOOL_DIR=C:\\Users\\ContainerUser\\Documents\\uvtools',
                                                                    'UV_PYTHON_CACHE_DIR=C:\\Users\\ContainerUser\\Documents\\uvpython',
                                                                    'UV_CACHE_DIR=C:\\Users\\ContainerUser\\Documents\\uvcache',
                                                                    "UV_CONFIG_FILE=${createUVConfig()}",
                                                                    "TOX_UV_PATH=${WORKSPACE}\\venv\\Scripts\\uv.exe",
                                                                ]){
                                                                    bat(
                                                                        label: 'Testing with tox',
                                                                        script: """python -m venv venv
                                                                                   .\\venv\\Scripts\\pip install --disable-pip-version-check uv
                                                                                   .\\venv\\Scripts\\uv python install cpython-${entry.PYTHON_VERSION}
                                                                                   .\\venv\\Scripts\\uv run --only-group=tox-uv --isolated --frozen tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                                """
                                                                    )
                                                                }
                                                             }
                                                        }
                                                    } else {
                                                        if(isUnix()){
                                                            withEnv([
                                                                "UV_CONFIG_FILE=${createUVConfig()}",
                                                                "TOX_UV_PATH=${WORKSPACE}/venv/bin/uv",
                                                            ]){
                                                                sh(
                                                                    label: 'Testing with tox',
                                                                    script: """python3 -m venv venv
                                                                               ./venv/bin/pip install --disable-pip-version-check uv
                                                                               ./venv/bin/uv run --only-group=tox-uv --isolated --frozen tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                            """
                                                                )
                                                            }
                                                        } else {
                                                            withEnv([
                                                                "UV_CONFIG_FILE=${createUVConfig()}",
                                                                "TOX_UV_PATH=${WORKSPACE}\\venv\\Scripts\\uv.exe",
                                                            ]){
                                                                bat(
                                                                    label: 'Testing with tox',
                                                                    script: """python -m venv venv
                                                                               .\\venv\\Scripts\\pip install --disable-pip-version-check uv
                                                                               .\\venv\\Scripts\\uv python install cpython-${entry.PYTHON_VERSION}
                                                                               .\\venv\\Scripts\\uv run --only-group=tox-uv --isolated --frozen tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                            """
                                                                )
                                                            }
                                                        }
                                                    }
                                                } finally{
                                                    if(isUnix()){
                                                        sh "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                    } else {
                                                        bat "${tool(name: 'Default', type: 'git')} clean -dfx"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                ]
                            )
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
                environment{
                    PIP_CACHE_DIR='/tmp/pipcache'
                    UV_TOOL_DIR='/tmp/uvtools'
                    UV_PYTHON_CACHE_DIR='/tmp/uvpython'
                    UV_CACHE_DIR='/tmp/uvcache'
                }
                agent {
                    docker{
                        image 'python'
                        label 'docker && linux'
                        args '--mount source=python-tmp-packageValidation,target=/tmp'
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
}