import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, scrolledtext
from datetime import datetime
import threading
import time
import random
import general_chat
import audio
import types
from google.genai import types
import religious
import cook_book
import news2
import json, os
import requests
historygc=[]
historyreligion=[]
historycookbook=[]

class DashboardApp:
    def __init__(self, root):
        self.api_key = "f4e60b8945f94e2e94363218250504"
        self.user_input = ""
        self.username = ""
        self.weather_loc = ""
        
        # Load saved user data if it exists
        self.load_user_data()
        
        # If no username saved, ask for it
        if not self.username:
            self.username = simpledialog.askstring("Username", "Enter your username: ")
            if not self.username:
                self.username = "Guest"
        
        # If no weather location saved, ask for it
        if not self.weather_loc:
            self.weather_loc = simpledialog.askstring("Location", "Enter weather location")
            if not self.weather_loc:
                self.weather_loc = "London"
        
        # Save user data
        self.save_user_data()

        # Main window configuration
        self.root = root
        self.root.title("Dashboard")
        self.root.state("zoomed")        
        # Set up the main container with a border
        self.main_frame = tk.Frame(root, bd=2, relief=tk.SOLID)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create sidebar and content area
        self.sidebar = tk.Frame(self.main_frame, width=150, bd=1, relief=tk.SOLID)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        self.sidebar.pack_propagate(False)  # Prevent sidebar from resizing
        
        self.content_area = tk.Frame(self.main_frame, bd=1, relief=tk.SOLID)
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Initialize active button tracking
        self.active_button = None
        # Load schedule and medication data
        self.schedule_data = self.load_schedule_data()
        self.medication_data = self.load_medication_data()
        # Create sidebar buttons
        self.create_sidebar_buttons()
        self.weather_info()
        
        # Default content is home
        self.show_home()
        
        # Start time update thread
        self.time_thread = threading.Thread(target=self.update_time_continuously)
        self.time_thread.daemon = True
        self.time_thread.start()

    def load_user_data(self):
        if os.path.exists("user_data.json"):
            try:
                with open("user_data.json", "r") as file:
                    data = json.load(file)
                    self.username = data.get("username", "")
                    self.weather_loc = data.get("weather_loc", "")
            except:
                pass

    def save_user_data(self):
        data = {
            "username": self.username,
            "weather_loc": self.weather_loc
        }
        try:
            with open("user_data.json", "w") as file:
                json.dump(data, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user data: {str(e)}")

    def load_schedule_data(self):
        if os.path.exists("schedule_data.json"):
            try:
                with open("schedule_data.json", "r") as file:
                    return json.load(file)
            except:
                pass
        return []

    def save_schedule_data(self):
        try:
            with open("schedule_data.json", "w") as file:
                json.dump(self.schedule_data, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save schedule data: {str(e)}")

    def load_medication_data(self):
        if os.path.exists("medication_data.json"):
            try:
                with open("medication_data.json", "r") as file:
                    return json.load(file)
            except:
                pass
        return []

    def save_medication_data(self):
        try:
            with open("medication_data.json", "w") as file:
                json.dump(self.medication_data, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save medication data: {str(e)}")

    def create_sidebar_buttons(self):
        # List of menu items
        menu_items = [
            ("HOME", self.show_home),
            ("GENERAL CHAT", self.show_general_chat),
            ("RELIGION", self.show_religion),
            ("COOK BOOK", self.show_cookbook),
            ("NEWS", self.show_news),
            #("JOURNAL", self.show_journal),
            ("SCRIBBLE", self.show_scribble),
            ("SCHEDULE", self.show_schedule),
            ("MEDICATIONS", self.show_medications)
        ]
        
        # Create a button for each menu item
        self.buttons = {}
        for text, command in menu_items:
            btn = tk.Button(
                self.sidebar, 
                text=text, 
                command=lambda cmd=command, txt=text: self.button_click(cmd, txt),
                bd=1,
                relief=tk.SOLID,
                width=20,
                anchor=tk.W,
                padx=5,
                height=2
            )
            btn.pack(fill=tk.X, padx=0, pady=0)
            self.buttons[text] = btn
            
            # Add a separator line after each button except the last one
            if text != menu_items[-1][0]:
                separator = tk.Frame(self.sidebar, height=1, bg="black")
                separator.pack(fill=tk.X, padx=0, pady=0)
    
    def button_click(self, command, button_text):
        # Reset previously active button
        if self.active_button:
            self.buttons[self.active_button].config(bg="SystemButtonFace", fg="black")
        
        # Highlight new active button
        self.buttons[button_text].config(bg="lightblue", fg="black")
        self.active_button = button_text
        
        # Execute the command
        command()
    
    def clear_content(self):
        # Remove all widgets from the content area
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def weather_info(self):
        try:
            url = f"https://api.weatherapi.com/v1/forecast.json?key={self.api_key}&q={self.weather_loc}&days=1&aqi=no&alerts=no&units=metric"
            response = requests.get(url)
            data = response.json()
            self.condition = data['current']['condition']['text']
            self.temperature = data['current']['temp_c']
            #print(self.condition,self.temperature)
            self.user_input = self.weather_loc
        except Exception as e:
            self.condition = "Unknown"
            self.temperature = "N/A"
            messagebox.showerror("Weather Error", f"Failed to fetch weather data: {str(e)}")
    
    def show_home(self):
        self.clear_content()
        
        # Welcome label
        welcome_label = tk.Label(
            self.content_area, 
            text="WELCOME", 
            font=("Arial", 24)
        )
        welcome_label.pack(pady=(50, 10))
        
        # Name label (placeholder)
        name_label = tk.Label(
            self.content_area, 
            text=self.username, 
            font=("Arial", 18)
        )
        name_label.pack(pady=(10, 20))
        
        # Weather and time frame
        weather_time_frame = tk.Frame(self.content_area)
        weather_time_frame.pack(pady=20)
        
        # Weather widget
        self.weather_frame = tk.LabelFrame(weather_time_frame, text="Weather", padx=10, pady=10)
        self.weather_frame.pack(side=tk.LEFT, padx=10)
        
        self.weather_location = tk.Label(self.weather_frame, text=f"Location:{self.user_input} ")
        self.weather_location.pack(anchor=tk.W)
        
        self.weather_temp = tk.Label(self.weather_frame, text=f"Temperature: {self.temperature}")
        self.weather_temp.pack(anchor=tk.W)
        
        self.weather_condition = tk.Label(self.weather_frame, text=f"Condition: {self.condition}")
        self.weather_condition.pack(anchor=tk.W)
        
        self.update_weather_button = tk.Button(self.weather_frame, text="Update Weather", command=self.update_weather)
        self.update_weather_button.pack(pady=(10, 0))
        
        # Time widget
        self.time_frame = tk.LabelFrame(weather_time_frame, text="Current Time", padx=10, pady=10)
        self.time_frame.pack(side=tk.LEFT, padx=10)
        
        self.time_label = tk.Label(self.time_frame, text="", font=("Arial", 14))
        self.time_label.pack(pady=5)
        
        self.date_label = tk.Label(self.time_frame, text="", font=("Arial", 12))
        self.date_label.pack(pady=5)
        
        self.update_time()
        
        # Quick access frame - shows upcoming schedule items and medications
        quick_access_frame = tk.LabelFrame(self.content_area, text="Today's Schedule & Medications", padx=10, pady=10)
        quick_access_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Schedule section
        schedule_label = tk.Label(quick_access_frame, text="Upcoming Events:", font=("Arial", 12, "bold"))
        schedule_label.pack(anchor=tk.W, pady=(0, 5))
        
        today = datetime.now().strftime("%Y-%m-%d")
        today_events = [event for event in self.schedule_data if event["date"] == today]
        
        if today_events:
            for event in today_events[:3]:  # Show max 3 events
                event_label = tk.Label(quick_access_frame, text=f"{event['time']} - {event['title']}")
                event_label.pack(anchor=tk.W, padx=(10, 0))
        else:
            no_events = tk.Label(quick_access_frame, text="No events scheduled for today")
            no_events.pack(anchor=tk.W, padx=(10, 0))
        
        # Medication section
        medication_label = tk.Label(quick_access_frame, text="Today's Medications:", font=("Arial", 12, "bold"))
        medication_label.pack(anchor=tk.W, pady=(10, 5))
        
        today_meds = [med for med in self.medication_data if med["days"] == "Daily" or datetime.now().strftime("%A") in med["days"]]
        
        if today_meds:
            for med in today_meds[:3]:  # Show max 3 medications
                med_label = tk.Label(quick_access_frame, text=f"{med['time']} - {med['name']} ({med['dosage']})")
                med_label.pack(anchor=tk.W, padx=(10, 0))
        else:
            no_meds = tk.Label(quick_access_frame, text="No medications scheduled for today")
            no_meds.pack(anchor=tk.W, padx=(10, 0))
        

        # Help button
        help_frame = tk.Frame(self.content_area)
        help_frame.pack(pady=30)
        
        help_button = tk.Button(
            help_frame, 
            text="HELP", 
            command=self.show_help,
            bd=2,
            relief=tk.SOLID,
            width=10,
            height=2
        )
        help_button.pack()
    
    def update_time(self):
        # Get current time and date
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%B %d, %Y")
        
        # Update labels
        if hasattr(self, 'time_label') and self.time_label.winfo_exists():
            self.time_label.config(text=time_str)
            self.date_label.config(text=date_str)
    
    def update_time_continuously(self):
        while True:
            try:
                self.update_time()
                time.sleep(1)
            except:
                # Handle possible errors like destroyed widgets
                pass
    
    def update_weather(self):
        try:
            self.weather_info()
            self.weather_location.config(text=f"Location: {self.user_input}")
            self.weather_temp.config(text=f"Temperature: {self.temperature}°C")
            self.weather_condition.config(text=f"Condition: {self.condition}")
        except Exception as e:
            messagebox.showerror("Weather Error", f"Failed to update weather.\n{str(e)}")
    
    def show_help(self):
        # Create a popup help window
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("400x300")
        
        help_label = tk.Label(
            help_window,
            text="Dashboard Help",
            font=("Arial", 16, "bold")
        )
        help_label.pack(pady=10)
        
        help_text = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Insert help content
        help_content = """
        Dashboard Navigation:
        
        - HOME: Returns to this main screen
        - GENERAL CHAT: Opens chat interface
        - RELIGION: Religious content and resources
        - MODE: Change application settings
        - COOK BOOK: Recipes and cooking tips
        - NEWS: Latest news updates
        - JOURNAL: Personal journal entries
        - SCRIBBLE: Drawing and note-taking
        
        Click any button in the sidebar to navigate.
        """
        
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)  # Make read-only
        
        close_button = tk.Button(help_window, text="Close", command=help_window.destroy)
        close_button.pack(pady=10)
    
    # Placeholder methods for other menu items
    def show_general_chat(self):
        self.clear_content()
                
        # Create frame containers for chat interface
        chat_frame = tk.Frame(self.content_area, bg="#f0f0f0")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left sidebar 
        sidebar_frame = tk.Frame(chat_frame, width=150, bg="#e0e0e0", bd=1, relief=tk.SOLID)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Add some placeholder elements to sidebar
        for i in range(5):
            sidebar_item = tk.Frame(sidebar_frame, height=40, bg="#e0e0e0", bd=1, relief=tk.SOLID)
            sidebar_item.pack(fill=tk.X, pady=2)
        
        # Content area
        content_frame = tk.Frame(chat_frame, bg="#f0f0f0")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Output area
        output_label = tk.Label(content_frame, text="OUTPUT", anchor=tk.W, bg="#f0f0f0", font=("Arial", 12, "bold"))
        output_label.pack(fill=tk.X, pady=(0, 5))
        
        self.output_area = scrolledtext.ScrolledText(content_frame, height=15, wrap=tk.WORD, bg="white", 
                                                    font=("Arial", 11))
        self.output_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.output_area.config(state=tk.DISABLED)
        
        # Input area with frame for proper layout
        input_frame = tk.Frame(content_frame, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        input_label = tk.Label(input_frame, text="INPUT", anchor=tk.W, bg="#f0f0f0", font=("Arial", 12, "bold"))
        input_label.pack(side=tk.LEFT)
        
        button_frame = tk.Frame(input_frame, bg="#f0f0f0")
        button_frame.pack(side=tk.RIGHT)  # Changed from LEFT to RIGHT to position buttons correctly
        
        # Input text area - Move this up before buttons to ensure it's created before we reference it
        self.input_area = tk.Text(content_frame, height=3, wrap=tk.WORD, bg="white", font=("Arial", 11))
        self.input_area.pack(fill=tk.X, pady=(5, 0))
        
        # Define these methods first so buttons can reference them
        def send_message_handler():
            message = self.input_area.get("1.0", tk.END).strip()
            if message:
                global historygc
                historygc+=[types.Content(role="user", parts=[types.Part.from_text(text=message)])]
                display_message('You: '+message)
                out = general_chat.generate(historygc)
                historygc+=[types.Content(role="model", parts=[types.Part.from_text(text=out)])]
                display_message('SenectusAI: '+out)
                self.input_area.delete("1.0", tk.END)
        
        def display_message(message):
            self.output_area.config(state=tk.NORMAL)
            self.output_area.insert(tk.END, message + "\n\n")
            self.output_area.see(tk.END)
            self.output_area.config(state=tk.DISABLED)
        
        def audio_input_handler():
            global historygc
            s = audio.record()
            historygc+=[types.Content(role="user", parts=[types.Part.from_text(text=s)])]
            display_message('You: '+s)
            out = general_chat.generate(historygc)
            historygc+=[types.Content(role="model", parts=[types.Part.from_text(text=out)])]
            audio.speak(out)
            display_message('SenectusAI: '+out)
        
        def handle_return_handler(event):
            if not (event.state & 0x1):  # Check if shift is not pressed
                send_message_handler()
                return "break"  # Prevents default behavior
        
        # Now create the buttons with the correct handlers
        # Send button
        self.send_button = tk.Button(button_frame, text="SEND", command=send_message_handler, bg="#4CAF50", 
                                    fg="white", font=("Arial", 10, "bold"), width=8)
        self.send_button.pack(side=tk.RIGHT, padx=5)
        
        # Audio input button
        self.audio_button = tk.Button(button_frame, text="🎤", command=audio_input_handler, bg="#2196F3", 
                                    fg="white", font=("Arial", 12), width=3)
        self.audio_button.pack(side=tk.RIGHT)
        
        # Bind return key after defining the handler
        self.input_area.bind('<Return>', handle_return_handler)
        
        # Store methods in class for potential use elsewhere
        self.send_message = send_message_handler
        self.display_message = display_message
        self.audio_input = audio_input_handler
        self.handle_return = handle_return_handler 
                      
    def show_religion(self):
        self.clear_content()
        global historyreligion
                
        # Create frame containers for chat interface
        chat_frame = tk.Frame(self.content_area, bg="#f0f0f0")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left sidebar 
        sidebar_frame = tk.Frame(chat_frame, width=150, bg="#e0e0e0", bd=1, relief=tk.SOLID)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Add some placeholder elements to sidebar
        for i in range(5):
            sidebar_item = tk.Frame(sidebar_frame, height=40, bg="#e0e0e0", bd=1, relief=tk.SOLID)
            sidebar_item.pack(fill=tk.X, pady=2)
        
        # Content area
        content_frame = tk.Frame(chat_frame, bg="#f0f0f0")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Output area
        output_label = tk.Label(content_frame, text="OUTPUT", anchor=tk.W, bg="#f0f0f0", font=("Arial", 12, "bold"))
        output_label.pack(fill=tk.X, pady=(0, 5))
        
        self.output_area = scrolledtext.ScrolledText(content_frame, height=15, wrap=tk.WORD, bg="white", 
                                                    font=("Arial", 11))
        self.output_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.output_area.config(state=tk.DISABLED)
        
        # Input area with frame for proper layout
        input_frame = tk.Frame(content_frame, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        input_label = tk.Label(input_frame, text="INPUT", anchor=tk.W, bg="#f0f0f0", font=("Arial", 12, "bold"))
        input_label.pack(side=tk.LEFT)
        
        button_frame = tk.Frame(input_frame, bg="#f0f0f0")
        button_frame.pack(side=tk.RIGHT)  # Changed from LEFT to RIGHT to position buttons correctly
        
        # Input text area - Move this up before buttons to ensure it's created before we reference it
        self.input_area = tk.Text(content_frame, height=3, wrap=tk.WORD, bg="white", font=("Arial", 11))
        self.input_area.pack(fill=tk.X, pady=(5, 0))
        
        # Define these methods first so buttons can reference them
        def send_message_handler():
            message = self.input_area.get("1.0", tk.END).strip()
            if message:
                global historyreligion
                historyreligion+=[types.Content(role="user", parts=[types.Part.from_text(text=message)])]
                display_message('You: '+message)
                out = religious.generate(historyreligion)
                historyreligion+=[types.Content(role="model", parts=[types.Part.from_text(text=out)])]
                display_message('SenectusAI: '+out)
                self.input_area.delete("1.0", tk.END)
        
        def display_message(message):
            self.output_area.config(state=tk.NORMAL)
            self.output_area.insert(tk.END, message + "\n\n")
            self.output_area.see(tk.END)
            self.output_area.config(state=tk.DISABLED)
        
        def audio_input_handler():
            global historyreligion
            s = audio.record()
            historyreligion+=[types.Content(role="user", parts=[types.Part.from_text(text=s)])]
            display_message('You: '+s)
            out = religious.generate(historyreligion)
            historyreligion+=[types.Content(role="model", parts=[types.Part.from_text(text=out)])]
            audio.speak(out)
            display_message('SenectusAI: '+out)
        
        def handle_return_handler(event):
            if not (event.state & 0x1):  # Check if shift is not pressed
                send_message_handler()
                return "break"  # Prevents default behavior
        
        # Now create the buttons with the correct handlers
        # Send button
        self.send_button = tk.Button(button_frame, text="SEND", command=send_message_handler, bg="#4CAF50", 
                                    fg="white", font=("Arial", 10, "bold"), width=8)
        self.send_button.pack(side=tk.RIGHT, padx=5)
        
        # Audio input button
        self.audio_button = tk.Button(button_frame, text="🎤", command=audio_input_handler, bg="#2196F3", 
                                    fg="white", font=("Arial", 12), width=3)
        self.audio_button.pack(side=tk.RIGHT)
        
        # Bind return key after defining the handler
        self.input_area.bind('<Return>', handle_return_handler)
        
        # Store methods in class for potential use elsewhere
        self.send_message = send_message_handler
        self.display_message = display_message
        self.audio_input = audio_input_handler
        self.handle_return = handle_return_handler 
        
    
    def show_cookbook(self):
        self.clear_content()
        global historycookbook
                
        # Create frame containers for chat interface
        chat_frame = tk.Frame(self.content_area, bg="#f0f0f0")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left sidebar 
        sidebar_frame = tk.Frame(chat_frame, width=150, bg="#e0e0e0", bd=1, relief=tk.SOLID)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Add some placeholder elements to sidebar
        for i in range(5):
            sidebar_item = tk.Frame(sidebar_frame, height=40, bg="#e0e0e0", bd=1, relief=tk.SOLID)
            sidebar_item.pack(fill=tk.X, pady=2)
        
        # Content area
        content_frame = tk.Frame(chat_frame, bg="#f0f0f0")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Output area
        output_label = tk.Label(content_frame, text="OUTPUT", anchor=tk.W, bg="#f0f0f0", font=("Arial", 12, "bold"))
        output_label.pack(fill=tk.X, pady=(0, 5))
        
        self.output_area = scrolledtext.ScrolledText(content_frame, height=15, wrap=tk.WORD, bg="white", 
                                                    font=("Arial", 11))
        self.output_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.output_area.config(state=tk.DISABLED)
        
        # Input area with frame for proper layout
        input_frame = tk.Frame(content_frame, bg="#f0f0f0")
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        input_label = tk.Label(input_frame, text="INPUT", anchor=tk.W, bg="#f0f0f0", font=("Arial", 12, "bold"))
        input_label.pack(side=tk.LEFT)
        
        button_frame = tk.Frame(input_frame, bg="#f0f0f0")
        button_frame.pack(side=tk.RIGHT)  # Changed from LEFT to RIGHT to position buttons correctly
        
        # Input text area - Move this up before buttons to ensure it's created before we reference it
        self.input_area = tk.Text(content_frame, height=3, wrap=tk.WORD, bg="white", font=("Arial", 11))
        self.input_area.pack(fill=tk.X, pady=(5, 0))
        
        # Define these methods first so buttons can reference them
        def send_message_handler():
            message = self.input_area.get("1.0", tk.END).strip()
            if message:
                global historycookbook
                historycookbook+=[types.Content(role="user", parts=[types.Part.from_text(text=message)])]
                display_message('You: '+message)
                out = cook_book.generate(historycookbook)
                historycookbook+=[types.Content(role="model", parts=[types.Part.from_text(text=out)])]
                display_message('SenectusAI: '+out)
                self.input_area.delete("1.0", tk.END)
        
        def display_message(message):
            self.output_area.config(state=tk.NORMAL)
            self.output_area.insert(tk.END, message + "\n\n")
            self.output_area.see(tk.END)
            self.output_area.config(state=tk.DISABLED)
        
        def audio_input_handler():
            global historycookbook
            s = audio.record()
            historycookbook+=[types.Content(role="user", parts=[types.Part.from_text(text=s)])]
            display_message('You: '+s)
            out = cook_book.generate(historycookbook)
            historycookbook+=[types.Content(role="model", parts=[types.Part.from_text(text=out)])]
            audio.speak(out)
            display_message('SenectusAI: '+out)
        
        def handle_return_handler(event):
            if not (event.state & 0x1):  # Check if shift is not pressed
                send_message_handler()
                return "break"  # Prevents default behavior
        
        # Now create the buttons with the correct handlers
        # Send button
        self.send_button = tk.Button(button_frame, text="SEND", command=send_message_handler, bg="#4CAF50", 
                                    fg="white", font=("Arial", 10, "bold"), width=8)
        self.send_button.pack(side=tk.RIGHT, padx=5)
        
        # Audio input button
        self.audio_button = tk.Button(button_frame, text="🎤", command=audio_input_handler, bg="#2196F3", 
                                    fg="white", font=("Arial", 12), width=3)
        self.audio_button.pack(side=tk.RIGHT)
        
        # Bind return key after defining the handler
        self.input_area.bind('<Return>', handle_return_handler)
        
        # Store methods in class for potential use elsewhere
        self.send_message = send_message_handler
        self.display_message = display_message
        self.audio_input = audio_input_handler
        self.handle_return = handle_return_handler 

        
    
    def show_news(self):
        self.clear_content()
        label = tk.Label(self.content_area, text="News", font=("Arial", 24))
        label.pack(pady=30)
        
        news_frame = tk.Frame(self.content_area)
        news_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # News categories
        categories_frame = tk.Frame(news_frame)
        categories_frame.pack(fill=tk.X)
        
        """ categories = ["World", "Local", "Technology", "Sports", "Entertainment", "Health"]
        
        for i, category in enumerate(categories):
            category_btn = tk.Button(categories_frame, text=category)
            category_btn.grid(row=0, column=i, padx=5, pady=5) """
        
        # News items
        news_content = tk.Frame(news_frame)
        news_content.pack(fill=tk.BOTH, expand=True, pady=10)
        content=news2.generate()

        content = content.partition(":")[2]
        content=' '.join(content.split('**'))

        news_item = tk.Frame(news_content, bd=1, relief=tk.SOLID, padx=10, pady=10)
        news_item.pack(fill=tk.X, pady=5)
        
        summary = tk.Label(news_item, text=f"This is the top 5 latest news.\n {content}", wraplength=500, anchor=tk.W, justify=tk.LEFT)
        summary.pack(anchor=tk.W)
    
    '''def show_journal(self):
        self.clear_content()
        label = tk.Label(self.content_area, text="Journal", font=("Arial", 24))
        label.pack(pady=20)
        
        journal_frame = tk.Frame(self.content_area)
        journal_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Date selection
        date_frame = tk.Frame(journal_frame)
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        date_label = tk.Label(date_frame, text="Date:")
        date_label.pack(side=tk.LEFT, padx=(0, 10))
        
        date_entry = tk.Entry(date_frame, width=15)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(side=tk.LEFT)
        
        # Journal entry
        entry_label = tk.Label(journal_frame, text="Journal Entry:", anchor=tk.W)
        entry_label.pack(anchor=tk.W, pady=(10, 5))
        
        journal_text = tk.Text(journal_frame, height=15, width=50)
        journal_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = tk.Frame(journal_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        save_button = tk.Button(button_frame, text="Save Entry")
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        load_button = tk.Button(button_frame, text="Load Entry")
        load_button.pack(side=tk.LEFT, padx=(0, 10))
        
        new_button = tk.Button(button_frame, text="New Entry")
        new_button.pack(side=tk.LEFT)'''
    
    def show_scribble(self):
        self.clear_content()
        label = tk.Label(self.content_area, text="Scribble", font=("Arial", 24))
        label.pack(pady=20)
        
        scribble_frame = tk.Frame(self.content_area)
        scribble_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create a canvas for drawing
        self.canvas = tk.Canvas(scribble_frame, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Set up event handlers for drawing
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        
        # Track the last position
        self.last_x = None
        self.last_y = None
        
        # Drawing tools
        tools_frame = tk.Frame(scribble_frame)
        tools_frame.pack(fill=tk.X)
        
        # Color selection
        colors = ["black", "red", "blue", "green", "yellow", "purple"]
        self.selected_color = tk.StringVar(value="black")
        
        color_label = tk.Label(tools_frame, text="Color:")
        color_label.pack(side=tk.LEFT, padx=(0, 5))
        
        for color in colors:
            color_btn = tk.Radiobutton(
                tools_frame, 
                bg=color, 
                width=2, 
                variable=self.selected_color, 
                value=color,
                indicator=0,
                selectcolor=color
            )
            color_btn.pack(side=tk.LEFT, padx=2)
        
        # Brush size
        size_label = tk.Label(tools_frame, text="Size:")
        size_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.brush_size = tk.IntVar(value=2)
        
        sizes = [1, 2, 5, 8]
        size_names = ["S", "M", "L", "XL"]
        
        for i, (size, name) in enumerate(zip(sizes, size_names)):
            size_btn = tk.Radiobutton(
                tools_frame,
                text=name,
                variable=self.brush_size,
                value=size,
                indicator=0,
                width=3
            )
            size_btn.pack(side=tk.LEFT, padx=2)
        
        # Clear button
        clear_button = tk.Button(tools_frame, text="Clear", command=self.clear_canvas)
        clear_button.pack(side=tk.RIGHT)
    
    def start_draw(self, event):
        self.last_x = event.x
        self.last_y = event.y
    
    def draw(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(
                self.last_x, self.last_y, 
                event.x, event.y, 
                width=self.brush_size.get(),
                fill=self.selected_color.get(),
                capstyle=tk.ROUND, 
                smooth=tk.TRUE
            )
        
        self.last_x = event.x
        self.last_y = event.y
    
    def clear_canvas(self):
        self.canvas.delete("all")

    # New functionality: Schedule
    def show_schedule(self):
        self.clear_content()
        label = tk.Label(self.content_area, text="Schedule", font=("Arial", 24))
        label.pack(pady=20)
        
        # Main schedule frame
        schedule_frame = tk.Frame(self.content_area)
        schedule_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side - Schedule list
        list_frame = tk.Frame(schedule_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        list_label = tk.Label(list_frame, text="Upcoming Events", font=("Arial", 14, "bold"))
        list_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Treeview for events
        columns = ("Date", "Time", "Title", "Description")
        self.schedule_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.schedule_tree.heading(col, text=col)
            width = 100 if col in ("Date", "Time") else 200
            self.schedule_tree.column(col, width=width)
        
        self.schedule_tree.pack(fill=tk.BOTH, expand=True)
        
        # Populate treeview with schedule data
        self.populate_schedule_tree()
        
        # Right side - Add/Edit event
        event_frame = tk.LabelFrame(schedule_frame, text="Add/Edit Event")
        event_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Event form
        form_frame = tk.Frame(event_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Date
        date_label = tk.Label(form_frame, text="Date:")
        date_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.event_date = tk.Entry(form_frame, width=15)
        self.event_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.event_date.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Time
        time_label = tk.Label(form_frame, text="Time:")
        time_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.event_time = tk.Entry(form_frame, width=15)
        self.event_time.insert(0, datetime.now().strftime("%H:%M"))
        self.event_time.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Title
        title_label = tk.Label(form_frame, text="Title:")
        title_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.event_title = tk.Entry(form_frame, width=25)
        self.event_title.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Description
        desc_label = tk.Label(form_frame, text="Description:")
        desc_label.grid(row=3, column=0, sticky=tk.NW, pady=5)
        
        self.event_desc = tk.Text(form_frame, width=25, height=5)
        self.event_desc.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        add_button = tk.Button(button_frame, text="Add Event", command=self.add_schedule_event)
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        update_button = tk.Button(button_frame, text="Update", command=self.update_schedule_event)
        update_button.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_schedule_event)
        delete_button.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_schedule_form)
        clear_button.pack(side=tk.LEFT)
        
        # Bind selection event
        self.schedule_tree.bind("<<TreeviewSelect>>", self.on_schedule_select)
    
    def populate_schedule_tree(self):
        # Clear existing items
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)
        
        # Sort schedule data by date and time
        sorted_data = sorted(self.schedule_data, key=lambda x: (x["date"], x["time"]))
        
        # Add items to tree
        for event in sorted_data:
            self.schedule_tree.insert(
                "", 
                tk.END, 
                values=(event["date"], event["time"], event["title"], event["description"])
            )
    
    def add_schedule_event(self):
        # Get form data
        date = self.event_date.get()
        time = self.event_time.get()
        title = self.event_title.get()
        description = self.event_desc.get("1.0", tk.END).strip()
        
        # Validate
        if not date or not time or not title:
            messagebox.showerror("Error", "Date, time, and title are required!")
            return
        
        # Add to data
        new_event = {
            "date": date,
            "time": time,
            "title": title,
            "description": description
        }
        
        self.schedule_data.append(new_event)
        self.save_schedule_data()
        
        # Update tree
        self.populate_schedule_tree()
        
        # Clear form
        self.clear_schedule_form()
        
        messagebox.showinfo("Success", "Event added successfully!")
    
    def update_schedule_event(self):
        # Get selected item
        selected = self.schedule_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No event selected!")
            return
        
        # Get form data
        date = self.event_date.get()
        time = self.event_time.get()
        title = self.event_title.get()
        description = self.event_desc.get("1.0", tk.END).strip()
        
        # Validate
        if not date or not time or not title:
            messagebox.showerror("Error", "Date, time, and title are required!")
            return
        
        # Get selected values
        item = self.schedule_tree.item(selected[0])
        old_date = item["values"][0]
        old_time = item["values"][1]
        old_title = item["values"][2]
        
        # Find and update item
        for i, event in enumerate(self.schedule_data):
            if (event["date"] == old_date and 
                event["time"] == old_time and 
                event["title"] == old_title):
                
                self.schedule_data[i] = {
                    "date": date,
                    "time": time,
                    "title": title,
                    "description": description
                }
                break
        
        self.save_schedule_data()
        
        # Update tree
        self.populate_schedule_tree()
        
        messagebox.showinfo("Success", "Event updated successfully!")
    
    def delete_schedule_event(self):
        # Get selected item
        selected = self.schedule_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No event selected!")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this event?"):
            return
        
        # Get selected values
        item = self.schedule_tree.item(selected[0])
        old_date = item["values"][0]
        old_time = item["values"][1]
        old_title = item["values"][2]
        
        # Find and remove item
        for i, event in enumerate(self.schedule_data):
            if (event["date"] == old_date and 
                event["time"] == old_time and 
                event["title"] == old_title):
                
                del self.schedule_data[i]
                break
        
        self.save_schedule_data()
        
        # Update tree
        self.populate_schedule_tree()
        
        # Clear form
        self.clear_schedule_form()
        
        messagebox.showinfo("Success", "Event deleted successfully!")
    
    def clear_schedule_form(self):
        self.event_date.delete(0, tk.END)
        self.event_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.event_time.delete(0, tk.END)
        self.event_time.insert(0, datetime.now().strftime("%H:%M"))
        
        self.event_title.delete(0, tk.END)
        self.event_desc.delete("1.0", tk.END)
    
    def on_schedule_select(self, event):
        # Get selected item
        selected = self.schedule_tree.selection()
        if not selected:
            return
        
        # Get selected values
        item = self.schedule_tree.item(selected[0])
        date = item["values"][0]
        time = item["values"][1]
        title = item["values"][2]
        description = item["values"][3]
        
        # Clear form
        self.clear_schedule_form()
        
        # Fill form with selected values
        self.event_date.delete(0, tk.END)
        self.event_date.insert(0, date)
        
        self.event_time.delete(0, tk.END)
        self.event_time.insert(0, time)
        
        self.event_title.delete(0, tk.END)
        self.event_title.insert(0, title)
        
        self.event_desc.delete("1.0", tk.END)
        self.event_desc.insert("1.0", description)

    # Medication management functionality
    def show_medications(self):
        self.clear_content()
        label = tk.Label(self.content_area, text="Medication Manager", font=("Arial", 24))
        label.pack(pady=20)
        
        # Main medication frame
        med_frame = tk.Frame(self.content_area)
        med_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side - Medication list
        list_frame = tk.Frame(med_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        list_label = tk.Label(list_frame, text="Your Medications", font=("Arial", 14, "bold"))
        list_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Treeview for medications
        columns = ("Name", "Dosage", "Time", "Days", "Notes")
        self.med_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.med_tree.heading(col, text=col)
            width = 100 if col in ("Dosage", "Time") else 150
            self.med_tree.column(col, width=width)
        
        self.med_tree.pack(fill=tk.BOTH, expand=True)
        
        # Populate treeview with medication data
        self.populate_med_tree()
        
        # Right side - Add/Edit medication
        form_frame = tk.LabelFrame(med_frame, text="Add/Edit Medication")
        form_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Medication form
        med_form = tk.Frame(form_frame)
        med_form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Name
        name_label = tk.Label(med_form, text="Medication Name:")
        name_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.med_name = tk.Entry(med_form, width=25)
        self.med_name.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Dosage
        dosage_label = tk.Label(med_form, text="Dosage:")
        dosage_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.med_dosage = tk.Entry(med_form, width=25)
        self.med_dosage.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Time
        time_label = tk.Label(med_form, text="Time:")
        time_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.med_time = tk.Entry(med_form, width=15)
        self.med_time.insert(0, "08:00")
        self.med_time.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Days
        days_label = tk.Label(med_form, text="Days:")
        days_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        # Days options
        days_frame = tk.Frame(med_form)
        days_frame.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        self.days_var = tk.StringVar(value="Daily")
        daily_radio = tk.Radiobutton(days_frame, text="Daily", variable=self.days_var, value="Daily")
        daily_radio.pack(anchor=tk.W)
        
        specific_radio = tk.Radiobutton(days_frame, text="Specific Days", variable=self.days_var, value="Specific")
        specific_radio.pack(anchor=tk.W)
        
        # Days selection
        days_select_frame = tk.Frame(med_form)
        days_select_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        self.day_vars = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for i, day in enumerate(days):
            var = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(days_select_frame, text=day[:3], variable=var)
            cb.grid(row=i//4, column=i%4, sticky=tk.W)
            self.day_vars[day] = var
        
        # Notes
        notes_label = tk.Label(med_form, text="Notes:")
        notes_label.grid(row=5, column=0, sticky=tk.NW, pady=5)
        
        self.med_notes = tk.Text(med_form, width=25, height=5)
        self.med_notes.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Button frame
        button_frame = tk.Frame(med_form)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        add_button = tk.Button(button_frame, text="Add Medication", command=self.add_medication)
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        update_button = tk.Button(button_frame, text="Update", command=self.update_medication)
        update_button.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_medication)
        delete_button.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_med_form)
        clear_button.pack(side=tk.LEFT)
        
        # Bind selection event
        self.med_tree.bind("<<TreeviewSelect>>", self.on_med_select)
        
        # Add reminder features
        reminder_frame = tk.LabelFrame(list_frame, text="Medication Reminders")
        reminder_frame.pack(fill=tk.X, pady=(10, 0))
        
        enable_remind = tk.Checkbutton(reminder_frame, text="Enable Medication Reminders")
        enable_remind.pack(anchor=tk.W, padx=10, pady=5)
        
        remind_label = tk.Label(reminder_frame, text="Remind me minutes before:")
        remind_label.pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        remind_entry = tk.Entry(reminder_frame, width=5)
        remind_entry.insert(0, "30")
        remind_entry.pack(anchor=tk.W, padx=10, pady=(0, 10))
    
    def populate_med_tree(self):
        # Clear existing items
        for item in self.med_tree.get_children():
            self.med_tree.delete(item)
        
        # Sort medication data by time
        sorted_data = sorted(self.medication_data, key=lambda x: x["time"])
        
        # Add items to tree
        for med in sorted_data:
            self.med_tree.insert(
                "", 
                tk.END, 
                values=(med["name"], med["dosage"], med["time"], med["days"], med["notes"])
            )
    
    def add_medication(self):
        # Get form data
        name = self.med_name.get()
        dosage = self.med_dosage.get()
        time = self.med_time.get()
        notes = self.med_notes.get("1.0", tk.END).strip()
        
        # Validate
        if not name or not dosage or not time:
            messagebox.showerror("Error", "Name, dosage, and time are required!")
            return
        
        # Get days
        days = "Daily"
        if self.days_var.get() == "Specific":
            selected_days = []
            for day, var in self.day_vars.items():
                if var.get():
                    selected_days.append(day)
            
            if not selected_days:
                messagebox.showerror("Error", "Please select at least one day!")
                return
            
            days = ", ".join(selected_days)
        
        # Add to data
        new_med = {
            "name": name,
            "dosage": dosage,
            "time": time,
            "days": days,
            "notes": notes
        }
        
        self.medication_data.append(new_med)
        self.save_medication_data()
        
        # Update tree
        self.populate_med_tree()
        
        # Clear form
        self.clear_med_form()
        
        messagebox.showinfo("Success", "Medication added successfully!")
    
    def update_medication(self):
        # Get selected item
        selected = self.med_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No medication selected!")
            return
        
        # Get form data
        name = self.med_name.get()
        dosage = self.med_dosage.get()
        time = self.med_time.get()
        notes = self.med_notes.get("1.0", tk.END).strip()
        
        # Validate
        if not name or not dosage or not time:
            messagebox.showerror("Error", "Name, dosage, and time are required!")
            return
        
        # Get days
        days = "Daily"
        if self.days_var.get() == "Specific":
            selected_days = []
            for day, var in self.day_vars.items():
                if var.get():
                    selected_days.append(day)
            
            if not selected_days:
                messagebox.showerror("Error", "Please select at least one day!")
                return
            
            days = ", ".join(selected_days)
        
        # Get selected values
        item = self.med_tree.item(selected[0])
        old_name = item["values"][0]
        old_dosage = item["values"][1]
        old_time = item["values"][2]
        
        # Find and update item
        for i, med in enumerate(self.medication_data):
            if (med["name"] == old_name and 
                med["dosage"] == old_dosage and 
                med["time"] == old_time):
                
                self.medication_data[i] = {
                    "name": name,
                    "dosage": dosage,
                    "time": time,
                    "days": days,
                    "notes": notes
                }
                break
        
        self.save_medication_data()
        
        # Update tree
        self.populate_med_tree()
        
        messagebox.showinfo("Success", "Medication updated successfully!")
    
    def delete_medication(self):
        # Get selected item
        selected = self.med_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No medication selected!")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this medication?"):
            return
        
        # Get selected values
        item = self.med_tree.item(selected[0])
        old_name = item["values"][0]
        old_dosage = item["values"][1]
        old_time = item["values"][2]
        
        # Find and remove item
        for i, med in enumerate(self.medication_data):
            if (med["name"] == old_name and 
                med["dosage"] == old_dosage and 
                med["time"] == old_time):
                
                del self.medication_data[i]
                break
        
        self.save_medication_data()
        
        # Update tree
        self.populate_med_tree()
        
        # Clear form
        self.clear_med_form()
        
        messagebox.showinfo("Success", "Medication deleted successfully!")
    
    def clear_med_form(self):
        self.med_name.delete(0, tk.END)
        self.med_dosage.delete(0, tk.END)
        
        self.med_time.delete(0, tk.END)
        self.med_time.insert(0, "08:00")
        
        self.days_var.set("Daily")
        
        for var in self.day_vars.values():
            var.set(False)
        
        self.med_notes.delete("1.0", tk.END)
    
    def on_med_select(self, event):
        # Get selected item
        selected = self.med_tree.selection()
        if not selected:
            return
        
        # Get selected values
        item = self.med_tree.item(selected[0])
        name = item["values"][0]
        dosage = item["values"][1]
        time = item["values"][2]
        days = item["values"][3]
        notes = item["values"][4] if item["values"][4] else ""
        
        # Clear form
        self.clear_med_form()
        
        # Fill form with selected values
        self.med_name.insert(0, name)
        self.med_dosage.insert(0, dosage)
        
        self.med_time.delete(0, tk.END)
        self.med_time.insert(0, time)
        
        # Set days
        if days == "Daily":
            self.days_var.set("Daily")
        else:
            self.days_var.set("Specific")
            day_list = [day.strip() for day in days.split(",")]
            
            for day, var in self.day_vars.items():
                if day in day_list:
                    var.set(True)
        
        self.med_notes.insert("1.0", notes)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()