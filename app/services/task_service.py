from app.repositories.task_repository import TaskRepository
from app.services.base import BaseService
from app.utils.logger import logger
from app.utils.http_exceptions import not_found, unauthorized, conflict

class TaskService(BaseService):
    
    def __init__(self):
        # We pass the repo and the schema variable to the parent
        super().__init__(repository=TaskRepository())

    