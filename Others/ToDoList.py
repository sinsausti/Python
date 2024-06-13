import os

def display_tasks(tasks):
    if not tasks:
        print("No tasks to show.")
    else:
        for i, task in enumerate(tasks, start=1):
            status = "Done" if task['completed'] else "Not Done"
            print(f"{i}. {task['description']} - {status}")

def save_tasks(tasks, filename='tasks.txt'):
    with open(filename, 'w') as file:
        for task in tasks:
            file.write(f"{task['description']}|{task['completed']}\n")

def load_tasks(filename='tasks.txt'):
    tasks = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                description, completed = line.strip().split('|')
                tasks.append({'description': description, 'completed': completed == 'True'})
    return tasks

def to_do_list_manager():
    tasks = load_tasks()
    print("Welcome to the To-Do List Manager!")

    while True:
        print("\nMenu:")
        print("1. View tasks")
        print("2. Add task")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_tasks(tasks)
        elif choice == '2':
            description = input("Enter task description: ").strip()
            tasks.append({'description': description, 'completed': False})
            save_tasks(tasks)
        elif choice == '3':
            task_num = int(input("Enter task number to complete: "))
            if 1 <= task_num <= len(tasks):
                tasks[task_num - 1]['completed'] = True
                save_tasks(tasks)
            else:
                print("Invalid task number.")
        elif choice == '4':
            task_num = int(input("Enter task number to delete: "))
            if 1 <= task_num <= len(tasks):
                tasks.pop(task_num - 1)
                save_tasks(tasks)
            else:
                print("Invalid task number.")
        elif choice == '5':
            break
        else:
            print("Invalid choice, please try again.")

to_do_list_manager()