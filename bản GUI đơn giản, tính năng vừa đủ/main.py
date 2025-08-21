import tkinter as tk
from gui_manager import TypingTestGUI

def main():
    root = tk.Tk()
    app = TypingTestGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()