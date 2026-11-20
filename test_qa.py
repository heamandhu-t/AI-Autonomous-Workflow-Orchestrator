from agents.qa import QAAgent
from agents.coding import CodingAgent

coding = CodingAgent()
qa = QAAgent()

task = "Create a student registration module"

coding_result = coding.execute_task(task)

qa_result = qa.review_task(task, coding_result)

print("Coding Result:")
print(coding_result)

print("\nQA Result:")
print(qa_result)