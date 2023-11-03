import os
import requests
from datetime import datetime

# Создаем директорию "tasks" если её нет
os.makedirs("tasks", exist_ok=True)

# Получаем данные о пользователях и задачах
users_url = "https://json.medrocket.ru/users"
tasks_url = "https://json.medrocket.ru/todos"
users_response = requests.get(users_url)
tasks_response = requests.get(tasks_url)
users_data = users_response.json()
tasks_data = tasks_response.json()

def create_user_report(user_data):
    username = user_data["username"]
    company_name = user_data["company"]["name"]
    email = user_data["email"]
    creation_time = datetime.now().strftime("%d-%m-%Y %H_%M")
    user_id = user_data["id"]
    #tasks = [task for task in tasks_data if task["id"] == user_id]
    tasks_url = f"https://json.medrocket.ru/todos?userId={user_id}"
    tasks_response = requests.get(tasks_url)
    tasks_data = tasks_response.json()

    unfinished_tasks = [task for task in tasks_data if not task["completed"]]
    finished_tasks = [task for task in tasks_data if task["completed"]]

    report_filename = f"tasks/{username}.txt"

    # Проверяем существует ли уже отчет для пользователя
    if os.path.isfile(report_filename):
        # Если отчет существует, то создаем новое имя с текущей датой и временем
        old_time_str = datetime.now().strftime("%d-%m-%Y %H_%M")
        old_report_filename = f"tasks/old_{username}_{old_time_str}.txt"

        # Переименовываем существующий файл
        os.rename(report_filename, old_report_filename)

    # Записываем новый отчет
    with open(report_filename, "w") as report_file:
        report_file.write(f"# Отчёт для {company_name}.\n")
        report_file.write(f"{username} <{email}> {creation_time}\n")
        report_file.write(f"Всего задач: {len(tasks_data)}\n\n")
        report_file.write(f"## Актуальные задачи ({len(unfinished_tasks)}):\n")
        for task in unfinished_tasks:
            task_title = task["title"][:46] + "…" if len(task["title"]) > 46 else task["title"]
            report_file.write(f"- {task_title}\n")
        report_file.write(f"## Завершённые задачи ({len(finished_tasks)}):\n")
        for task in finished_tasks:
            task_title = task["title"][:46] + "…" if len(task["title"]) > 46 else task["title"]
            report_file.write(f"- {task_title}\n")

# Создаем отчеты для всех пользователей
for user_data in users_data:
    create_user_report(user_data)
