pipeline {
    agent any

    triggers {
        // 9am morning
        cron('H 9 * * *')
    }

    options {
        timestamps()
        timeout(time: 24, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '30', artifactNumToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    environment {
        PROJECT_DIR = '/Users/user/Documents/GitHub/local-multi-agent-dev'
        PYTHON      = "${PROJECT_DIR}/venv/bin/python3"
        // Add the Homebrew bin directory so Jenkins can find the `ipsw` CLI
        PATH        = "${PROJECT_DIR}/venv/bin:/opt/homebrew/bin:${env.PATH}"

        PIPELINE_DEVICES         = ''
        PIPELINE_DEVICE_FAMILY   = 'iPhone'
        PIPELINE_KEEP_PER_DEVICE = '1'
    }

    stages {
        stage('Detect new firmware') {
            steps {
                dir("${PROJECT_DIR}") {
                    script {
                        def code = sh(
                            script: "${PYTHON} scripts/automation.py check",
                            returnStatus: true
                        )
                        if (code == 2) {
                            env.NEW_FIRMWARE = 'false'
                            echo 'No new firmware; skipping download, analysis and cleanup.'
                        } else if (code == 0) {
                            env.NEW_FIRMWARE = 'true'
                        } else {
                            error("automation.py check exited with ${code}")
                        }
                    }
                }
            }
        }

        stage('Download firmware') {
            when { environment name: 'NEW_FIRMWARE', value: 'true' }
            steps {
                dir("${PROJECT_DIR}") {
                    // Exit 1 means no devices are available to analyse, so stop the pipeline
                    sh "${PYTHON} scripts/automation.py download"
                }
            }
        }

        stage('Diff and analyse') {
            when { environment name: 'NEW_FIRMWARE', value: 'true' }
            steps {
                dir("${PROJECT_DIR}") {
                    script {
                        def code = sh(
                            script: "${PYTHON} scripts/automation.py analyze",
                            returnStatus: true
                        )
                        env.ANALYSIS_OK = 'true'
                        if (code == 2) {
                            echo 'Baseline recorded; no predecessor to diff against yet.'
                        } else if (code != 0) {
                            // Mark unstable so the job retries next time
                            env.ANALYSIS_OK = 'false'
                            unstable("automation.py analyze exited with ${code}")
                        }
                    }
                }
            }
        }

        // Skipped when the analysis failed
        stage('Prune old IPSWs') {
            when {
                allOf {
                    environment name: 'NEW_FIRMWARE', value: 'true'
                    environment name: 'ANALYSIS_OK', value: 'true'
                }
            }
            steps {
                dir("${PROJECT_DIR}") {
                    sh "${PYTHON} scripts/automation.py cleanup"
                }
            }
        }
    }

    post {
        always {
            dir("${PROJECT_DIR}") {
                // Archive the current run's feature analysis markdown and report.json
                archiveArtifacts(
                    artifacts: '.jenkins_pipeline/*.json, .jenkins_pipeline/reports/**',
                    allowEmptyArchive: true,
                    fingerprint: false
                )
            }
        }
        success {
            echo 'Full analysis output: artifacts/firmware_diff/<run id>/'
        }
        unstable {
            echo 'Some devices failed; they stay uncommitted and retry on the next run.'
            echo 'Pruning was skipped so the predecessor IPSW survives for the retry.'
        }
    }
}