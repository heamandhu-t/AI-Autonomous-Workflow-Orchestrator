
from agents.coordinator import CoordinatorAgent
from agents.coding import CodingAgent
from agents.qa import QAAgent


class WorkflowOrchestrator:

    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.coding_agent = CodingAgent()
        self.qa_agent = QAAgent()

    def run_workflow(self, user_request):

        if not user_request or not user_request.strip():
            return {
                "status": "error",
                "message": "Please provide a project request."
            }

        # Step 1: Coordinator starts the workflow
        coordinator_result = self.coordinator.receive_request(user_request)

        if coordinator_result.get("status") != "workflow_started":
            return coordinator_result

        # Step 2: Get tasks from Scoping Agent
        plan = coordinator_result["plan"]
        tasks = plan.get("tasks", [])

        results = []

        # Step 3: Coding Agent receives each task
        for task in tasks:

            coding_result = self.coding_agent.execute_task(task)

            # Step 4: QA Agent reviews the task result
            qa_result = self.qa_agent.review_task(
                task, coding_result
            )

            results.append({
                "task": task,
                "coding_result": coding_result,
                "qa_result": qa_result
            })

        return {
            "project": user_request,
            "status": "workflow_processed",
            "coordinator": coordinator_result,
            "execution_results": results
        }
