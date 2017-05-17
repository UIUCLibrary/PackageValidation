import pytest

from dcc_qc import tasks
from dcc_qc import task_manager
from dcc_qc import task_states


@pytest.fixture
def task_fixture():
    return tasks.Task(name="dummy task")


@pytest.fixture
def my_task_manager():
    return task_manager.TaskManager()


def test_manage_empty_size(my_task_manager):
    assert len(my_task_manager) == 0


def test_task2_name(task_fixture):
    assert task_fixture.name == "dummy task"


def test_task2_empty(task_fixture):
    assert len(task_fixture) == 0
    assert task_fixture.status == task_states.TaskStatus.EMPTY


def test_task2_add_to_empty(task_fixture):
    task_fixture.add_process("DUMMY")
    assert len(task_fixture) == 1
    assert task_fixture.status == task_states.TaskStatus.QUEUED
    task_fixture.add_process("DUMMY2")
    assert len(task_fixture) == 2
    assert task_fixture.status == task_states.TaskStatus.QUEUED


def test_task2_reset_from_queued_state(task_fixture):
    task_fixture.add_process("DUMMY")
    task_fixture.add_process("DUMMY2")
    task_fixture.reset()
    assert len(task_fixture) == 0
    assert task_fixture.status == task_states.TaskStatus.EMPTY
