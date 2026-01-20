import json

#mở file câu hỏi
with open("Static/Raw_Questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)
file = {}
for question in questions:
    file[question["question"]] = question["answer"]
with open("Static/Question_Library.json", "w", encoding="utf-8") as f:
    json.dump(file,f,ensure_ascii=False,indent=2)

