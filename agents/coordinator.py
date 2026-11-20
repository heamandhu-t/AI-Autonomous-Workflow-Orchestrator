from agents.scoping import ScopingAgent


class CoordinatorAgent:

    def __init__(self):
        self.name = "Coordinator Agent"
        self.scoping_agent = ScopingAgent()

    def receive_request(self, user_request):

        if not user_request.strip():
            return {
                "status": "error",
                "message": "Please provide a project request."
            }

        plan = self.scoping_agent.create_plan(user_request)

        return {
            "coordinator": self.name,
            "request": user_request,
            "status": "workflow_started",
            "next_agent": "Scoping Agent",
            "plan": plan
        }