import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from data_manager import DataManager
from calculator import Calculator
from statistics_manager import StatisticsManager
from mode_selection_dialog import ModeSelectionDialog

class TypingTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TypingMaster Pro")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Set modern color scheme
        self.colors = {
            'primary': '#2E3440',
            'secondary': '#3B4252', 
            'accent': '#5E81AC',
            'success': '#A3BE8C',
            'warning': '#EBCB8B',
            'error': '#BF616A',
            'text_primary': '#ECEFF4',
            'text_secondary': '#D8DEE9',
            'background': '#ECEFF4',
            'surface': '#FFFFFF',
            'gradient_start': '#5E81AC',
            'gradient_end': '#81A1C1'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['background'])
        
        # Configure modern styles
        self.setup_styles()
        
        self.data_manager = DataManager()
        self.calculator = Calculator()
        self.stats_manager = StatisticsManager()
        
        self.current_text = ""
        self.user_input = ""
        self.start_time = None
        self.is_started = False
        self.is_finished = False
        
        # Word by word mode variables
        self.display_mode = "full_sentence"
        self.words_list = []
        self.current_word_index = 0
        self.completed_words = []
        
        self.setup_ui()
        self.current_text = ""
        self.check_initial_state()
        
    def setup_styles(self):
        style = ttk.Style()
        
        # Configure modern button style
        style.configure('Modern.TButton',
                       background=self.colors['accent'],
                       foreground='black',
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 10))
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['gradient_end']),
                           ('pressed', self.colors['secondary'])])
        
        # Configure primary button
        style.configure('Primary.TButton',
                       background=self.colors['success'],
                       foreground='black',
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(25, 12))
        
        style.map('Primary.TButton',
                 background=[('active', '#93AE83'),
                           ('pressed', self.colors['secondary'])])
        
        # Configure danger button
        style.configure('Danger.TButton',
                       background=self.colors['error'],
                       foreground='black',
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 10))
        
        # Configure modern frame
        style.configure('Card.TFrame',
                       background=self.colors['surface'],
                       relief='flat',
                       borderwidth=0)
        
        # Configure modern labelframe
        style.configure('Card.TLabelframe',
                       background=self.colors['surface'],
                       relief='flat',
                       borderwidth=1,
                       lightcolor=self.colors['text_secondary'],
                       darkcolor=self.colors['text_secondary'])
        
        style.configure('Card.TLabelframe.Label',
                       background=self.colors['surface'],
                       foreground=self.colors['secondary'],
                       font=('Segoe UI', 11, 'bold'))
        
        # Configure modern progressbar
        style.configure('Modern.Horizontal.TProgressbar',
                       background=self.colors['accent'],
                       troughcolor=self.colors['text_secondary'],
                       borderwidth=0,
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'])
        
    def setup_ui(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header section with gradient effect
        header_frame = tk.Frame(main_container, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title with modern typography
        title_label = tk.Label(header_frame, 
                              text="TypingMaster Pro",
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['text_primary'],
                              bg=self.colors['primary'])
        title_label.pack(pady=20)
        
        # Create scrollable content area
        self.setup_scrollable_content(main_container)
        
    def setup_scrollable_content(self, parent):
        # Create canvas and scrollbar for scrollable content
        canvas_frame = tk.Frame(parent, bg=self.colors['background'])
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        # Create scrollable frame
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Content frame inside scrollable area with 3 columns
        content_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        content_frame.columnconfigure(0, weight=1)  # Live Stats column
        content_frame.columnconfigure(1, weight=3)  # Main content column (widest)
        content_frame.columnconfigure(2, weight=1)  # Actions column
        
        # Left column frame (Live Stats)
        left_frame = tk.Frame(content_frame, bg=self.colors['background'])
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        
        # Middle column frame (Main content)
        middle_frame = tk.Frame(content_frame, bg=self.colors['background'])
        middle_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        middle_frame.columnconfigure(0, weight=1)
        
        # Right column frame (Actions)
        right_frame = tk.Frame(content_frame, bg=self.colors['background'])
        right_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        right_frame.columnconfigure(0, weight=1)
        
        # Setup content in columns
        self.setup_stats_card(left_frame)
        
        # Setup main content in middle column
        self.setup_text_display_card(middle_frame)
        self.setup_input_card(middle_frame)
        self.setup_mode_info_card(middle_frame)
        
        # Setup actions in right column
        self.setup_action_buttons(right_frame)
        
    def create_card(self, parent, title=None, **kwargs):
        """Create a modern card-style frame"""
        card_frame = tk.Frame(parent, bg=self.colors['surface'], relief='flat', bd=0)
        card_frame.pack(fill=tk.BOTH, expand=True, pady=15, padx=10)
        
        if title:
            title_frame = tk.Frame(card_frame, bg=self.colors['surface'])
            title_frame.pack(fill=tk.X, padx=25, pady=(20, 0))
            
            tk.Label(title_frame, text=title, 
                    font=('Segoe UI', 14, 'bold'),
                    fg=self.colors['secondary'],
                    bg=self.colors['surface']).pack(anchor=tk.W)
            
            # Add accent line
            accent_line = tk.Frame(title_frame, bg=self.colors['accent'], height=3)
            accent_line.pack(fill=tk.X, pady=(5, 0))
        
        return card_frame
    
    def setup_mode_info_card(self, parent):
        self.mode_card = self.create_card(parent, "Current Mode", row=0, pady=(0, 15))
        
        mode_content = tk.Frame(self.mode_card, bg=self.colors['surface'])
        mode_content.pack(fill=tk.X, padx=25, pady=(10, 25))
        
        self.mode_info_label = tk.Label(mode_content, 
                                       text="",
                                       font=('Segoe UI', 11),
                                       fg=self.colors['text_secondary'],
                                       bg=self.colors['surface'])
        self.mode_info_label.pack(anchor=tk.W)
        
    def setup_text_display_card(self, parent):
        text_card = self.create_card(parent, "Text to Type", row=1, pady=15)
        
        text_content = tk.Frame(text_card, bg=self.colors['surface'])
        text_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=(10, 25))
        
        # Text display with modern styling
        text_frame = tk.Frame(text_content, bg=self.colors['background'], relief='flat', bd=1)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_display = tk.Text(text_frame, 
                                   height=8, 
                                   font=('Consolas', 14),
                                   wrap=tk.WORD,
                                   state=tk.DISABLED,
                                   bg=self.colors['background'],
                                   fg=self.colors['secondary'],
                                   relief='flat',
                                   bd=0,
                                   padx=20,
                                   pady=20,
                                   selectbackground=self.colors['accent'])
        self.text_display.pack(fill=tk.BOTH, expand=True)
        
    def setup_input_card(self, parent):
        input_card = self.create_card(parent, "Your Input", row=2, pady=15)
        
        input_content = tk.Frame(input_card, bg=self.colors['surface'])
        input_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=(10, 25))
        
        # Progress bar
        progress_frame = tk.Frame(input_content, bg=self.colors['surface'])
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(progress_frame, text="Progress:", 
                font=('Segoe UI', 10, 'bold'),
                fg=self.colors['secondary'],
                bg=self.colors['surface']).pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                          style='Modern.Horizontal.TProgressbar',
                                          mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Input text area
        input_frame = tk.Frame(input_content, bg=self.colors['background'], relief='flat', bd=1)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        self.input_entry = tk.Text(input_frame, 
                                  height=6,
                                  font=('Consolas', 14),
                                  wrap=tk.WORD,
                                  bg=self.colors['background'],
                                  fg=self.colors['secondary'],
                                  relief='flat',
                                  bd=0,
                                  padx=20,
                                  pady=20,
                                  selectbackground=self.colors['accent'],
                                  insertbackground=self.colors['accent'])
        self.input_entry.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.input_entry.bind('<KeyRelease>', self.on_key_release)
        self.input_entry.bind('<Button-1>', self.on_click)
        self.input_entry.bind('<Return>', self.on_enter_pressed)
        self.input_entry.bind('<space>', self.on_space_pressed)
        
        # Input hint
        hint_label = tk.Label(input_content,
                             text="💡 Start typing to begin the test • Press Enter to finish",
                             font=('Segoe UI', 10),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['surface'])
        hint_label.pack(anchor=tk.W, pady=(10, 0))
        
    def setup_stats_card(self, parent):
        # Real-time stats card
        stats_card = self.create_card(parent, "Live Stats", row=0, pady=(0, 15))
        
        stats_content = tk.Frame(stats_card, bg=self.colors['surface'])
        stats_content.pack(fill=tk.X, padx=25, pady=(10, 25))
        
        # Stats grid
        stats_grid = tk.Frame(stats_content, bg=self.colors['surface'])
        stats_grid.pack(fill=tk.X)
        stats_grid.columnconfigure(0, weight=1)
        
        # WPM
        wpm_frame = tk.Frame(stats_grid, bg=self.colors['surface'])
        wpm_frame.grid(row=0, column=0, sticky="w", pady=5)
        
        tk.Label(wpm_frame, text="WPM", 
                font=('Segoe UI', 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['surface']).pack(anchor=tk.W)
        
        self.wpm_var = tk.StringVar(value="0")
        tk.Label(wpm_frame, textvariable=self.wpm_var,
                font=('Segoe UI', 18, 'bold'),
                fg=self.colors['accent'],
                bg=self.colors['surface']).pack(anchor=tk.W)
        
        # Accuracy
        acc_frame = tk.Frame(stats_grid, bg=self.colors['surface'])
        acc_frame.grid(row=1, column=0, sticky="w", pady=5)
        
        tk.Label(acc_frame, text="Accuracy", 
                font=('Segoe UI', 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['surface']).pack(anchor=tk.W)
        
        self.accuracy_var = tk.StringVar(value="100%")
        tk.Label(acc_frame, textvariable=self.accuracy_var,
                font=('Segoe UI', 18, 'bold'),
                fg=self.colors['success'],
                bg=self.colors['surface']).pack(anchor=tk.W)
        
        # Time
        time_frame = tk.Frame(stats_grid, bg=self.colors['surface'])
        time_frame.grid(row=2, column=0, sticky="w", pady=5)
        
        tk.Label(time_frame, text="Time", 
                font=('Segoe UI', 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['surface']).pack(anchor=tk.W)
        
        self.time_var = tk.StringVar(value="00:00")
        tk.Label(time_frame, textvariable=self.time_var,
                font=('Segoe UI', 18, 'bold'),
                fg=self.colors['warning'],
                bg=self.colors['surface']).pack(anchor=tk.W)
        
        # Words -> Characters
        chars_frame = tk.Frame(stats_grid, bg=self.colors['surface'])
        chars_frame.grid(row=3, column=0, sticky="w", pady=5)
        
        tk.Label(chars_frame, text="Characters", 
                font=('Segoe UI', 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['surface']).pack(anchor=tk.W)
        
        self.chars_var = tk.StringVar(value="0/0")
        tk.Label(chars_frame, textvariable=self.chars_var,
                font=('Segoe UI', 18, 'bold'),
                fg=self.colors['secondary'],
                bg=self.colors['surface']).pack(anchor=tk.W)
        
        # Quick actions inside stats card
        actions_section = tk.Frame(stats_content, bg=self.colors['surface'])
        actions_section.pack(fill=tk.X, pady=(20, 0))
        
        # Actions title
        tk.Label(actions_section, text="Quick Actions", 
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['secondary'],
                bg=self.colors['surface']).pack(anchor=tk.W, pady=(0, 10))
        
        # Quick action buttons
        ttk.Button(actions_section, text="🔄 New Text", 
                  style='Modern.TButton',
                  command=self.load_new_text).pack(fill=tk.X, pady=2)
        
        ttk.Button(actions_section, text="⚙️ Change Mode", 
                  style='Modern.TButton',
                  command=self.change_mode).pack(fill=tk.X, pady=2)
        
        ttk.Button(actions_section, text="🔄 Reset", 
                  style='Modern.TButton',
                  command=self.reset_test).pack(fill=tk.X, pady=2)
        
    def setup_action_buttons(self, parent):
        button_card = self.create_card(parent, "Main Actions", row=1, pady=15)
        
        button_content = tk.Frame(button_card, bg=self.colors['surface'])
        button_content.pack(fill=tk.X, padx=25, pady=(10, 25))
        
        # Main action buttons
        ttk.Button(button_content, text="📁 Import File", 
                  style='Primary.TButton',
                  command=self.import_csv).pack(fill=tk.X, pady=5)
        
        ttk.Button(button_content, text="➕ Add Text", 
                  style='Modern.TButton',
                  command=self.add_custom_text).pack(fill=tk.X, pady=5)
        
        ttk.Button(button_content, text="📊 Statistics", 
                  style='Modern.TButton',
                  command=self.show_statistics).pack(fill=tk.X, pady=5)
        
    def setup_results_card(self, parent):
        results_card = self.create_card(parent, "Test Results", row=5, pady=15)
        
        results_content = tk.Frame(results_card, bg=self.colors['surface'])
        results_content.pack(fill=tk.BOTH, expand=True, padx=25, pady=(10, 25))
        
        results_frame = tk.Frame(results_content, bg=self.colors['background'], relief='flat', bd=1)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(results_frame, 
                                  height=8, 
                                  state=tk.DISABLED,
                                  font=('Segoe UI', 11),
                                  bg=self.colors['background'],
                                  fg=self.colors['secondary'],
                                  relief='flat',
                                  bd=0,
                                  padx=20,
                                  pady=20,
                                  selectbackground=self.colors['accent'])
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
    # Keep all the original methods unchanged
    def check_initial_state(self):
        if not self.data_manager.texts:
            self.input_entry.config(state=tk.DISABLED)
        else:
            self.input_entry.config(state=tk.NORMAL)
    
    def show_mode_selection(self):
        """Hiển thị dialog chọn mode"""
        dialog = ModeSelectionDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.data_manager.set_preferences(dialog.result)
            self.display_mode = dialog.result['display_mode']
            self.update_mode_info(dialog.result)
            return True
        return False
    
    def update_mode_info(self, preferences):
        """Cập nhật hiển thị thông tin mode"""
        difficulty_text = {
            "easy": "Easy (0-25 chars)",
            "medium": "Medium (26-60 chars)", 
            "hard": "Hard (61+ chars)"
        }
        
        content_text = {
            "letters_only": "Letters only",
            "with_special": "With numbers & symbols"
        }
        
        display_text = {
            "full_sentence": "Full sentence",
            "word_by_word": "Word by word"
        }
        
        mode_info = f"🎯 {difficulty_text[preferences['difficulty']]} • {content_text[preferences['content_type']]} • {display_text[preferences['display_mode']]}"
        self.mode_info_label.config(text=mode_info, fg=self.colors['accent'])
    
    def change_mode(self):
        """Thay đổi mode"""
        if not self.data_manager.texts:
            messagebox.showwarning("No Data", "Please import a file first!")
            return
        
        if self.show_mode_selection():
            self.load_new_text()
            
    def load_new_text(self):
        if not self.data_manager.texts:
            messagebox.showwarning("No Data", "Please import a file first!")
            return
            
        try:
            # Sử dụng filtered text theo preferences
            self.current_text = self.data_manager.get_filtered_text()
            
            if not self.current_text:
                messagebox.showwarning("No Match", "No matching sentences found. Loading random sentence...")
                self.current_text = self.data_manager.get_random_text()
            
            # Prepare for word by word mode
            if self.display_mode == "word_by_word":
                self.words_list = self.current_text.split()
                self.current_word_index = 0
                self.completed_words = []
            
            self.display_text()
            self.reset_test()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load text: {str(e)}")
            
    def display_text(self):
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        
        if self.display_mode == "word_by_word":
            self.display_word_by_word()
        else:
            self.text_display.insert(1.0, self.current_text)
            
        self.text_display.config(state=tk.DISABLED)
    
    def display_word_by_word(self):
        """Hiển thị theo mode word by word"""
        if not self.words_list:
            return
            
        display_text = ""
        
        # Hiển thị các từ đã hoàn thành với màu xanh lá
        for word in self.completed_words:
            display_text += word + " "
            
        # Hiển thị từ hiện tại (không có ngoặc vuông)
        if self.current_word_index < len(self.words_list):
            current_word = self.words_list[self.current_word_index]
            display_text += current_word
            
            # Hiển thị preview các từ tiếp theo với màu xám nhạt
            remaining_words = self.words_list[self.current_word_index + 1:]
            if remaining_words:
                display_text += " " + " ".join(remaining_words[:5])  # Hiển thị tối đa 5 từ tiếp theo
            
        self.text_display.insert(1.0, display_text)
        
        # Tính toán vị trí để highlight từ hiện tại
        completed_text = " ".join(self.completed_words)
        start_pos = len(completed_text)
        if self.completed_words:
            start_pos += 1  # Thêm space sau từ cuối cùng đã hoàn thành
            
        if self.current_word_index < len(self.words_list):
            current_word = self.words_list[self.current_word_index]
            end_pos = start_pos + len(current_word)
            
            # Tag cho các từ đã hoàn thành (màu xanh lá)
            if self.completed_words:
                self.text_display.tag_add("completed_words", "1.0", f"1.{start_pos-1}")
                self.text_display.tag_config("completed_words", 
                                           background=self.colors['success'], 
                                           foreground="white",
                                           font=("Consolas", 14))
            
            # Tag cho từ hiện tại (màu vàng nhạt, không in đậm)
            self.text_display.tag_add("current_word", f"1.{start_pos}", f"1.{end_pos}")
            self.text_display.tag_config("current_word", 
                                       background=self.colors['warning'], 
                                       foreground="black",
                                       font=("Consolas", 14))
            
            # Tag cho các từ sắp tới (màu xám nhạt)
            remaining_start = end_pos
            if remaining_start < len(display_text):
                self.text_display.tag_add("upcoming_words", f"1.{remaining_start}", "end")
                self.text_display.tag_config("upcoming_words", 
                                           background=self.colors['background'], 
                                           foreground=self.colors['text_secondary'],
                                           font=("Consolas", 14))
        
        # Fix vấn đề selection color
        self.text_display.tag_config("sel", background=self.colors['accent'], foreground="white")
    
    def on_space_pressed(self, event):
        """Xử lý khi nhấn space trong word by word mode"""
        if self.display_mode == "word_by_word" and self.is_started:
            typed_word = self.input_entry.get(1.0, tk.END).strip()
            
            if self.current_word_index < len(self.words_list):
                expected_word = self.words_list[self.current_word_index]
                
                # Kiểm tra từ vừa gõ
                if typed_word == expected_word:
                    self.completed_words.append(typed_word)
                else:
                    self.completed_words.append(f"({typed_word})")  # Đánh dấu từ sai
                
                self.current_word_index += 1
                self.input_entry.delete(1.0, tk.END)
                
                # Cập nhật hiển thị
                self.display_text()
                self.update_real_time_stats()
                
                # Kiểm tra hoàn thành
                if self.current_word_index >= len(self.words_list):
                    self.finish_test()
                    
            return 'break'  # Ngăn space được thêm vào text widget
    
    def reset_test(self):
        if not self.data_manager.texts:
            messagebox.showwarning("No Data", "Please import a file first!")
            return
            
        self.user_input = ""
        self.start_time = None
        self.is_started = False
        self.is_finished = False
        
        # Reset word by word mode
        if self.display_mode == "word_by_word":
            self.current_word_index = 0
            self.completed_words = []
        
        self.input_entry.delete(1.0, tk.END)
        self.progress_bar['value'] = 0
        self.wpm_var.set("0")
        self.accuracy_var.set("100%")
        self.time_var.set("00:00")
        
        if self.display_mode == "word_by_word":
            total_chars_in_text = len(" ".join(self.words_list)) if self.words_list else 0
            self.chars_var.set(f"0/{total_chars_in_text}")
        else:
            self.chars_var.set("0/" + str(len(self.current_text)) if self.current_text else "0/0")
        
        if hasattr(self, 'current_text') and self.current_text:
            self.update_text_highlighting()
        
    def on_click(self, event):
        if not self.is_started and not self.is_finished:
            self.start_test()
            
    def on_enter_pressed(self, event):
        if self.is_started and not self.is_finished:
            self.finish_test()
            # After finishing test, load new text automatically
            self.root.after(100, self.load_new_text)  # Small delay to let finish_test complete
        elif not self.is_started:
            # If no test is running, load new text
            self.load_new_text()
        return 'break'
            
    def on_key_release(self, event):
        if event.keysym == 'Return':
            return
        
        if event.keysym == 'space' and self.display_mode == "word_by_word":
            return  # Đã xử lý trong on_space_pressed
            
        if not self.is_started and not self.is_finished:
            self.start_test()
            
        self.user_input = self.input_entry.get(1.0, tk.END).rstrip('\n')
        self.update_real_time_stats()
        
        if self.display_mode == "full_sentence":
            self.update_text_highlighting()
            
            if len(self.user_input) >= len(self.current_text):
                self.finish_test()
        
    def start_test(self):
        if not self.is_started:
            self.is_started = True
            self.start_time = time.time()
            
    def update_real_time_stats(self):
        if not self.is_started or self.start_time is None:
            return
            
        try:
            elapsed_time = time.time() - self.start_time
            
            if self.display_mode == "word_by_word":
                # Tính toán cho word by word mode
                total_chars = sum(len(word) for word in self.completed_words)
                wpm = self.calculator.calculate_wpm(" ".join(self.completed_words), elapsed_time)
                
                correct_words = sum(1 for i, word in enumerate(self.completed_words) 
                                  if i < len(self.words_list) and word == self.words_list[i])
                accuracy = (correct_words / max(len(self.completed_words), 1)) * 100 if self.completed_words else 100
                
                progress = (len(self.completed_words) / len(self.words_list)) * 100 if self.words_list else 0
                total_chars_in_text = len(" ".join(self.words_list)) if self.words_list else 0
                typed_chars = len(" ".join(self.completed_words))
                self.chars_var.set(f"{typed_chars}/{total_chars_in_text}")
                
            else:
                # Tính toán cho full sentence mode
                wpm = self.calculator.calculate_wpm(self.user_input, elapsed_time)
                accuracy = self.calculator.calculate_accuracy(self.current_text, self.user_input)
                progress = min(len(self.user_input) / len(self.current_text) * 100, 100)
                self.chars_var.set(f"{len(self.user_input)}/{len(self.current_text)}")
            
            self.wpm_var.set(f"{wpm:.1f}")
            self.accuracy_var.set(f"{accuracy:.1f}%")
            self.time_var.set(f"{int(elapsed_time//60):02d}:{int(elapsed_time%60):02d}")
            self.progress_bar['value'] = progress
            
        except Exception:
            pass
            
    def update_text_highlighting(self):
        if self.display_mode == "word_by_word":
            return  # Không cần highlighting cho word by word mode
            
        self.text_display.config(state=tk.NORMAL)
        self.text_display.tag_remove("correct", 1.0, tk.END)
        self.text_display.tag_remove("incorrect", 1.0, tk.END)
        self.text_display.tag_remove("current", 1.0, tk.END)
        
        for i, char in enumerate(self.user_input):
            pos = f"1.{i}"
            end_pos = f"1.{i+1}"
            
            if i < len(self.current_text):
                if char == self.current_text[i]:
                    self.text_display.tag_add("correct", pos, end_pos)
                else:
                    self.text_display.tag_add("incorrect", pos, end_pos)
                    
        if len(self.user_input) < len(self.current_text):
            current_pos = f"1.{len(self.user_input)}"
            current_end_pos = f"1.{len(self.user_input)+1}"
            self.text_display.tag_add("current", current_pos, current_end_pos)
            
        self.text_display.tag_config("correct", background=self.colors['success'])
        self.text_display.tag_config("incorrect", background=self.colors['error'])
        self.text_display.tag_config("current", background=self.colors['warning'])
        
        self.text_display.config(state=tk.DISABLED)
        
    def finish_test(self):
        if self.is_finished:
            return
            
        self.is_finished = True
        elapsed_time = time.time() - self.start_time
        
        try:
            if self.display_mode == "word_by_word":
                # Tính kết quả cho word by word mode
                typed_text = " ".join(self.completed_words)
                wpm = self.calculator.calculate_wpm(typed_text, elapsed_time)
                
                correct_words = sum(1 for i, word in enumerate(self.completed_words) 
                                  if i < len(self.words_list) and word == self.words_list[i])
                accuracy = (correct_words / len(self.words_list)) * 100 if self.words_list else 0
                
            else:
                # Tính kết quả cho full sentence mode
                wpm = self.calculator.calculate_wpm(self.user_input, elapsed_time)
                accuracy = self.calculator.calculate_accuracy(self.current_text, self.user_input)
            
            result = {
                'wpm': wpm,
                'accuracy': accuracy,
                'time': elapsed_time,
                'text_length': len(self.current_text),
                'user_length': len(self.user_input) if self.display_mode == "full_sentence" else len(" ".join(self.completed_words)),
                'mode': self.display_mode
            }
            
            self.stats_manager.save_result(result)
            # Show completion message in a simple messagebox instead of result_text
            mode_text = "Word by Word" if result.get('mode') == "word_by_word" else "Full Sentence"
            message = f"""Test Completed! (Mode: {mode_text})

Time: {int(result['time']//60):02d}:{int(result['time']%60):02d}
Speed: {result['wpm']:.2f} WPM  
Accuracy: {result['accuracy']:.2f}%
Characters: {result['user_length']}/{result['text_length']}

{self.get_performance_message(result['wpm'], result['accuracy'])}"""
            
            messagebox.showinfo("Test Complete", message)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate results: {str(e)}")
            
    def display_final_results(self, result):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        mode_text = "Word by Word" if result.get('mode') == "word_by_word" else "Full Sentence"
        
        # Create formatted results with better styling
        results_str = f"""✨ Test Completed Successfully! ✨
Mode: {mode_text}

⏱️  Time: {int(result['time']//60):02d}:{int(result['time']%60):02d}
🚀 Speed: {result['wpm']:.2f} WPM
🎯 Accuracy: {result['accuracy']:.2f}%
📝 Characters: {result['user_length']}/{result['text_length']}
📊 Completion: {(result['user_length']/result['text_length']*100):.1f}%

{self.get_performance_message(result['wpm'], result['accuracy'])}"""
        
        self.result_text.insert(1.0, results_str)
        self.result_text.config(state=tk.DISABLED)
        
    def get_performance_message(self, wpm, accuracy):
        if wpm >= 60 and accuracy >= 95:
            return "🏆 Excellent! Professional typing speed!"
        elif wpm >= 40 and accuracy >= 90:
            return "🎉 Great job! Above average performance."
        elif wpm >= 25 and accuracy >= 85:
            return "👍 Good work! Keep practicing."
        else:
            return "💪 Keep practicing to improve your speed and accuracy."
            
    def import_csv(self):
        from tkinter import filedialog
        
        try:
            filename = filedialog.askopenfilename(
                title="Import Text File",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            if filename:
                count = self.data_manager.import_txt_file(filename)
                if count > 0:
                    self.input_entry.config(state=tk.NORMAL)
                    self.input_entry.delete(1.0, tk.END)
                    
                    # Hiển thị mode selection dialog sau khi import thành công
                    if self.show_mode_selection():
                        self.load_new_text()
                        messagebox.showinfo("Success", f"Successfully imported {count} new texts!\n\nReady to start typing practice!")
                    else:
                        messagebox.showinfo("Import Success", f"Successfully imported {count} new texts!\nPlease select mode to start practicing.")
                else:
                    # Show debug info nếu không import được
                    try:
                        with open(filename, 'r', encoding='utf-8') as f:
                            preview = f.read(200)
                            
                        messagebox.showwarning("No Import", 
                            f"No new texts were imported.\n\n" +
                            f"File preview (first 200 chars):\n{preview[:100]}...\n\n" +
                            "Possible reasons:\n" +
                            "• All texts already exist\n" +
                            "• Lines are too short (need 10+ characters)\n" +
                            "• File encoding issues\n\n" +
                            "Format: One sentence per line\n" +
                            "Example:\n" +
                            "This is the first sentence.\n" +
                            "This is the second sentence.")
                    except:
                        messagebox.showwarning("No Import", 
                            "No new texts were imported.\n\n" +
                            "File could not be read. Try a different file format.")
                    
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import file:\n\n{str(e)}")
            
    def add_custom_text(self):
        if not self.data_manager.texts:
            messagebox.showwarning("No Data", "Please import a file first!")
            return
            
        dialog = CustomTextDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                self.data_manager.add_text(dialog.result)
                self.load_new_text()
                messagebox.showinfo("Success", "Text added successfully to DATA.txt!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add text: {str(e)}")
                
    def show_statistics(self):
        try:
            stats_window = StatisticsWindow(self.root, self.stats_manager)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load statistics: {str(e)}")

# Các class khác giữ nguyên như CustomTextDialog và StatisticsWindow...
class CustomTextDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Text")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.result = None
        
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Enter new text (will be added to DATA.txt):", 
                 font=("Arial", 12)).pack(anchor=tk.W, pady=(0, 10))
        
        self.text_widget = tk.Text(main_frame, height=15, width=60, 
                                  font=("Arial", 11), wrap=tk.WORD)
        self.text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Cancel", 
                  command=self.cancel).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Add Text", 
                  command=self.add_text).pack(side=tk.RIGHT)
        
    def add_text(self):
        text = self.text_widget.get(1.0, tk.END).strip()
        if len(text) >= 10:
            self.result = text
            self.dialog.destroy()
        else:
            messagebox.showwarning("Invalid Input", 
                                 "Text must be at least 10 characters long.")
            
    def cancel(self):
        self.dialog.destroy()

class StatisticsWindow:
    def __init__(self, parent, stats_manager):
        self.window = tk.Toplevel(parent)
        self.window.title("Statistics")
        self.window.geometry("600x500")
        self.window.transient(parent)
        
        self.stats_manager = stats_manager
        
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Your Typing Statistics", 
                 font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        self.stats_text = tk.Text(main_frame, font=("Courier", 10), 
                                 state=tk.DISABLED)
        self.stats_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Clear All Data", 
                  command=self.clear_data).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Close", 
                  command=self.window.destroy).pack(side=tk.RIGHT)
        
        self.load_statistics()
        
    def load_statistics(self):
        try:
            stats = self.stats_manager.get_statistics()
            
            self.stats_text.config(state=tk.NORMAL)
            self.stats_text.delete(1.0, tk.END)
            
            if not stats['results']:
                self.stats_text.insert(1.0, "No typing tests completed yet.")
            else:
                stats_str = f"""OVERALL STATISTICS
==================
Total Tests: {stats['total_tests']}
Average WPM: {stats['avg_wpm']:.2f}
Best WPM: {stats['best_wpm']:.2f}
Average Accuracy: {stats['avg_accuracy']:.2f}%
Best Accuracy: {stats['best_accuracy']:.2f}%
Total Time Practiced: {stats['total_time']:.0f} seconds

RECENT RESULTS (Last 10)
========================
"""
                
                for i, result in enumerate(stats['recent_results'][:10], 1):
                    mode_info = f" ({result.get('mode', 'full_sentence')})" if 'mode' in result else ""
                    stats_str += f"{i:2d}. {result['wpm']:5.1f} WPM | {result['accuracy']:5.1f}% | {int(result['time']):3d}s{mode_info}\n"
                    
            self.stats_text.insert(1.0, stats_str)
            self.stats_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.stats_text.config(state=tk.NORMAL)
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, f"Error loading statistics: {str(e)}")
            self.stats_text.config(state=tk.DISABLED)
            
    def clear_data(self):
        if messagebox.askyesno("Confirm", 
                              "Are you sure you want to clear all statistics?"):
            try:
                self.stats_manager.clear_all_data()
                self.load_statistics()
                messagebox.showinfo("Success", "All data cleared successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear data: {str(e)}")