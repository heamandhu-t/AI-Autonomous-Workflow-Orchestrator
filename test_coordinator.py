from agents.coordinator import CoordinatorAgent

coordinator = CoordinatorAgent()

result = coordinator.receive_request(
    "Build a student management system"
)

print(result)