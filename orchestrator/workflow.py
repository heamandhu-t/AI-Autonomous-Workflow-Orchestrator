
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

        # Step 1: Start workflow
        coordinator_result = self.coordinator.receive_request(
            user_request
        )

        if coordinator_result.get("status") != "workflow_started":
            return coordinator_result

        # Step 2: Get tasks
        plan = coordinator_result["plan"]
        tasks = plan.get("tasks", [])

        if not tasks:
            return {
                "status": "error",
                "message": "No tasks found in the execution plan."
            }

        results = []
        completed_tasks = 0
        failed_tasks = 0

        # Step 3: Execute and track each task
        for task_number, task in enumerate(tasks, start=1):

            task_result = {
                "task_id": task_number,
                "task": task,
                "status": "processing"
            }

            try:
                coding_result = self.coding_agent.execute_task(task)

                task_result["coding_result"] = coding_result

                if coding_result.get("status") != "task_received":
                    task_result["status"] = "failed"
                    failed_tasks += 1
                    results.append(task_result)
                    continue

                qa_result = self.qa_agent.review_task(
                    task, coding_result
                )

                task_result["qa_result"] = qa_result

                if qa_result.get("status") == "review_passed":
                    task_result["status"] = "completed"
                    completed_tasks += 1
                else:
                    task_result["status"] = "failed"
                    failed_tasks += 1

            except Exception as error:
                task_result["status"] = "failed"
                task_result["error"] = str(error)
                failed_tasks += 1

            results.append(task_result)

        # Step 4: Final workflow report
        return {
            "project": user_request,
            "status": (
                "completed" if failed_tasks == 0
                else "completed_with_errors"
            ),
            "total_tasks": len(tasks),
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "execution_results": results
        }
