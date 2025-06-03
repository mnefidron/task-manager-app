# notifications.py
import customtkinter as ctk

def show_popup_notification(parent, title, message, duration=5000):
    """
    Показывает не модальное всплывающее уведомление внутри окна приложения.
    """
# Определяем текущую тему
    current_theme = ctk.get_appearance_mode().lower()

    # Цвета для светлой и темной темы
    if current_theme == "dark":
        bg_color = "#2a2d2e"
        text_color = "white"
        border_color = "#555555"
        button_hover = "#444444"
        button_text = "white"
    else:
        bg_color = "#f8f9fa"
        text_color = "black"
        border_color = "#ced4da"
        button_hover = "#e0e0e0"
        button_text = "black"

    notification_frame = ctk.CTkFrame(
        parent,
        corner_radius=15,  # Закругленные края
        fg_color=bg_color,
        border_width=1,
        border_color=border_color
    )
    
    # Позиционирование в правом нижнем углу
    notification_frame.place(relx=0.98, rely=0.98, anchor="se")

    # Заголовок
    title_label = ctk.CTkLabel(
        notification_frame,
        text=title,
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=text_color
    )
    title_label.pack(anchor="w", padx=10, pady=(10, 5))

    # Сообщение
    msg_label = ctk.CTkLabel(
        notification_frame,
        text=message,
        wraplength=280,
        justify="left",
        text_color=text_color
    )
    msg_label.pack(anchor="w", padx=10, pady=(0, 10))

    # Кнопка закрытия
    close_button = ctk.CTkButton(
        notification_frame,
        text="✕",
        width=20,
        fg_color="transparent",
        hover_color=button_hover,
        text_color=button_text,
        command=lambda: notification_frame.place_forget()
    )
    close_button.place(relx=0.98, rely=0.05, anchor="ne")

    # Автоматическое закрытие
    notification_frame.after(duration, notification_frame.destroy)

    # Сохраняем ссылку на фрейм, чтобы он не удалился сборщиком мусора
    if not hasattr(parent, "active_notifications"):
        parent.active_notifications = []
    parent.active_notifications.append(notification_frame)