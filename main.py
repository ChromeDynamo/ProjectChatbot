import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import re
import json
from collections import Counter


class ChatbotGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initialize chatbot data
        self.filename = "keywords.json"
        self.keyword_responses = self.load_responses()
        self.user_questions = []
        self.keyword_tracker = Counter()
        self.personalities = {
            "Alex": "quirky and loves puns",
            "Jordan": "friendly and empathetic",
            "Taylor": "witty with a touch of sarcasm",
            "Morgan": "calm and professional",
            "Casey": "playful and loves jokes"
        }
        self.agent_name = random.choice(list(self.personalities.keys()))
        self.user_name = None
        self.current_topic = None
        self.current_responses = None
        self.response_index = 0
        self.awaiting_name = True
        self.awaiting_topics_confirmation = False
        self.awaiting_more_info = False

        # Window setup
        self.title("University of Poppleton Chatbot")
        self.geometry("900x700")
        self.configure(bg='#1e1e1e')

        # Configure style with rounded corners
        self.style = ttk.Style()
        self.style.configure('Dark.TFrame', background='#1e1e1e')
        self.style.configure('Header.TLabel',
                             background='#4CAF50',
                             foreground='white',
                             font=('Arial', 14, 'bold'),
                             padding=10,
                             anchor='center')
        self.style.configure('Dark.TButton',
                             padding=10)
        self.style.configure('Input.TFrame',
                             background='#2d2d2d',
                             relief='solid')

        # Create main container
        self.create_widgets()
        self.start_chat()

    def get_confirmation(self, user_input):
        """Determines if input is a 'yes' or 'no' response based on synonyms."""
        yes_synonyms = {"yes", "yea", "yeah", "sure", "okay", "ok", "yep", "alright"}
        no_synonyms = {"no", "nah", "nope", "not really", "no thanks"}

        normalized_input = user_input.strip().lower()
        if any(word in normalized_input for word in yes_synonyms):
            return "yes"
        elif any(word in normalized_input for word in no_synonyms):
            return "no"
        return None

    def create_widgets(self):
        # Main container with padding and rounded corners
        main_container = ttk.Frame(self, style='Dark.TFrame')
        main_container.pack(expand=True, fill="both", padx=20, pady=20)

        # Header with rounded corners
        header_frame = tk.Frame(main_container, bg='#4CAF50')
        header_frame.pack(fill="x", pady=(0, 20))
        # Apply rounded corners to header
        header_frame.bind('<Configure>', lambda e: self.round_corners(header_frame, 10))

        header = tk.Label(header_frame,
                          text="University of Poppleton Chat Assistant",
                          bg='#4CAF50',
                          fg='white',
                          font=('Arial', 14, 'bold'),
                          pady=10)
        header.pack(fill="x")

        # Chat display area with rounded corners
        chat_frame = tk.Frame(main_container, bg='#2d2d2d')
        chat_frame.pack(expand=True, fill="both", pady=(0, 10))
        # Apply rounded corners to chat frame
        chat_frame.bind('<Configure>', lambda e: self.round_corners(chat_frame, 10))

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            height=20,
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='white',
            relief="flat",
            border=0
        )
        self.chat_display.pack(expand=True, fill="both", padx=2, pady=2)

        # Input area with rounded corners
        input_frame = tk.Frame(main_container, bg='#2d2d2d')
        input_frame.pack(fill="x", pady=(10, 20))
        # Apply rounded corners to input frame
        input_frame.bind('<Configure>', lambda e: self.round_corners(input_frame, 10))

        # Rounded input box
        self.user_input = tk.Entry(
            input_frame,
            font=('Arial', 11),
            bg='#2d2d2d',
            fg='white',
            insertbackground='white',
            relief='flat',
            border=0
        )
        self.user_input.pack(side="left", expand=True, fill="x", padx=10, pady=10)

        # Rounded send button
        send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.process_input,
            font=('Arial', 10, 'bold'),
            bg='#4CAF50',
            fg='white',
            relief='flat',
            activebackground='#45a049',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        send_button.pack(side="right", padx=10, pady=5)
        # Apply rounded corners to send button
        send_button.bind('<Configure>', lambda e: self.round_corners(send_button, 15))

        # Rounded admin button
        admin_button = tk.Button(
            main_container,
            text="Admin Mode",
            command=self.show_admin_login,
            font=('Arial', 10),
            bg='#4CAF50',
            fg='white',
            relief='flat',
            activebackground='#45a049',
            padx=15,
            pady=5,
            cursor='hand2'
        )
        admin_button.pack()
        # Apply rounded corners to admin button
        admin_button.bind('<Configure>', lambda e: self.round_corners(admin_button, 15))

        # Bind Enter key
        self.user_input.bind("<Return>", lambda e: self.process_input())

    def round_corners(self, widget, radius):
        """Apply rounded corners to a widget"""
        # Create a rounded corner mask
        radius = radius * 2  # Scale radius for better appearance
        widget._round_corners_path = f"""
            M {radius},0
            L {widget.winfo_width() - radius},0
            Q {widget.winfo_width()},0 {widget.winfo_width()},{radius}
            L {widget.winfo_width()},{widget.winfo_height() - radius}
            Q {widget.winfo_width()},{widget.winfo_height()} {widget.winfo_width() - radius},{widget.winfo_height()}
            L {radius},{widget.winfo_height()}
            Q 0,{widget.winfo_height()} 0,{widget.winfo_height() - radius}
            L 0,{radius}
            Q 0,0 {radius},0
        """
        widget.update_idletasks()
        try:
            # Try to create rounded corners using tkinter's built-in methods
            widget._round_corners_region = widget._round_corners_path
            widget.region_create = widget._round_corners_region
            widget.region_configure = widget._round_corners_region
        except:
            pass  # Fallback to regular corners if rounded corners are not supported

    def display_message(self, sender, message):
        self.chat_display.tag_configure('sender',
                                        font=('Arial', 10, 'bold'),
                                        foreground='#4CAF50')  # Green sender names
        self.chat_display.tag_configure('message',
                                        font=('Arial', 10),
                                        foreground='white')  # White messages

        self.chat_display.insert(tk.END, f"{sender}: ", 'sender')
        self.chat_display.insert(tk.END, f"{message}\n", 'message')
        self.chat_display.see(tk.END)

    def process_input(self):
        user_input = self.user_input.get().strip()
        if not user_input:
            return

        self.user_input.delete(0, tk.END)
        self.display_message("You", user_input)

        # Handle name input
        if self.awaiting_name:
            self.user_name = user_input
            self.awaiting_name = False
            self.display_message(self.agent_name, f"Hello {self.user_name}, it's great to meet you!")
            self.display_message(self.agent_name, "Would you like to see the available topics?")
            self.awaiting_topics_confirmation = True
            return

        # Handle topics confirmation
        if self.awaiting_topics_confirmation:
            confirmation = self.get_confirmation(user_input)
            if confirmation == "yes":
                self.show_topics()
            else:
                self.display_message(self.agent_name,
                                     "No problem! Let me know if there's anything else you'd like to discuss.")
            self.awaiting_topics_confirmation = False
            return

        # Handle more info confirmation
        if self.awaiting_more_info:
            confirmation = self.get_confirmation(user_input)
            if confirmation == "yes":
                if self.current_responses and self.response_index < len(self.current_responses[self.agent_name]):
                    response = self.current_responses[self.agent_name][self.response_index]
                    self.display_message(self.agent_name, response)
                    self.response_index += 1
                    self.display_message(self.agent_name, f"Would you like to know more about {self.current_topic}?")
                else:
                    self.display_message(self.agent_name,
                                         f"Sorry, I've run out of information about {self.current_topic}.")
                    self.awaiting_more_info = False
                    self.current_topic = None
                    self.current_responses = None
            else:
                self.display_message(self.agent_name,
                                     "No problem! Let me know if there's anything else you'd like to discuss.")
                self.awaiting_more_info = False
                self.current_topic = None
                self.current_responses = None
            return

        # Track user input
        self.user_questions.append(user_input)

        # Process the input
        if re.search(r"\b(bye|exit|quit)\b", user_input, re.IGNORECASE):
            self.handle_exit()
        elif re.search(r"\b(topics|topic|topic list|topics list)\b", user_input, re.IGNORECASE):
            self.display_message(self.agent_name, "Would you like me to show the topic list again?")
            self.awaiting_topics_confirmation = True
        elif re.search(r"\b(admin|administrator|admin mode|config|configuration mode)\b", user_input, re.IGNORECASE):
            self.display_message(self.agent_name, "Entering Configuration Mode requires authentication.")
            self.show_admin_login()
        else:
            self.process_keywords(user_input)

    def process_keywords(self, user_input):
        found_keyword = False
        for keyword, responses in self.keyword_responses.items():
            if re.search(rf"\b{keyword}\b", user_input, re.IGNORECASE):
                self.keyword_tracker[keyword] += 1
                self.current_topic = keyword
                self.current_responses = responses
                self.response_index = 1  # Start at 1 since we're showing the first response now

                if isinstance(responses, dict) and self.agent_name in responses:
                    response = responses[self.agent_name][0]  # Show first response
                    self.display_message(self.agent_name, response)
                    if len(responses[self.agent_name]) > 1:
                        self.awaiting_more_info = True
                        self.display_message(self.agent_name, f"Would you like to know more about {keyword}?")
                found_keyword = True
                break

        if not found_keyword:
            fallback_responses = {
                "Alex": ["I'm not sure, but let's wing it!", "Oops, my brain froze! Ask me that again?"],
                "Jordan": ["I'm not sure, but I'm here to help.",
                           "That's an interesting question! Let's figure it out."],
                "Taylor": ["You stumped me there, but I'll give it a go!", "Wow, tricky one. Let's see..."],
                "Morgan": ["I'm not certain about that, but let's find a solution.",
                           "Let me gather my thoughts on that."],
                "Casey": ["Whoa! That's above my pay grade, but I'll try!", "Hold up, let me boot my brain!"]
            }
            self.display_message(self.agent_name, random.choice(fallback_responses[self.agent_name]))

    def show_admin_login(self):
        login_window = tk.Toplevel(self)
        login_window.title("Admin Login")
        login_window.geometry("400x300")
        login_window.configure(bg='#1e1e1e')

        # Apply rounded corners to the login window elements
        container = tk.Frame(login_window, bg='#1e1e1e')
        container.pack(expand=True, fill="both", padx=20, pady=20)
        container.bind('<Configure>', lambda e: self.round_corners(container, 10))

        # Center the login window
        login_window.transient(self)
        login_window.grab_set()

        # Create styled container
        container = ttk.Frame(login_window, style='Green.TFrame')
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Header
        header = ttk.Label(container,
                           text="Administrator Login",
                           style='Header.TLabel')
        header.pack(fill="x", pady=(0, 20))

        # Login fields
        ttk.Label(container, text="Username:",
                  font=('Arial', 10, 'bold')).pack(pady=5)
        username_entry = ttk.Entry(container, font=('Arial', 10))
        username_entry.pack(pady=(0, 10), fill="x")

        ttk.Label(container, text="Password:",
                  font=('Arial', 10, 'bold')).pack(pady=5)
        password_entry = ttk.Entry(container, show="*", font=('Arial', 10))
        password_entry.pack(pady=(0, 20), fill="x")

        def try_login():
            if username_entry.get() == "admin" and password_entry.get() == "admin123":
                login_window.destroy()
                self.show_config_mode()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        # Create a frame for the login button with custom styling
        login_button = tk.Button(
            container,
            text="Login",
            command=try_login,
            font=('Arial', 10, 'bold'),
            bg='#4CAF50',
            fg='white',
            relief='flat',
            activebackground='#45a049',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        login_button.pack(pady=10)
        # Apply rounded corners to login button
        login_button.bind('<Configure>', lambda e: self.round_corners(login_button, 15))

        # Bind Enter key to try_login function
        login_window.bind('<Return>', lambda e: try_login())

    def show_config_mode(self):
        config_window = tk.Toplevel(self)
        config_window.title("Configuration Mode")
        config_window.geometry("800x600")
        config_window.configure(bg='#1e1e1e')

        # Create main container
        container = ttk.Frame(config_window, style='Green.TFrame')
        container.pack(expand=True, fill="both", padx=20, pady=20)

        # Header
        header = ttk.Label(container,
                           text="Configuration Mode",
                           style='Header.TLabel')
        header.pack(fill="x", pady=(0, 20))

        # Create notebook with styled tabs
        notebook = ttk.Notebook(container)
        notebook.pack(expand=True, fill="both")

        # View topics tab
        view_frame = ttk.Frame(notebook, style='Green.TFrame')
        notebook.add(view_frame, text="View Topics")

        topics_display = scrolledtext.ScrolledText(
            view_frame,
            wrap=tk.WORD,
            font=('Arial', 10),
            bg='#f8f9fa'
        )
        topics_display.pack(expand=True, fill="both", padx=10, pady=10)

        def update_topics_display():
            topics_display.delete(1.0, tk.END)
            for topic, responses in self.keyword_responses.items():
                topics_display.insert(tk.END, f"Topic: {topic}\n", "topic")
                if isinstance(responses, dict):
                    for personality, response_list in responses.items():
                        topics_display.insert(tk.END, f"  {personality}:\n", "personality")
                        for response in response_list:
                            topics_display.insert(tk.END, f"    - {response}\n", "response")
                topics_display.insert(tk.END, "\n")

        update_topics_display()

        # Add topic tab
        add_frame = ttk.Frame(notebook, style='Green.TFrame')
        notebook.add(add_frame, text="Add Topic")

        add_container = ttk.Frame(add_frame, style='Green.TFrame')
        add_container.pack(expand=True, fill="both", padx=20, pady=20)

        ttk.Label(add_container,
                  text="Add New Topic",
                  style='Header.TLabel').pack(fill="x", pady=(0, 20))

        ttk.Label(add_container,
                  text="Topic name:",
                  font=('Arial', 10, 'bold')).pack(pady=5)
        topic_entry = ttk.Entry(add_container, font=('Arial', 10))
        topic_entry.pack(pady=(0, 20), fill="x")

        def add_topic():
            topic = topic_entry.get().strip()
            if topic:
                if topic not in self.keyword_responses:
                    self.keyword_responses[topic] = {
                        personality: [] for personality in self.personalities
                    }
                    self.save_responses()
                    messagebox.showinfo("Success", f"Topic '{topic}' added successfully!")
                    topic_entry.delete(0, tk.END)
                    update_topics_display()
                else:
                    messagebox.showerror("Error", f"Topic '{topic}' already exists!")

        tk.Button(add_container,
                  text="Add Topic",
                  command=add_topic,
                  font=('Arial', 10, 'bold'),
                  bg='#4CAF50',
                  fg='white',
                  relief='flat',
                  activebackground='#45a049',
                  padx=20,
                  pady=8,
                  cursor='hand2').pack()

        # Edit topic tab
        edit_topic_frame = ttk.Frame(notebook, style='Green.TFrame')
        notebook.add(edit_topic_frame, text="Edit Topic")

        edit_topic_container = ttk.Frame(edit_topic_frame, style='Green.TFrame')
        edit_topic_container.pack(expand=True, fill="both", padx=20, pady=20)

        ttk.Label(edit_topic_container,
                  text="Edit Topic",
                  style='Header.TLabel').pack(fill="x", pady=(0, 20))

        ttk.Label(edit_topic_container,
                  text="Select topic:",
                  font=('Arial', 10, 'bold')).pack(pady=5)

        topic_var = tk.StringVar()
        topic_dropdown = ttk.Combobox(edit_topic_container,
                                      textvariable=topic_var,
                                      values=list(self.keyword_responses.keys()))
        topic_dropdown.pack(pady=(0, 10), fill="x")

        ttk.Label(edit_topic_container,
                  text="New topic name:",
                  font=('Arial', 10, 'bold')).pack(pady=5)
        new_topic_entry = ttk.Entry(edit_topic_container, font=('Arial', 10))
        new_topic_entry.pack(pady=(0, 20), fill="x")

        def edit_topic():
            old_topic = topic_var.get()
            new_topic = new_topic_entry.get().strip()
            if old_topic and new_topic:
                if new_topic not in self.keyword_responses:
                    self.keyword_responses[new_topic] = self.keyword_responses.pop(old_topic)
                    self.save_responses()
                    messagebox.showinfo("Success", f"Topic renamed from '{old_topic}' to '{new_topic}'!")
                    topic_dropdown['values'] = list(self.keyword_responses.keys())
                    new_topic_entry.delete(0, tk.END)
                    update_topics_display()
                    update_response_dropdowns()
                else:
                    messagebox.showerror("Error", f"Topic '{new_topic}' already exists!")

        tk.Button(edit_topic_container,
                  text="Update Topic",
                  command=edit_topic,
                  font=('Arial', 10, 'bold'),
                  bg='#4CAF50',
                  fg='white',
                  relief='flat',
                  activebackground='#45a049',
                  padx=20,
                  pady=8,
                  cursor='hand2').pack()

        # Edit response tab
        edit_response_frame = ttk.Frame(notebook, style='Green.TFrame')
        notebook.add(edit_response_frame, text="Edit Response")

        edit_response_container = ttk.Frame(edit_response_frame, style='Green.TFrame')
        edit_response_container.pack(expand=True, fill="both", padx=20, pady=20)

        ttk.Label(edit_response_container,
                  text="Edit Response",
                  style='Header.TLabel').pack(fill="x", pady=(0, 20))

        # Topic selection
        ttk.Label(edit_response_container,
                  text="Select topic:",
                  font=('Arial', 10, 'bold')).pack(pady=5)
        response_topic_var = tk.StringVar()
        response_topic_dropdown = ttk.Combobox(edit_response_container,
                                               textvariable=response_topic_var,
                                               values=list(self.keyword_responses.keys()))
        response_topic_dropdown.pack(pady=(0, 10), fill="x")

        # Personality selection
        ttk.Label(edit_response_container,
                  text="Select personality:",
                  font=('Arial', 10, 'bold')).pack(pady=5)
        personality_var = tk.StringVar()
        personality_dropdown = ttk.Combobox(edit_response_container,
                                            textvariable=personality_var,
                                            values=list(self.personalities.keys()))
        personality_dropdown.pack(pady=(0, 10), fill="x")

        # Response selection
        ttk.Label(edit_response_container,
                  text="Select response:",
                  font=('Arial', 10, 'bold')).pack(pady=5)
        response_var = tk.StringVar()
        response_dropdown = ttk.Combobox(edit_response_container,
                                         textvariable=response_var)
        response_dropdown.pack(pady=(0, 10), fill="x")

        def update_response_dropdowns():
            topic = response_topic_var.get()
            personality = personality_var.get()
            if topic and personality and topic in self.keyword_responses:
                responses = self.keyword_responses[topic].get(personality, [])
                response_dropdown['values'] = responses

        response_topic_dropdown.bind('<<ComboboxSelected>>', lambda e: update_response_dropdowns())
        personality_dropdown.bind('<<ComboboxSelected>>', lambda e: update_response_dropdowns())

        # New response entry
        ttk.Label(edit_response_container,
                  text="New response:",
                  font=('Arial', 10, 'bold')).pack(pady=5)
        new_response_entry = ttk.Entry(edit_response_container, font=('Arial', 10))
        new_response_entry.pack(pady=(0, 20), fill="x")

        def edit_response():
            topic = response_topic_var.get()
            personality = personality_var.get()
            old_response = response_var.get()
            new_response = new_response_entry.get().strip()

            if topic and personality and old_response and new_response:
                responses = self.keyword_responses[topic][personality]
                index = responses.index(old_response)
                responses[index] = new_response
                self.save_responses()
                messagebox.showinfo("Success", "Response updated successfully!")
                new_response_entry.delete(0, tk.END)
                update_topics_display()
                update_response_dropdowns()

        tk.Button(edit_response_container,
                  text="Update Response",
                  command=edit_response,
                  font=('Arial', 10, 'bold'),
                  bg='#4CAF50',
                  fg='white',
                  relief='flat',
                  activebackground='#45a049',
                  padx=20,
                  pady=8,
                  cursor='hand2').pack()

        # Delete topic tab
        delete_topic_frame = ttk.Frame(notebook, style='Green.TFrame')
        notebook.add(delete_topic_frame, text="Delete Topic")

        delete_topic_container = ttk.Frame(delete_topic_frame, style='Green.TFrame')
        delete_topic_container.pack(expand=True, fill="both", padx=20, pady=20)

        ttk.Label(delete_topic_container,
                  text="Delete Topic",
                  style='Header.TLabel').pack(fill="x", pady=(0, 20))

        ttk.Label(delete_topic_container,
                  text="Select topic to delete:",
                  font=('Arial', 10, 'bold')).pack(pady=5)

        delete_topic_var = tk.StringVar()
        delete_topic_dropdown = ttk.Combobox(delete_topic_container,
                                             textvariable=delete_topic_var,
                                             values=list(self.keyword_responses.keys()))
        delete_topic_dropdown.pack(pady=(0, 20), fill="x")

        def delete_topic():
            topic = delete_topic_var.get()
            if topic:
                if messagebox.askyesno("Confirm Delete",
                                       f"Are you sure you want to delete the topic '{topic}'?"):
                    del self.keyword_responses[topic]
                    self.save_responses()
                    messagebox.showinfo("Success", f"Topic '{topic}' deleted successfully!")
                    delete_topic_dropdown['values'] = list(self.keyword_responses.keys())
                    topic_dropdown['values'] = list(self.keyword_responses.keys())
                    response_topic_dropdown['values'] = list(self.keyword_responses.keys())
                    update_topics_display()

        tk.Button(delete_topic_container,
                  text="Delete Topic",
                  command=delete_topic,
                  font=('Arial', 10, 'bold'),
                  bg='#ff4444',
                  fg='white',
                  relief='flat',
                  activebackground='#cc0000',
                  padx=20,
                  pady=8,
                  cursor='hand2').pack()

        # Delete response tab
        delete_response_frame = ttk.Frame(notebook, style='Green.TFrame')
        notebook.add(delete_response_frame, text="Delete Response")

        delete_response_container = ttk.Frame(delete_response_frame, style='Green.TFrame')
        delete_response_container.pack(expand=True, fill="both", padx=20, pady=20)

        ttk.Label(delete_response_container,
                  text="Delete Response",
                  style='Header.TLabel').pack(fill="x", pady=(0, 20))

        # Topic selection for delete
        ttk.Label(delete_response_container,
                  text="Select topic:",
                  font=('Arial', 10, 'bold')).pack(pady=5)
        delete_response_topic_var = tk.StringVar()
        delete_response_topic_dropdown = ttk.Combobox(delete_response_container,
                                                      textvariable=delete_response_topic_var,
                                                      values=list(self.keyword_responses.keys()))
        delete_response_topic_dropdown.pack(pady=(0, 10), fill="x")

        # Personality selection for delete
        ttk.Label(delete_response_container,
                  text="Select personality:",
                  font=('Arial', 10, 'bold')).pack(pady=5)
        delete_personality_var = tk.StringVar()
        delete_personality_dropdown = ttk.Combobox(delete_response_container,
                                                   textvariable=delete_personality_var,
                                                   values=list(self.personalities.keys()))
        delete_personality_dropdown.pack(pady=(0, 10), fill="x")

        # Response selection for delete
        ttk.Label(delete_response_container,
                  text="Select response to delete:",
                  font=('Arial', 10, 'bold')).pack(pady=5)
        delete_response_var = tk.StringVar()
        delete_response_dropdown = ttk.Combobox(delete_response_container,
                                                textvariable=delete_response_var)
        delete_response_dropdown.pack(pady=(0, 20), fill="x")

        def update_delete_response_dropdown():
            topic = delete_response_topic_var.get()
            personality = delete_personality_var.get()
            if topic and personality and topic in self.keyword_responses:
                responses = self.keyword_responses[topic].get(personality, [])
                delete_response_dropdown['values'] = responses

        delete_response_topic_dropdown.bind('<<ComboboxSelected>>',
                                            lambda e: update_delete_response_dropdown())
        delete_personality_dropdown.bind('<<ComboboxSelected>>',
                                         lambda e: update_delete_response_dropdown())

        def delete_response():
            topic = delete_response_topic_var.get()
            personality = delete_personality_var.get()
            response = delete_response_var.get()

            if topic and personality and response:
                if messagebox.askyesno("Confirm Delete",
                                       f"Are you sure you want to delete this response?"):
                    self.keyword_responses[topic][personality].remove(response)
                    self.save_responses()
                    messagebox.showinfo("Success", "Response deleted successfully!")
                    update_topics_display()
                    update_delete_response_dropdown()
                    update_response_dropdowns()

        tk.Button(delete_response_container,
                  text="Delete Response",
                  command=delete_response,
                  font=('Arial', 10, 'bold'),
                  bg='#ff4444',
                  fg='white',
                  relief='flat',
                  activebackground='#cc0000',
                  padx=20,
                  pady=8,
                  cursor='hand2').pack()

        # Add a button to close the config window
        tk.Button(container,
                  text="Close Configuration",
                  command=config_window.destroy,
                  font=('Arial', 10, 'bold'),
                  bg='#808080',
                  fg='white',
                  relief='flat',
                  activebackground='#696969',
                  padx=20,
                  pady=8,
                  cursor='hand2').pack(pady=20)

        # Update the response dropdowns initially
        def update_response_dropdowns():
            response_topic_dropdown['values'] = list(self.keyword_responses.keys())
            delete_response_topic_dropdown['values'] = list(self.keyword_responses.keys())
            delete_topic_dropdown['values'] = list(self.keyword_responses.keys())
            topic_dropdown['values'] = list(self.keyword_responses.keys())

        update_response_dropdowns()

    def start_chat(self):
        self.display_message("System", "Welcome to the University of Poppleton chat!")
        self.display_message(self.agent_name, "What's your name?")

    def show_topics(self):
        topics_list = "\n".join([f"- {topic}" for topic in self.keyword_responses.keys()])
        self.display_message(self.agent_name, f"Here are the available topics:\n{topics_list}")

    def handle_exit(self):
        if messagebox.askyesno("Exit", "Would you like to end the chat?"):
            if messagebox.askyesno("Summary", "Would you like to see a chat summary?"):
                summary = f"""Chat Summary:
- Total questions asked: {len(self.user_questions)}
- Most frequent keywords: {', '.join([kw for kw, _ in self.keyword_tracker.most_common(3)])}"""
                self.display_message("System", summary)
            self.after(2000, self.destroy)

    def load_responses(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Could not load responses file.")
            return {}

    def save_responses(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.keyword_responses, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save responses: {e}")


if __name__ == "__main__":
    app = ChatbotGUI()
    app.mainloop()