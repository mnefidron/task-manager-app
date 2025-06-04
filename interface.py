# interface.py
import customtkinter as ctk
import crud
import notifications
from datetime import datetime
from tkcalendar import DateEntry
import tkinter as tk
import json
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TaskManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Система управления задачами")
        self.geometry("1075x700")
        self.resizable(False, False)
        
        # Путь к файлу настроек
        self.settings_file = os.path.join(os.path.dirname(__file__), "settings.json")
        # Загрузка настроек
        self.load_settings()
        
        # Кнопка настроек
        self.settings_button = ctk.CTkButton(
            self,
            text="⚙️",
            width=30,
            command=self.open_settings
        )
        self.settings_button.place(x=10, y=20)

        self.create_widgets()
        self.load_tasks()
        self.check_notifications()

    def create_widgets(self):
        # Заголовок
        self.title_label = ctk.CTkLabel(
            self,
            text="Kanban Доска",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=10)

        # Кнопка добавления задачи
        self.add_button = ctk.CTkButton(
            self,
            text="Добавить задачу",
            command=self.open_add_task_window
        )
        self.add_button.place(x=900, y=20)

        # Колонки Kanban с заголовками и скролл-баром
        self.columns = {
            "To Do": {"scroll_frame": None, "tasks": []},
            "In Progress": {"scroll_frame": None, "tasks": []},
            "Done": {"scroll_frame": None, "tasks": []}
        }

        x_pos = 20
        for status in self.columns:
            col_frame = ctk.CTkFrame(self, width=330, height=600)
            col_frame.place(x=x_pos, y=60)

            # Заголовок колонки
            col_title = ctk.CTkLabel(
                col_frame,
                text=status,
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="center"
            )
            col_title.pack(pady=(0, 5), fill="x")

            # Прокручиваемый фрейм для задач
            scroll_frame = ctk.CTkScrollableFrame(
                col_frame,
                width=310,
                height=530
            )
            scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

            self.columns[status]["scroll_frame"] = scroll_frame
            self.columns[status]["tasks"] = []
            x_pos += 340

        # Список задач
        self.task_widgets = {"To Do": [], "In Progress": [], "Done": []}

    def open_add_task_window(self):
        """Открывает окно добавления задачи"""
        AddEditTaskWindow(self, mode="add")

    def open_edit_task_window(self, task):
        """Открывает окно редактирования задачи"""
        AddEditTaskWindow(self, mode="edit", task=task)

    def load_tasks(self):
        for status in self.columns:
            for widget in self.columns[status]["tasks"]:
                widget.destroy()
            self.columns[status]["tasks"].clear()

        tasks = crud.get_tasks()
        for task in tasks:
            task_id, title, description, deadline, priority, status, assignees = task

            task_frame = ctk.CTkFrame(self.columns[status]["scroll_frame"], width=310, height=100)
            task_frame.pack(pady=5, padx=5, fill="x")

            # Цвет по приоритету
            priority_colors = {
                "низкий": "#d4edda",
                "средний": "#fff3cd",
                "высокий": "#f8d7da"
            }
            task_frame.configure(fg_color=priority_colors.get(priority.lower(), "#ffffff"))

            # Заголовок задачи (чёрный текст)
            title_label = ctk.CTkLabel(
                task_frame,
                text=title,
                font=ctk.CTkFont(weight="bold"),
                text_color="black"
            )
            title_label.pack(anchor="w", padx=5, pady=2)

            # Описание задачи
            desc_label = ctk.CTkLabel(
                task_frame,
                text=description[:50] + ("..." if len(description) > 50 else ""),
                font=ctk.CTkFont(size=12),
                text_color="black"
            )
            desc_label.pack(anchor="w", padx=5, pady=2)

            # Дедлайн и исполнители
            info_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
            info_frame.pack(fill="x", padx=5, pady=2)

            deadline_label = ctk.CTkLabel(
                info_frame,
                text=f"До: {deadline}",
                font=ctk.CTkFont(size=10),
                text_color="black"
            )
            deadline_label.pack(side="left")

            assignees_label = ctk.CTkLabel(
                info_frame,
                text=f"Исполнители: {assignees}",
                font=ctk.CTkFont(size=10),
                text_color="black"
            )
            assignees_label.pack(side="right")

            # Кнопки действий
            action_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
            action_frame.pack(fill="x", padx=5, pady=2)

            view_button = ctk.CTkButton(
                action_frame,
                text="👁",
                width=20,
                command=lambda t=task: self.view_task(t),
                text_color="black"
            )
            view_button.pack(side="left", padx=2)

            edit_button = ctk.CTkButton(
                action_frame,
                text="✏️",
                width=20,
                command=lambda t=task: self.open_edit_task_window(t),
                text_color="black"
            )
            edit_button.pack(side="left", padx=2)

            delete_button = ctk.CTkButton(
                action_frame,
                text="🗑",
                width=20,
                command=lambda t=task: self.delete_task(t),
                text_color="black"
            )
            delete_button.pack(side="left", padx=2)

            # Drag-and-Drop
            task_frame.bind("<Button-1>", lambda e, tf=task_frame, stat=status, tid=task_id: self.start_drag(e, tf, stat, tid))
            task_frame.bind("<B1-Motion>", self.do_drag)
            task_frame.bind("<ButtonRelease-1>", lambda e, tf=task_frame, stat=status, tid=task_id: self.end_drag(e, tf, stat, tid))

            self.columns[status]["tasks"].append(task_frame)
            self.task_widgets[status].append(task_frame)

    def start_drag(self, event, task_frame, status, task_id):
        self.drag_data = {
            "widget": task_frame,
            "start_x": event.x,
            "start_y": event.y,
            "original_status": status,
            "task_id": task_id
        }

    def do_drag(self, event):
        widget = self.drag_data["widget"]
        x = widget.winfo_x() + event.x - self.drag_data["start_x"]
        y = widget.winfo_y() + event.y - self.drag_data["start_y"]
        widget.place(x=x, y=y)

    def end_drag(self, event, widget, original_status, task_id):
        widget.place_forget()
        widget.pack_propagate(True)
        widget.pack(pady=5, padx=5, fill="x")

        new_status = None
        for col_status, col_data in self.columns.items():
            col_frame = col_data["scroll_frame"].master
            frame_x = col_frame.winfo_rootx()
            frame_y = col_frame.winfo_rooty()
            frame_width = col_frame.winfo_width()
            frame_height = col_frame.winfo_height()

            if frame_x < event.x_root < frame_x + frame_width and frame_y < event.y_root < frame_y + frame_height:
                new_status = col_status
                break

        if new_status and new_status != original_status:
            crud.update_task_status(task_id, new_status)
            self.load_tasks()
        else:
            # Возвращаем в исходную колонку
            self.drag_data["original_status"] = original_status
            self.drag_data["widget"].pack(pady=5, padx=5, fill="x")

    def view_task(self, task):
        task_window = ctk.CTkToplevel(self)
        task_window.title("Просмотр задачи")
        task_window.geometry("400x300")
        task_window.grab_set()
        task_id, title, description, deadline, priority, status, assignees = task

        ctk.CTkLabel(task_window, text=f"Название: {title}", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        ctk.CTkLabel(task_window, text="Описание:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10)
        ctk.CTkLabel(task_window, text=description, wraplength=380).pack(pady=5, padx=10, fill="x")

        info_frame = ctk.CTkFrame(task_window, fg_color="transparent")
        info_frame.pack(fill="x", padx=10)
        ctk.CTkLabel(info_frame, text=f"Дедлайн: {deadline}").pack(side="left")
        ctk.CTkLabel(info_frame, text=f"Приоритет: {priority}").pack(side="left", padx=10)
        ctk.CTkLabel(info_frame, text=f"Статус: {status}").pack(side="left", padx=10)

        ctk.CTkLabel(task_window, text="Исполнители:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10)
        assignees_list = ", ".join(assignees.split(",")) if assignees else "Нет исполнителей"
        ctk.CTkLabel(task_window, text=assignees_list).pack(pady=5, padx=10)
        ctk.CTkButton(task_window, text="Закрыть", command=task_window.destroy).pack(pady=10)

    def delete_task(self, task):
        if tk.messagebox.askyesno("Удалить задачу", "Вы действительно хотите удалить эту задачу?"):
            crud.delete_task(task[0])
            self.load_tasks()

    def check_notifications(self):
        tasks = crud.get_tasks()
        current_time = datetime.now()

        # Очистка старых уведомлений
        for frame in getattr(self, "active_notifications", []):
            frame.destroy()
        self.active_notifications = []

        for task in tasks:
            task_id, title, description, deadline, priority, status, assignees = task
            try:
                deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
                time_diff = (deadline_date - current_time).days

                if 0 <= time_diff <= 1 and status != "Done":
                    notifications.show_popup_notification(
                        self,
                        f"⚠️ Близкий дедлайн: {title}",
                        f"Задача: {title}\nДедлайн: {deadline_date.strftime('%d.%m.%Y')}"
                    )
            except ValueError:
                pass

        self.after(300000, self.check_notifications)

    def open_settings(self):
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Настройки")
        settings_window.geometry("400x200")
        settings_window.resizable(False, False)
        settings_window.grab_set()

        ctk.CTkLabel(settings_window, text="Настройки внешнего вида", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        theme_label = ctk.CTkLabel(settings_window, text="Цветовая тема:")
        theme_label.pack(anchor="w", padx=20)

        theme_options = ["Светлая", "Темная", "Системная"]
        current_theme = ctk.get_appearance_mode().lower()
        theme_mapping = {
            "light": "Светлая",
            "dark": "Темная",
            "system": "Системная"
        }
        current_theme_rus = theme_mapping.get(current_theme, "Системная")

        theme_combobox = ctk.CTkComboBox(settings_window, values=theme_options)
        theme_combobox.set(current_theme_rus)
        theme_combobox.pack(pady=5, padx=20, fill="x")

        def save_and_close():
            selected_theme = theme_combobox.get()
            theme_map = {
                "Светлая": "Light",
                "Темная": "Dark",
                "Системная": "System"
            }
            ctk.set_appearance_mode(theme_map[selected_theme])
            self.save_settings(theme_map[selected_theme])
            settings_window.destroy()

        save_button = ctk.CTkButton(settings_window, text="Сохранить", command=save_and_close)
        save_button.pack(pady=15)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
                theme = settings.get("theme", "system")
                ctk.set_appearance_mode(theme.capitalize())

    def save_settings(self, theme):
        with open(self.settings_file, "w") as f:
            json.dump({"theme": theme.lower()}, f)

class AddEditTaskWindow(ctk.CTkToplevel):
    def __init__(self, parent, mode, task=None):
        super().__init__(parent)
        self.parent = parent
        self.mode = mode
        self.task = task
        self.title("Добавить задачу" if mode == "add" else "Редактировать задачу")
        self.geometry("500x500")
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        # Заголовок задачи
        self.title_label = ctk.CTkLabel(self, text="Название задачи:", font=ctk.CTkFont(weight="bold"))
        self.title_label.pack(anchor="w", padx=20, pady=(10, 0))
        self.title_entry = ctk.CTkEntry(self, width=460)
        self.title_entry.pack(padx=20, fill="x")

        # Описание задачи
        self.desc_label = ctk.CTkLabel(self, text="Описание:", font=ctk.CTkFont(weight="bold"))
        self.desc_label.pack(anchor="w", padx=20, pady=(10, 0))
        self.desc_entry = ctk.CTkTextbox(self, height=100)
        self.desc_entry.pack(padx=20, fill="x")

        # Приоритет и статус
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=10)

        self.priority_label = ctk.CTkLabel(info_frame, text="Приоритет:", font=ctk.CTkFont(weight="bold"))
        self.priority_label.pack(side="left")
        self.priority_combo = ctk.CTkComboBox(info_frame, values=["низкий", "средний", "высокий"])
        self.priority_combo.pack(side="left", padx=10)

        self.status_label = ctk.CTkLabel(info_frame, text="Статус:", font=ctk.CTkFont(weight="bold"))
        self.status_label.pack(side="left")
        self.status_combo = ctk.CTkComboBox(info_frame, values=["To Do", "In Progress", "Done"])
        self.status_combo.pack(side="left", padx=10)

        # Дедлайн
        self.deadline_label = ctk.CTkLabel(self, text="Дедлайн:", font=ctk.CTkFont(weight="bold"))
        self.deadline_label.pack(anchor="w", padx=20, pady=(10, 0))
        self.deadline_picker = DateEntry(self, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.deadline_picker.pack(padx=20, anchor="w")

        # Исполнители
        self.assignees_label = ctk.CTkLabel(self, text="Исполнители:", font=ctk.CTkFont(weight="bold"))
        self.assignees_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.assignees_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.assignees_frame.pack(fill="x", padx=20)
        self.assignees_list_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.assignees_list_frame.pack(fill="x", padx=20)
        self.assignees_input = ctk.CTkEntry(self.assignees_frame, width=200)
        self.assignees_input.pack(side="left")
        self.add_assignee_button = ctk.CTkButton(self.assignees_frame, text="+", width=30, command=self.add_assignee)
        self.add_assignee_button.pack(side="left", padx=5)

        self.assignees = []
        if self.mode == "edit" and self.task:
            self.title_entry.insert(0, self.task[1])
            self.desc_entry.insert("1.0", self.task[2])
            
            priority_index = ["низкий", "средний", "высокий"].index(self.task[4]) if self.task[4] in ["низкий", "средний", "высокий"] else 0
            self.priority_combo.set(["низкий", "средний", "высокий"][priority_index])
            
            status_index = ["To Do", "In Progress", "Done"].index(self.task[5]) if self.task[5] in ["To Do", "In Progress", "Done"] else 0
            self.status_combo.set(["To Do", "In Progress", "Done"][status_index])
            
            try:
                deadline_date = datetime.strptime(self.task[3], "%Y-%m-%d")
                self.deadline_picker.set_date(deadline_date)
            except:
                pass
            
            assignees_list = self.task[6].split(",") if self.task[6] else []
            for assignee in assignees_list:
                self.create_assignee_tag(assignee.strip())
        
        # Кнопка сохранения
        self.save_button = ctk.CTkButton(self, text="Создать задачу" if self.mode == "add" else "Сохранить изменения", 
                                         command=self.save_task)
        self.save_button.pack(pady=20)

    def add_assignee(self):
        name = self.assignees_input.get().strip()
        if name:
            self.create_assignee_tag(name)
            self.assignees_input.delete(0, "end")
    
    def create_assignee_tag(self, name):
        assignee_frame = ctk.CTkFrame(self.assignees_list_frame, fg_color="transparent")
        assignee_frame.pack(side="left", padx=2, pady=2)
        
        ctk.CTkLabel(assignee_frame, text=name, width=80).pack(side="left")
        ctk.CTkButton(assignee_frame, text="✕", width=20, command=lambda: self.remove_assignee(assignee_frame, name)).pack(side="left")
        
        self.assignees.append(name)
    
    def remove_assignee(self, frame, name):
        frame.destroy()
        if name in self.assignees:
            self.assignees.remove(name)
    
    def save_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get("1.0", "end-1c")
        deadline = self.deadline_picker.get_date().strftime("%Y-%m-%d")
        priority = self.priority_combo.get()
        status = self.status_combo.get()
        
        if not title:
            tk.messagebox.showerror("Ошибка", "Введите название задачи")
            return
        
        if self.mode == "add":
            crud.create_task(title, description, deadline, priority, status, self.assignees)
        else:
            crud.update_task(self.task[0], title, description, deadline, priority, status, self.assignees)
        
        self.parent.load_tasks()
        self.destroy()