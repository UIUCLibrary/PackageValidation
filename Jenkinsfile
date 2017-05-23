#!/usr/bin/env groovy
pipeline{
  agent any

  stages {
    stage("Cloning source") {
      agent any

      steps{
        echo "Cloning source"
        stash includes: "**", name: "source", useDefaultExclusives: false
      }
    }
  }
}
