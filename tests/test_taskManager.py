import pytest
from dcc_qc import task_manager


@pytest.fixture
def my_task():
    return task_manager.Task(name="dummy task")


@pytest.fixture
def my_task_manager():
    return task_manager.TaskManager()


def test_my_task(my_task):
    assert my_task.name == "dummy task"


def test_manage_empty_size(my_task_manager):
    assert len(my_task_manager) == 0
