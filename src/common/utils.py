import datetime
import uuid

from models import Task, UserTask

def generate_update_diff(model, update_data: dict):
    diff = {}
    for key, after in update_data.items():
        before = getattr(model, key, None)
        if before != after:
            diff[key] = {"before": before, "after": after}
    return diff


def create_user_tasks(task_data: Task, user_id: str) -> list[UserTask]:
    if task_data.recurrence_interval is not None:
        start_time = task_data.start_time
        end_time = task_data.end_time
        return [
            UserTask(
                id=uuid.uuid4().hex,
                uid=user_id,
                task=task_data.id,
                status="ONGOING",
                start_time=start_time + datetime.timedelta(days=i * task_data.recurrence_interval),
                end_time=end_time + datetime.timedelta(days=i * task_data.recurrence_interval),
            )
            for i in range(365)
        ]
    return [
        UserTask(
            id=uuid.uuid4().hex,
            uid=user_id,
            task=task_data.id,
            status="ONGOING",
            start_time=task_data.start_time,
            end_time=task_data.end_time,
        )
    ]
