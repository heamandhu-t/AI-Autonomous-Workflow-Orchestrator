
from orchestrator.workflow import WorkflowOrchestrator

workflow = WorkflowOrchestrator()

result = workflow.run_workflow(
    "Build a student management system"
)

print(result)
