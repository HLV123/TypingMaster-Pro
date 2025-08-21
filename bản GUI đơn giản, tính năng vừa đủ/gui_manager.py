import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from data_manager import DataManager
from calculator import Calculator
from statistics_manager import StatisticsManager

class TypingTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.data_manager = DataManager()
        self.calculator = Calculator()
        self.stats_manager = StatisticsManager()
        
        self.current_text = ""
        self.user_input = ""
        self.start_time = None
        self.is_started = False
        self.is_finished = False
        
        self.setup_ui()
        self.current_text = ""
        self.check_initial_state()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        title_label = ttk.Label(main_frame, text="Typing Speed Test", 
                               font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        self.text_display = tk.Text(main_frame, height=6, width=70, 
                                   font=("Courier", 14), wrap=tk.WORD,
                                   state=tk.DISABLED)
        self.text_display.grid(row=1, column=0, columnspan=3, pady=(0, 20), 
                              sticky=(tk.W, tk.E))
        
        input_label = ttk.Label(main_frame, text="Type here (Press Enter to finish):", 
                               font=("Arial", 12))
        input_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        
        self.input_entry = tk.Text(main_frame, height=4, width=70, 
                                  font=("Courier", 14), wrap=tk.WORD)
        self.input_entry.grid(row=3, column=0, columnspan=3, pady=(0, 20),
                             sticky=(tk.W, tk.E))
        self.input_entry.bind('<KeyRelease>', self.on_key_release)
        self.input_entry.bind('<Button-1>', self.on_click)
        self.input_entry.bind('<Return>', self.on_enter_pressed)
        
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=4, column=0, columnspan=3, pady=(0, 20), 
                           sticky=(tk.W, tk.E))
        progress_frame.columnconfigure(1, weight=1)
        
        ttk.Label(progress_frame, text="Progress:").grid(row=0, column=0, 
                                                        sticky=tk.W)
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        stats_frame = ttk.LabelFrame(main_frame, text="Real-time Stats", 
                                    padding="10")
        stats_frame.grid(row=5, column=0, columnspan=3, pady=(0, 20), 
                        sticky=(tk.W, tk.E))
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(3, weight=1)
        
        ttk.Label(stats_frame, text="WPM:").grid(row=0, column=0, sticky=tk.W)
        self.wpm_var = tk.StringVar(value="0")
        ttk.Label(stats_frame, textvariable=self.wpm_var, 
                 font=("Arial", 12, "bold")).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(stats_frame, text="Accuracy:").grid(row=0, column=2, 
                                                     sticky=tk.W, padx=(20, 0))
        self.accuracy_var = tk.StringVar(value="100%")
        ttk.Label(stats_frame, textvariable=self.accuracy_var, 
                 font=("Arial", 12, "bold")).grid(row=0, column=3, sticky=tk.W)
        
        ttk.Label(stats_frame, text="Time:").grid(row=1, column=0, sticky=tk.W)
        self.time_var = tk.StringVar(value="00:00")
        ttk.Label(stats_frame, textvariable=self.time_var, 
                 font=("Arial", 12, "bold")).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(stats_frame, text="Characters:").grid(row=1, column=2, 
                                                       sticky=tk.W, padx=(20, 0))
        self.chars_var = tk.StringVar(value="0/0")
        ttk.Label(stats_frame, textvariable=self.chars_var, 
                 font=("Arial", 12, "bold")).grid(row=1, column=3, sticky=tk.W)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=(0, 20))
        
        ttk.Button(button_frame, text="Import File", 
                  command=self.import_csv).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="New Text", 
                  command=self.load_new_text).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Reset", 
                  command=self.reset_test).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Add Text", 
                  command=self.add_custom_text).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="View Statistics", 
                  command=self.show_statistics).pack(side=tk.LEFT)
        
        result_frame = ttk.LabelFrame(main_frame, text="Final Results", 
                                     padding="10")
        result_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E))
        result_frame.columnconfigure(1, weight=1)
        
        self.result_text = tk.Text(result_frame, height=6, state=tk.DISABLED,
                                  font=("Arial", 10))
        self.result_text.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
    def check_initial_state(self):
        if not self.data_manager.texts:
            self.input_entry.config(state=tk.DISABLED)
        else:
            self.input_entry.config(state=tk.NORMAL)
            
    def load_new_text(self):
        if not self.data_manager.texts:
            messagebox.showwarning("No Data", "Chưa import file. Vui lòng import file trước!")
            return
            
        try:
            self.current_text = self.data_manager.get_random_text()
            self.display_text()
            self.reset_test()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load text: {str(e)}")
            
    def display_text(self):
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(1.0, self.current_text)
        self.text_display.config(state=tk.DISABLED)
        
    def reset_test(self):
        if not self.data_manager.texts:
            messagebox.showwarning("No Data", "Chưa import file. Vui lòng import file trước!")
            return
            
        self.user_input = ""
        self.start_time = None
        self.is_started = False
        self.is_finished = False
        
        self.input_entry.delete(1.0, tk.END)
        self.progress_bar['value'] = 0
        self.wpm_var.set("0")
        self.accuracy_var.set("100%")
        self.time_var.set("00:00")
        self.chars_var.set("0/" + str(len(self.current_text)) if hasattr(self, 'current_text') and self.current_text else "0/0")
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        if hasattr(self, 'current_text') and self.current_text:
            self.update_text_highlighting()
        
    def on_click(self, event):
        if not self.is_started and not self.is_finished:
            self.start_test()
            
    def on_enter_pressed(self, event):
        if self.is_started and not self.is_finished:
            self.finish_test()
        return 'break'
            
    def on_key_release(self, event):
        if event.keysym == 'Return':
            return
            
        if not self.is_started and not self.is_finished:
            self.start_test()
            
        self.user_input = self.input_entry.get(1.0, tk.END).rstrip('\n')
        self.update_real_time_stats()
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
            
            wpm = self.calculator.calculate_wpm(self.user_input, elapsed_time)
            accuracy = self.calculator.calculate_accuracy(self.current_text, 
                                                        self.user_input)
            
            progress = min(len(self.user_input) / len(self.current_text) * 100, 100)
            
            self.wpm_var.set(f"{wpm:.1f}")
            self.accuracy_var.set(f"{accuracy:.1f}%")
            self.time_var.set(f"{int(elapsed_time//60):02d}:{int(elapsed_time%60):02d}")
            self.chars_var.set(f"{len(self.user_input)}/{len(self.current_text)}")
            self.progress_bar['value'] = progress
            
        except Exception:
            pass
            
    def update_text_highlighting(self):
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
            
        self.text_display.tag_config("correct", background="lightgreen")
        self.text_display.tag_config("incorrect", background="lightcoral")
        self.text_display.tag_config("current", background="lightyellow")
        
        self.text_display.config(state=tk.DISABLED)
        
    def finish_test(self):
        if self.is_finished:
            return
            
        self.is_finished = True
        elapsed_time = time.time() - self.start_time
        
        try:
            wpm = self.calculator.calculate_wpm(self.user_input, elapsed_time)
            accuracy = self.calculator.calculate_accuracy(self.current_text, 
                                                        self.user_input)
            
            result = {
                'wpm': wpm,
                'accuracy': accuracy,
                'time': elapsed_time,
                'text_length': len(self.current_text),
                'user_length': len(self.user_input)
            }
            
            self.stats_manager.save_result(result)
            self.display_final_results(result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate results: {str(e)}")
            
    def display_final_results(self, result):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        results_str = f"""Test Completed!
        
Time: {int(result['time']//60):02d}:{int(result['time']%60):02d}
Speed: {result['wpm']:.2f} WPM
Accuracy: {result['accuracy']:.2f}%
Characters: {result['user_length']}/{result['text_length']}
Completion: {(result['user_length']/result['text_length']*100):.1f}%

{self.get_performance_message(result['wpm'], result['accuracy'])}"""
        
        self.result_text.insert(1.0, results_str)
        self.result_text.config(state=tk.DISABLED)
        
    def get_performance_message(self, wpm, accuracy):
        if wpm >= 60 and accuracy >= 95:
            return "Excellent! Professional typing speed!"
        elif wpm >= 40 and accuracy >= 90:
            return "Great job! Above average performance."
        elif wpm >= 25 and accuracy >= 85:
            return "Good work! Keep practicing."
        else:
            return "Keep practicing to improve your speed and accuracy."
            
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
                    self.load_new_text()  # Reload to show new texts
                    messagebox.showinfo("Success", f"Successfully imported {count} new texts!\n\nReady to start typing practice!")
                else:
                    # Show debug info
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
            messagebox.showwarning("No Data", "Chưa import file. Vui lòng import file trước!")
            return
            
        dialog = CustomTextDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            try:
                self.data_manager.add_text(dialog.result)
                self.load_new_text()  # Reload to show new text
                messagebox.showinfo("Success", "Text added successfully to DATA.txt!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add text: {str(e)}")
                
    def show_statistics(self):
        try:
            stats_window = StatisticsWindow(self.root, self.stats_manager)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load statistics: {str(e)}")

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
                    stats_str += f"{i:2d}. {result['wpm']:5.1f} WPM | {result['accuracy']:5.1f}% | {int(result['time']):3d}s\n"
                    
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