import sys
import os
import tkinter as tk

# Thêm đường dẫn module gốc nếu chạy trực tiếp
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))

from controller.ui.main_window import MainWindow


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
