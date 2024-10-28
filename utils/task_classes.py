TASK_PROMPT = lambda text: 'You are tasked with detecting whether the given text describes adding, removing, or updating a task. \
    If any field is not explicitly mentioned in the text, leave it empty. \
    Here are two examples:\n\n\
    Example 1:\n\
    Text: "Add a dentist appointment on December 5th, 2024 at 3 PM at 34 Avenue."\n\
    Result: {\
        "type": "add",\
        "task": "dentist appointment",\
        "time": "3 PM",\
        "location": "34 Avenue",\
        "year": "2024",\
        "month": "12",\
        "day": "5",\
        "hour": "15",\
        "minute": "00"\
    }\n\n\
    Example 2:\n\
    Text: "Remove the gym session on October 25th."\n\
    Result: {\
        "type": "remove",\
        "task": "gym session",\
        "time": "",\
        "location": "",\
        "year": "2024",\
        "month": "10",\
        "day": "25",\
        "hour": "",\
        "minute": ""\
    }\n\n\
    Here is the text:\n' + text + '\n\
    Return the result only in the following JSON format without any extra explanation:' + '{\
        "type": "<add or remove or update>",\
        "task": "<task description>",\
        "time": "<time>",\
        "location": "<location>",\
        "year": "<year>",\
        "month": "<month>",\
        "day": "<day>",\
        "hour": "<hour>",\
        "minute": "<minute>"\
    }'

class TASK:
    def __init__(self, **kwargs) -> None:
        self.task_name = kwargs["name"]
        self.task_describtion = kwargs["describe"]

class TASK_MANAGER:
    def __init__(self) -> None:
        self.task_list = {}