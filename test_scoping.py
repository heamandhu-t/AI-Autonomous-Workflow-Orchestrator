from agents.scoping import ScopingAgent

scoping = ScopingAgent()

result = scoping.create_plan(
    "Build a student management system"
)

print(result)