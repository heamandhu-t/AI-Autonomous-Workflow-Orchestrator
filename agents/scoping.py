class ScopingAgent:
    """Agent responsible for breaking project requests into tasks."""

    def __init__(self):
        self.name = "Scoping Agent"

    def create_plan(self, user_request):
        if not user_request.strip():
            return {
                "status": "error",
                "message": "No project request provided."
            }

        tasks = [
            "Analyze project requirements",
            "Identify required technologies",
            "Break the project into smaller tasks",
            "Identify task dependencies",
            "Prepare the execution plan"
        ]

        return {
            "agent": self.name,
            "project": user_request,
            "status": "plan_created",
            "tasks": tasks
        }