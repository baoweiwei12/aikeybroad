from typing import Dict
import redis


class RedisClient:
    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def set_task(self, task_id: str, task_data: dict):
        self.client.hset(task_id, mapping=task_data)

    def get_task(self, task_id: str) -> Dict[str, str]:
        task = self.client.hgetall(task_id)
        return {
            key.decode("utf-8"): value.decode("utf-8") for key, value in task.items()  # type: ignore
        }

    def update_task(self, task_id: str, update_data: dict):
        self.client.hset(task_id, mapping=update_data)

    def task_exists(self, task_id: str) -> bool:
        return self.client.exists(task_id)  # type: ignore


redis_client = RedisClient(host="localhost", port=6379, db=0)
