import streamlit as st
from datetime import datetime

class Node:
    def __init__(self, task, priority, start_date, due_date, status):
        self.task = task
        self.priority = priority
        self.start_date = start_date
        self.due_date = due_date
        self.status = status
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_task(self, task, priority, start_date, due_date, status):
        new_node = Node(task, priority, start_date, due_date, status)
        if self.head is None or self.head.priority > priority:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next is not None and current.next.priority <= priority:
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def remove_task(self, task):
        current = self.head
        previous = None
        while current is not None:
            if current.task == task:
                if previous is not None:
                    previous.next = current.next
                else:
                    self.head = current.next
                return True
            previous = current
            current = current.next
        return False

    def edit_task(self, task_number, field_to_edit, edit_value):
        current = self.head
        counter = 1
        while current is not None:
            if counter == task_number:
                if field_to_edit == "Task":
                    current.task = edit_value
                elif field_to_edit == "Due Date":
                    current.due_date = edit_value
                elif field_to_edit == "Priority":
                    current.priority = edit_value
                elif field_to_edit == "Start Time":
                    current.start_date = edit_value
                elif field_to_edit == "End Time":
                    current.end_time = edit_value
                return True
            current = current.next
            counter += 1
        return False

    def display_tasks(self):
        tasks = []
        current = self.head
        while current is not None:
            tasks.append((current.task, current.priority, current.start_date, current.due_date, current.status))
            current = current.next
        return tasks

    def to_list(self):
        tasks = []
        current = self.head
        while current is not None:
            tasks.append((current.task, current.priority, current.due_date, current.status))
            current = current.next
        return tasks

    def from_list(self, tasks):
        self.head = None
        for task, priority, due_date, status in reversed(tasks):
            self.add_task(task, priority, due_date, status)

def init_tasks_list():
    if 'tasks_list' not in st.session_state:
        st.session_state.tasks_list = LinkedList()

def add_task():
    st.sidebar.subheader("Add a new task")
    task_input = st.sidebar.text_input("Task description")
    priority_input = st.sidebar.selectbox("Priority", ["High", "Medium", "Low"])
    start_date_input = st.sidebar.date_input("Start date", datetime.now())
    due_date_input = st.sidebar.date_input("Due date", datetime.now())
    status_input = st.sidebar.selectbox("Status", ["Not Started", "In Progress", "Completed"])

    if st.sidebar.button("Add Task"):
        if task_input:
            st.session_state.tasks_list.add_task(task_input, priority_input, start_date_input, due_date_input, status_input)
            st.sidebar.success(f"Task '{task_input}' added with priority '{priority_input}', start date '{start_date_input}', due date '{due_date_input}', and status '{status_input}'.")
        else:
            st.sidebar.error("Task description cannot be empty.")

def edit_task():
    st.sidebar.subheader("Edit a task")
    task_number = st.sidebar.number_input("Task number to edit", min_value=1, value=1)
    field_to_edit = st.sidebar.selectbox("Field to edit", ["Task", "Priority", "Start Time", "Due Date", "End Time"])
    edit_value = None
    if field_to_edit in ["Task", "Priority"]:
        edit_value = st.sidebar.text_input(f"New {field_to_edit.lower()}")
    elif field_to_edit in ["Start Time", "Due Date", "End Time"]:
        edit_value = st.sidebar.date_input(f"New {field_to_edit.lower()}", datetime.now())

    if st.sidebar.button("Edit Task"):
        if edit_value is not None:
            if st.session_state.tasks_list.edit_task(task_number, field_to_edit, edit_value):
                st.sidebar.success(f"Task {task_number} {field_to_edit.lower()} edited successfully.")
            else:
                st.sidebar.error("Task number out of range.")
        else:
            st.sidebar.error("Edit value cannot be empty.")

def remove_task():
    st.sidebar.subheader("Remove a task")
    task_to_remove = st.sidebar.text_input("Task description to remove")
    if st.sidebar.button("Remove Task"):
        if task_to_remove:
            if st.session_state.tasks_list.remove_task(task_to_remove):
                st.sidebar.success(f"Task '{task_to_remove}' removed.")
            else:
                st.sidebar.error(f"Task '{task_to_remove}' not found.")
        else:
            st.sidebar.error("Task description cannot be empty.")

def display_tasks():
    st.subheader("Your To-Do List")
    tasks = st.session_state.tasks_list.display_tasks()
    if not tasks:
        st.write("No tasks yet. Add some tasks using the sidebar!")
    else:
        st.table({
            "Task": [task[0] for task in tasks],
            "Priority": [task[1] for task in tasks],
            "Start Date": [task[2] for task in tasks],
            "Due Date": [task[3] for task in tasks],
            "Status": [task[4] for task in tasks]
        })

def main():
    st.title("To-Do List Application")

    init_tasks_list()

    st.sidebar.title("Manage Your Tasks")
    add_task()
    remove_task()
    edit_task()

    display_tasks()

if __name__ == "__main__":
    main()
