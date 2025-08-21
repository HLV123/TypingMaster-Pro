import tkinter as tk
from tkinter import ttk
import re
from typing import Dict, Any

class ModeSelectionDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Chọn chế độ luyện tập")
        self.dialog.geometry("550x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(True, True)
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (550 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (700 // 2)
        self.dialog.geometry(f"550x700+{x}+{y}")
        
        self.result = None
        self.setup_ui()
        
    def setup_ui(self):
        # Main container frame
        container_frame = ttk.Frame(self.dialog)
        container_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(container_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        
        # Configure scrollable frame
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main content frame with padding
        main_frame = ttk.Frame(self.scrollable_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Cấu hình chế độ luyện tập", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 30))
        
        # Difficulty Level Section
        difficulty_frame = ttk.LabelFrame(main_frame, text="1. Độ khó (theo độ dài câu)", 
                                         padding="20")
        difficulty_frame.pack(fill=tk.X, pady=(0, 25))
        
        self.difficulty_var = tk.StringVar(value="easy")
        
        difficulty_desc = ttk.Label(difficulty_frame, 
                                   text="Chọn độ khó dựa trên số ký tự trong câu:",
                                   font=("Arial", 10), foreground="gray")
        difficulty_desc.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Radiobutton(difficulty_frame, text="Easy (0-25 ký tự) - Câu ngắn, dễ gõ", 
                       variable=self.difficulty_var, value="easy").pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(difficulty_frame, text="Medium (26-60 ký tự) - Câu trung bình", 
                       variable=self.difficulty_var, value="medium").pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(difficulty_frame, text="Hard (61+ ký tự) - Câu dài, thử thách", 
                       variable=self.difficulty_var, value="hard").pack(anchor=tk.W, pady=5)
        
        # Content Filter Section
        content_frame = ttk.LabelFrame(main_frame, text="2. Loại nội dung", 
                                      padding="20")
        content_frame.pack(fill=tk.X, pady=(0, 25))
        
        self.content_var = tk.StringVar(value="letters_only")
        
        content_desc = ttk.Label(content_frame, 
                                text="Chọn loại ký tự xuất hiện trong bài tập:",
                                font=("Arial", 10), foreground="gray")
        content_desc.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Radiobutton(content_frame, text="Chỉ chữ cái và khoảng trắng - Phù hợp người mới bắt đầu", 
                       variable=self.content_var, value="letters_only").pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(content_frame, text="Bao gồm số và ký tự đặc biệt (@, #, $, ...) - Nâng cao", 
                       variable=self.content_var, value="with_special").pack(anchor=tk.W, pady=5)
        
        # Display Mode Section
        display_frame = ttk.LabelFrame(main_frame, text="3. Cách hiển thị", 
                                      padding="20")
        display_frame.pack(fill=tk.X, pady=(0, 25))
        
        self.display_var = tk.StringVar(value="full_sentence")
        
        display_desc = ttk.Label(display_frame, 
                                text="Chọn cách hiển thị văn bản trong quá trình luyện tập:",
                                font=("Arial", 10), foreground="gray")
        display_desc.pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Radiobutton(display_frame, text="Hiển thị cả câu - Xem toàn bộ câu cần gõ", 
                       variable=self.display_var, value="full_sentence").pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(display_frame, text="Hiển thị từng từ (Word by Word) - Tập trung từng từ một", 
                       variable=self.display_var, value="word_by_word").pack(anchor=tk.W, pady=5)
        
        # Tips Section
        tips_frame = ttk.LabelFrame(main_frame, text="💡 Gợi ý", 
                                   padding="20")
        tips_frame.pack(fill=tk.X, pady=(0, 25))
        
        tips_text = """• Người mới học: Chọn Easy + Chỉ chữ cái + Hiển thị cả câu
• Muốn cải thiện tốc độ: Chọn Medium + Có ký tự đặc biệt + Word by word
• Thách thức bản thân: Chọn Hard + Có ký tự đặc biệt + Hiển thị cả câu
• Word by word giúp tập trung và giảm lỗi chính tả"""
        
        tips_label = ttk.Label(tips_frame, text=tips_text, 
                              font=("Arial", 9), foreground="darkgreen",
                              justify=tk.LEFT)
        tips_label.pack(anchor=tk.W)
        
        # Preview Section
        preview_frame = ttk.LabelFrame(main_frame, text="📋 Xem trước cấu hình", 
                                      padding="20")
        preview_frame.pack(fill=tk.X, pady=(0, 30))
        
        self.preview_label = ttk.Label(preview_frame, 
                                      text="Chọn các tùy chọn ở trên để xem cấu hình",
                                      font=("Arial", 11),
                                      foreground="gray",
                                      justify=tk.LEFT)
        self.preview_label.pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="Hủy", 
                  command=self.cancel, 
                  style="TButton").pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Bắt đầu luyện tập", 
                  command=self.confirm,
                  style="Accent.TButton").pack(side=tk.RIGHT)
        
        # Bind events to update preview
        self.difficulty_var.trace('w', self.update_preview)
        self.content_var.trace('w', self.update_preview)
        self.display_var.trace('w', self.update_preview)
        
        # Bind mousewheel to canvas for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Initial preview update
        self.update_preview()
        
    def update_preview(self, *args):
        difficulty_text = {
            "easy": "Dễ (0-25 ký tự)",
            "medium": "Trung bình (26-60 ký tự)", 
            "hard": "Khó (61+ ký tự)"
        }
        
        content_text = {
            "letters_only": "Chỉ chữ cái",
            "with_special": "Có số + ký tự đặc biệt"
        }
        
        display_text = {
            "full_sentence": "Hiển thị cả câu",
            "word_by_word": "Hiển thị từng từ"
        }
        
        preview = f"""Cấu hình hiện tại:
• Độ khó: {difficulty_text[self.difficulty_var.get()]}
• Nội dung: {content_text[self.content_var.get()]}
• Hiển thị: {display_text[self.display_var.get()]}"""
        
        self.preview_label.config(text=preview, foreground="black")
        
    def confirm(self):
        self.result = {
            'difficulty': self.difficulty_var.get(),
            'content_type': self.content_var.get(),
            'display_mode': self.display_var.get()
        }
        self.dialog.destroy()
        
    def cancel(self):
        self.result = None
        self.dialog.destroy()