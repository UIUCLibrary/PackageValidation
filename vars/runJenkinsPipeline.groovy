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
                                image 'python'
                                label 'docker && linux && x86_64'
                                args '--mount source=python-tmp-packageValidation,target=/tmp'
                            }
                        }
                        environment{
                            PIP_CACHE_DIR='/tmp/pipcache'
                            UV_INDEX_STRATEGY='unsafe-best-match'
                            UV_TOOL_DIR='/tmp/uvtools'
                            UV_PYTHON_INSTALL_DIR='/tmp/uvpython'
                            UV_CACHE_DIR='/tmp/uvcache'
                        }
                        steps {
                            sh (
                                label: "Building docs on ${env.NODE_NAME}",
                                script: '''python3 -m venv venv
                                           venv/bin/pip install uv
                                           trap "rm -rf venv" EXIT
                                           . ./venv/bin/activate
                                           mkdir -p logs
                                           uvx --python 3.12 --from sphinx --with-editable . --with-requirements requirements-ci.txt sphinx-build docs/source build/docs/html -d build/docs/.doctrees -v -w logs/build_sphinx.log
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
                                    def props = readTOML( file: 'pyproject.toml')['project']
                                    def DOC_ZIP_FILENAME = "${props.name}-${props.version}.doc.zip"
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
                                    docker{
                                        image 'python'
                                        label 'docker && linux && x86_64'
                                        args '--mount source=python-tmp-packageValidation,target=/tmp'
                                    }
                                }
                                environment{
                                    PIP_CACHE_DIR='/tmp/pipcache'
                                    UV_INDEX_STRATEGY='unsafe-best-match'
                                    UV_TOOL_DIR='/tmp/uvtools'
                                    UV_PYTHON_INSTALL_DIR='/tmp/uvpython'
                                    UV_CACHE_DIR='/tmp/uvcache'
                                }
                                stages{
                                    stage('Setup Testing Environment'){
                                        steps{
                                            sh(
                                                label: 'Create virtual environment',
                                                script: '''python3 -m venv bootstrap_uv
                                                           bootstrap_uv/bin/pip install uv
                                                           bootstrap_uv/bin/uv venv --python 3.12 venv
                                                           . ./venv/bin/activate
                                                           bootstrap_uv/bin/uv pip install uv
                                                           rm -rf bootstrap_uv
                                                           uv pip install -r requirements-ci.txt
                                                           '''
                                                       )
                                            sh(
                                                label: 'Install package in development mode',
                                                script: '''. ./venv/bin/activate
                                                           uv pip install -e .
                                                        '''
                                                )
                                        }
                                    }
                                    stage('Run Tests'){
                                        parallel {
                                            stage('PyTest'){
                                                steps{
                                                    sh '''. ./venv/bin/activate
                                                          coverage run --parallel-mode --source=dcc_qc -m pytest --junitxml=reports/junit-pytest.xml
                                                       '''
                                                }
                                                post {
                                                    always{
                                                        junit 'reports/junit-pytest.xml'
                                                    }
                                                }
                                            }
                                            stage('Documentation'){
                                                steps{
                                                        sh '''. ./venv/bin/activate
                                                              mkdir -p logs
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
                                                            sh '''. ./venv/bin/activate
                                                                  mypy -p dcc_qc --html-report reports/mypy_html
                                                               '''
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
                                                        sh '''. ./venv/bin/activate
                                                              mkdir -p logs
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
                                                sh '''. ./venv/bin/activate
                                                      coverage combine
                                                      coverage xml -o reports/coverage.xml
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
                                     UV_INDEX_STRATEGY='unsafe-best-match'
                                     UV_TOOL_DIR='/tmp/uvtools'
                                     UV_PYTHON_INSTALL_DIR='/tmp/uvpython'
                                     UV_CACHE_DIR='/tmp/uvcache'
                                 }
                                 steps{
                                     script{
                                         def envs = []
                                         node('docker && linux'){
                                             docker.image('python').inside('--mount source=python-tmp-packageValidation,target=/tmp'){
                                                 try{
                                                     checkout scm
                                                     sh(script: 'python3 -m venv venv && venv/bin/pip install uv')
                                                     envs = sh(
                                                         label: 'Get tox environments',
                                                         script: './venv/bin/uvx --quiet --with tox-uv tox list -d --no-desc',
                                                         returnStdout: true,
                                                     ).trim().split('\n')
                                                 } finally{
                                                     cleanWs(
                                                         patterns: [
                                                             [pattern: 'venv/', type: 'INCLUDE'],
                                                             [pattern: '.tox', type: 'INCLUDE'],
                                                             [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                         ]
                                                     )
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
                                                             docker.image('python').inside('--mount source=python-tmp-packageValidation,target=/tmp'){
                                                                 checkout scm
                                                                 try{
                                                                     sh( label: 'Running Tox',
                                                                         script: """python3 -m venv venv && venv/bin/pip install uv
                                                                                    . ./venv/bin/activate
                                                                                    uv python install cpython-${version}
                                                                                    uvx -p ${version} --with tox-uv tox run -e ${toxEnv}
                                                                                 """
                                                                         )
                                                                 } catch(e) {
                                                                     sh(script: '''. ./venv/bin/activate
                                                                           uv python list
                                                                           '''
                                                                             )
                                                                     throw e
                                                                 } finally{
                                                                     cleanWs(
                                                                         patterns: [
                                                                             [pattern: 'venv/', type: 'INCLUDE'],
                                                                             [pattern: '.tox', type: 'INCLUDE'],
                                                                             [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                                         ]
                                                                     )
                                                                 }
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
                                    UV_INDEX_STRATEGY='unsafe-best-match'
                                    PIP_CACHE_DIR='C:\\Users\\ContainerUser\\Documents\\pipcache'
                                    UV_TOOL_DIR='C:\\Users\\ContainerUser\\Documents\\uvtools'
                                    UV_PYTHON_INSTALL_DIR='C:\\Users\\ContainerUser\\Documents\\uvpython'
                                    UV_CACHE_DIR='C:\\Users\\ContainerUser\\Documents\\uvcache'
                                }
                                steps{
                                    script{
                                        def envs = []
                                        node('docker && windows'){
                                            docker.image('python').inside('--mount source=python-tmp-packageValidation,target=C:\\Users\\ContainerUser\\Documents'){
                                                try{
                                                    checkout scm
                                                    bat(script: 'python -m venv venv && venv\\Scripts\\pip install uv')
                                                    envs = bat(
                                                        label: 'Get tox environments',
                                                        script: '@.\\venv\\Scripts\\uvx --quiet --with tox-uv tox list -d --no-desc',
                                                        returnStdout: true,
                                                    ).trim().split('\r\n')
                                                } finally{
                                                    cleanWs(
                                                        patterns: [
                                                            [pattern: 'venv/', type: 'INCLUDE'],
                                                            [pattern: '.tox', type: 'INCLUDE'],
                                                            [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                        ]
                                                    )
                                                }
                                            }
                                        }
                                        parallel(
                                            envs.collectEntries{toxEnv ->
                                                def version = toxEnv.replaceAll(/py(\d)(\d+)/, '$1.$2')
                                                [
                                                    "Tox Environment: ${toxEnv}",
                                                    {
                                                        node('docker && windows'){
                                                            docker.image('python').inside('--mount source=python-tmp-packageValidation,target=C:\\Users\\ContainerUser\\Documents'){
                                                                checkout scm
                                                                try{
                                                                    bat(label: 'Install uv',
                                                                        script: 'python -m venv venv && venv\\Scripts\\pip install uv'
                                                                    )
                                                                    retry(3){
                                                                        bat(label: 'Running Tox',
                                                                            script: """call venv\\Scripts\\activate.bat
                                                                                   uv python install cpython-${version}
                                                                                   uvx -p ${version} --with tox-uv tox run -e ${toxEnv}
                                                                                """
                                                                        )
                                                                    }
                                                                } finally{
                                                                    cleanWs(
                                                                        patterns: [
                                                                            [pattern: 'venv/', type: 'INCLUDE'],
                                                                            [pattern: '.tox', type: 'INCLUDE'],
                                                                            [pattern: '**/__pycache__/', type: 'INCLUDE'],
                                                                        ]
                                                                    )
                                                                }
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
                                image 'python'
                                label 'linux && docker'
                                args '--mount source=python-tmp-packageValidation,target=/tmp'
                            }
                        }
                        environment{
                            PIP_CACHE_DIR='/tmp/pipcache'
                            UV_INDEX_STRATEGY='unsafe-best-match'
                            UV_CACHE_DIR='/tmp/uvcache'
                        }
                        options {
                            retry(2)
                        }
                        steps{
                            timeout(5){
                                sh(
                                    label: 'Package',
                                    script: '''python3 -m venv venv && venv/bin/pip install uv
                                               trap "rm -rf venv" EXIT
                                               . ./venv/bin/activate
                                               uv build
                                            '''
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
                        environment{
                            UV_INDEX_STRATEGY='unsafe-best-match'
                        }
                        steps{
                            customMatrix(
                                axes: [
                                    [
                                        name: 'PYTHON_VERSION',
                                        values: ['3.9', '3.10', '3.11', '3.12','3.13']
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
                                                        docker.image('python').inside(isUnix() ? '': "--mount type=volume,source=uv_python_install_dir,target=C:\\Users\\ContainerUser\\Documents\\uvpython"){
                                                             if(isUnix()){
                                                                withEnv([
                                                                    'PIP_CACHE_DIR=/tmp/pipcache',
                                                                    'UV_TOOL_DIR=/tmp/uvtools',
                                                                    'UV_PYTHON_INSTALL_DIR=/tmp/uvpython',
                                                                    'UV_CACHE_DIR=/tmp/uvcache',
                                                                ]){
                                                                     sh(
                                                                        label: 'Testing with tox',
                                                                        script: """python3 -m venv venv
                                                                                   ./venv/bin/pip install --disable-pip-version-check uv
                                                                                   ./venv/bin/uv python install cpython-${entry.PYTHON_VERSION}
                                                                                   ./venv/bin/uvx --with tox-uv tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                                """
                                                                    )
                                                                }
                                                             } else {
                                                                withEnv([
                                                                    'PIP_CACHE_DIR=C:\\Users\\ContainerUser\\Documents\\pipcache',
                                                                    'UV_TOOL_DIR=C:\\Users\\ContainerUser\\Documents\\uvtools',
                                                                    'UV_PYTHON_INSTALL_DIR=C:\\Users\\ContainerUser\\Documents\\uvpython',
                                                                    'UV_CACHE_DIR=C:\\Users\\ContainerUser\\Documents\\uvcache',
                                                                ]){
                                                                    bat(
                                                                        label: 'Testing with tox',
                                                                        script: """python -m venv venv
                                                                                   .\\venv\\Scripts\\pip install --disable-pip-version-check uv
                                                                                   .\\venv\\Scripts\\uv python install cpython-${entry.PYTHON_VERSION}
                                                                                   .\\venv\\Scripts\\uvx --with tox-uv tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                                """
                                                                    )
                                                                }
                                                             }
                                                        }
                                                    } else {
                                                        if(isUnix()){
                                                            sh(
                                                                label: 'Testing with tox',
                                                                script: """python3 -m venv venv
                                                                           ./venv/bin/pip install --disable-pip-version-check uv
                                                                           ./venv/bin/uvx --with tox-uv tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                        """
                                                            )
                                                        } else {
                                                            bat(
                                                                label: 'Testing with tox',
                                                                script: """python -m venv venv
                                                                           .\\venv\\Scripts\\pip install --disable-pip-version-check uv
                                                                           .\\venv\\Scripts\\uv python install cpython-${entry.PYTHON_VERSION}
                                                                           .\\venv\\Scripts\\uvx --with tox-uv tox --installpkg ${findFiles(glob: entry.PACKAGE_TYPE == 'wheel' ? 'dist/*.whl' : 'dist/*.tar.gz')[0].path} -e py${entry.PYTHON_VERSION.replace('.', '')}
                                                                        """
                                                            )
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
                    UV_INDEX_STRATEGY='unsafe-best-match'
                    UV_TOOL_DIR='/tmp/uvtools'
                    UV_PYTHON_INSTALL_DIR='/tmp/uvpython'
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