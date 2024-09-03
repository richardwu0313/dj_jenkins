from enum import Enum


class Timeout:
    XXLong = 60000
    XLong = 9999
    Long = 6000
    Medium = 3000
    Short = 600
    XShort = 180


class JenkinsType(Enum):
    FOLDER = "com.cloudbees.hudson.plugins.folder.Folder"
    JOB = "hudson.model.FreeStyleProject"
    JOB_BUILD = "hudson.model.FreeStyleBUILD"
    PIPELINE = "org.jenkinsci.plugins.workflow.job.WorkflowJob"
    PIPELINE_BUILD = "org.jenkinsci.plugins.workflow.job.WorkflowRun"
    VIEW = "hudson.model.AllView"


class JenkinsResultType(Enum):
    SUCCESS = "SUCCESS"
    UNSTABLE = "UNSTABLE"
    FAILURE = "FAILURE"
    ABORTED = "ABORTED"
    NOT_BUILT = "NOT_BUILT"
