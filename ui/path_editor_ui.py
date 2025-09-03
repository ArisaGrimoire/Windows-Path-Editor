import customtkinter as ctk
import tkinter as tk
from logic.path_utils import get_env_variable, set_env_variable, path_exists


class PathEditorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Windows Path Editor")
        self.geometry("950x600")

        ctk.set_appearance_mode("dark")

        # 初期状態保存（Undo用）
        self.user_path = get_env_variable("Path", "user")
        self.system_path = get_env_variable("Path", "system")
        self.last_user_path = self.user_path
        self.last_system_path = self.system_path

        self.create_widgets()

    def create_widgets(self):
        # User PATH
        self.user_label = ctk.CTkLabel(self, text="User PATH")
        self.user_label.grid(row=0, column=0, padx=10, pady=5)

        self.user_text = tk.Text(self, width=55, height=30, bg="#1e1e1e", fg="white", insertbackground="white")
        self.user_text.grid(row=1, column=0, padx=10, pady=5)
        self.user_text.insert("1.0", self.user_path.replace(";", "\n"))

        # System PATH
        self.sys_label = ctk.CTkLabel(self, text="System PATH")
        self.sys_label.grid(row=0, column=1, padx=10, pady=5)

        self.sys_text = tk.Text(self, width=55, height=30, bg="#1e1e1e", fg="white", insertbackground="white")
        self.sys_text.grid(row=1, column=1, padx=10, pady=5)
        self.sys_text.insert("1.0", self.system_path.replace(";", "\n"))

        # 色付けのタグ設定
        for text_widget in (self.user_text, self.sys_text):
            text_widget.tag_configure("invalid", foreground="red")
            text_widget.tag_configure("valid", foreground="white")

        # 初期チェック
        self.highlight_invalid_paths()

        # Buttons
        self.apply_btn = ctk.CTkButton(self, text="Apply", command=self.apply_changes)
        self.apply_btn.grid(row=2, column=0, pady=10)

        self.undo_btn = ctk.CTkButton(self, text="Undo", command=self.undo_changes)
        self.undo_btn.grid(row=2, column=1, pady=10)

        self.clear_btn = ctk.CTkButton(self, text="Clear (Remove Invalid)", command=self.clear_invalid)
        self.clear_btn.grid(row=3, column=0, pady=10)

        self.close_btn = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.close_btn.grid(row=3, column=1, pady=10)

    def highlight_invalid_paths(self):
        """存在しないパスを赤で表示"""
        for text_widget in (self.user_text, self.sys_text):
            text_widget.tag_remove("invalid", "1.0", "end")
            text_widget.tag_remove("valid", "1.0", "end")

            lines = text_widget.get("1.0", "end").strip().split("\n")
            for i, line in enumerate(lines, start=1):
                start = f"{i}.0"
                end = f"{i}.end"
                if line.strip():
                    if path_exists(line.strip()):
                        text_widget.tag_add("valid", start, end)
                    else:
                        text_widget.tag_add("invalid", start, end)

    def apply_changes(self):
        new_user = self.user_text.get("1.0", "end").strip().replace("\n", ";")
        new_sys = self.sys_text.get("1.0", "end").strip().replace("\n", ";")

        # Undo用に保存
        self.last_user_path = self.user_path
        self.last_system_path = self.system_path

        # Apply
        set_env_variable("Path", new_user, "user")
        set_env_variable("Path", new_sys, "system")

        # 更新
        self.user_path = new_user
        self.system_path = new_sys
        self.highlight_invalid_paths()

    def undo_changes(self):
        self.user_text.delete("1.0", "end")
        self.user_text.insert("1.0", self.last_user_path.replace(";", "\n"))

        self.sys_text.delete("1.0", "end")
        self.sys_text.insert("1.0", self.last_system_path.replace(";", "\n"))

        self.highlight_invalid_paths()

    def clear_invalid(self):
        """存在しないパスを一括削除"""
        for text_widget in (self.user_text, self.sys_text):
            lines = text_widget.get("1.0", "end").strip().split("\n")
            valid_lines = [line for line in lines if path_exists(line.strip())]
            text_widget.delete("1.0", "end")
            text_widget.insert("1.0", "\n".join(valid_lines))

        self.highlight_invalid_paths()
