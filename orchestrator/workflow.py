
from agents.coordinator import CoordinatorAgent
from agents.coding import CodingAgent
from agents.qa import QAAgent


class WorkflowOrchestrator:

    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.coding_agent = CodingAgent()
        self.qa_agent = QAAgent()

    def validate_dependencies(self, tasks, dependencies):

        total_tasks = len(tasks)

        for task_number, required_tasks in dependencies.items():

            if task_number < 1 or task_number > total_tasks:
                return False, f"Invalid task number: {task_number}"

            for dependency in required_tasks:

                if dependency < 1 or dependency > total_tasks:
                    return False, (
                        f"Task {task_number} has invalid dependency "
                        f"{dependency}."
                    )

                if dependency == task_number:
                    return False, (
                        f"Task {task_number} cannot depend on itself."
                    )

        # Detect circular dependencies
        visited = set()
        visiting = set()

        def has_cycle(task_number):

            if task_number in visiting:
                return True

            if task_number in visited:
                return False

            visiting.add(task_number)

            for dependency in dependencies.get(task_number, []):
                if has_cycle(dependency):
                    return True

            visiting.remove(task_number)
            visited.add(task_number)

            return False

        for task_number in range(1, total_tasks + 1):

            if has_cycle(task_number):
                return False, "Circular dependency detected."

        return True, "All dependencies are valid."

    def get_execution_order(self, tasks, dependencies):

        total_tasks = len(tasks)

        # Count dependencies for every task
        in_degree = {
            task_number: len(dependencies.get(task_number, []))
            for task_number in range(1, total_tasks + 1)
        }

        # Create dependency connections
        dependents = {
            task_number: []
            for task_number in range(1, total_tasks + 1)
        }

        for task_number, required_tasks in dependencies.items():

            for dependency in required_tasks:
                dependents[dependency].append(task_number)

        # Start with tasks that have no dependencies
        ready_tasks = sorted([
            task_number
            for task_number, count in in_degree.items()
            if count == 0
        ])

        execution_order = []

        while ready_tasks:

            current_task = ready_tasks.pop(0)
            execution_order.append(current_task)

            for dependent in sorted(dependents[current_task]):

                in_degree[dependent] -= 1

                if in_degree[dependent] == 0:
                    ready_tasks.append(dependent)

            ready_tasks.sort()

        return execution_order

    def run_workflow(self, user_request):

        if not user_request or not user_request.strip():
            return {
                "status": "error",
                "message": "Please provide a project request."
            }

        coordinator_result = self.coordinator.receive_request(
            user_request
        )

        if coordinator_result.get("status") != "workflow_started":
            return coordinator_result

        plan = coordinator_result["plan"]
        tasks = plan.get("tasks", [])

        if not tasks:
            return {
                "status": "error",
                "message": "No tasks found."
            }

        # Current prototype dependencies
        dependencies = {
            1: [],
            2: [1],
            3: [1, 2],
            4: [3],
            5: [1, 2, 3, 4]
        }

        # Validate dependencies
        valid, validation_message = self.validate_dependencies(
            tasks, dependencies
        )

        if not valid:
            return {
                "status": "error",
                "message": validation_message
            }

        # Automatically determine execution order
        execution_order = self.get_execution_order(
            tasks, dependencies
        )

        if len(execution_order) != len(tasks):
            return {
                "status": "error",
                "message": "Unable to determine a valid execution order."
            }

        results = []
        task_status = {}

        # Execute tasks according to dependency order
        for task_number in execution_order:

            task = tasks[task_number - 1]
            required_tasks = dependencies.get(task_number, [])

            blocked = [
                dependency
                for dependency in required_tasks
                if task_status.get(dependency) != "completed"
            ]

            if blocked:
                task_status[task_number] = "blocked"

                results.append({
                    "task_id": task_number,
                    "task": task,
                    "status": "blocked",
                    "blocked_by": blocked
                })
                continue

            task_result = {
                "task_id": task_number,
                "task": task,
                "status": "processing",
                "dependencies": required_tasks
            }

            try:
                coding_result = self.coding_agent.execute_task(task)
                task_result["coding_result"] = coding_result

                if coding_result.get("status") != "task_received":
                    task_result["status"] = "failed"
                    task_status[task_number] = "failed"
                    results.append(task_result)
                    continue

                qa_result = self.qa_agent.review_task(
                    task, coding_result
                )
                task_result["qa_result"] = qa_result

                if qa_result.get("status") == "review_passed":
                    task_result["status"] = "completed"
                    task_status[task_number] = "completed"
                else:
                    task_result["status"] = "failed"
                    task_status[task_number] = "failed"

            except Exception as error:
                task_result["status"] = "failed"
                task_result["error"] = str(error)
                task_status[task_number] = "failed"

            results.append(task_result)

        completed = sum(
            1 for status in task_status.values()
            if status == "completed"
        )

        failed = sum(
            1 for status in task_status.values()
            if status == "failed"
        )

        blocked = sum(
            1 for status in task_status.values()
            if status == "blocked"
        )

        return {
            "project": user_request,
            "status": "workflow_processed",
            "total_tasks": len(tasks),
            "completed_tasks": completed,
            "failed_tasks": failed,
            "blocked_tasks": blocked,
            "dependency_validation": validation_message,
            "execution_order": execution_order,
            "execution_results": results
        }
