class TASK:
    def __init__(self, **kwargs) -> None:
        self.task_name = kwargs["name"]
        self.task_describtion = kwargs["describe"]

class TASK_MANAGER:
    def __init__(self) -> None:
        self.task_list = {}