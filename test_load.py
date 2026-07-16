import json

with open('data/knowledge_base/startup_cases.json', 'r') as file:
    startup_cases = json.load(file)



with open('data/knowledge_base/project_cases.json', 'r') as file:
    project_cases = json.load(file)

print(f"Loaded {len(startup_cases)} startup cases")
print(f"Loaded {len(project_cases)} project cases")