class QAAgent:

    def __init__(self):
        self.name = "QA Agent"

    def review_task(self, task, result):

        if not task.strip():
            return {
                "status": "error",
                "message": "No task provided."
            }

        if result.get("status") == "task_received":
            return {
                "agent": self.name,
                "task": task,
                "status": "review_passed",
                "message": "Task was successfully received by Coding Agent."
            }

        return {
            "agent": self.name,
            "task": task,
            "status": "review_failed",
            "message": "Task requires further review."
        }