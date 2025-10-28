from enum import Enum

class TaskStatus(Enum):
    EMPTY = "empty"
    QUEUED = "queued"
    WORKING = "working"
    FAILED = "failed"
    SUCCESS = "success"