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

        # Window setup
        self.title("University of Poppleton Chatbot")
        self.geometry("800x600")

        # Create main container
        self.create_widgets()

        # Start chat
        self.start_chat()

    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(expand=True, fill="both", padx=10, pady=10)

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(main_container, wrap=tk.WORD, height=20)
        self.chat_display.pack(expand=True, fill="both", pady=(0, 10))

        # Input area
        input_frame = ttk.Frame(main_container)
        input_frame.pack(fill="x")

        self.user_input = ttk.Entry(input_frame)
        self.user_input.pack(side="left", expand=True, fill="x", padx=(0, 5))

        send_button = ttk.Button(input_frame, text="Send", command=self.process_input)
        send_button.pack(side="right")

        # Bind Enter key to send message
        self.user_input.bind("<Return>", lambda e: self.process_input())

        # Admin button
        admin_button = ttk.Button(main_container, text="Admin Mode", command=self.show_admin_login)
        admin_button.pack(pady=(10, 0))

    def display_message(self, sender, message):
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.see(tk.END)

    def process_input(self):
        user_input = self.user_input.get().strip()
        if not user_input:
            return

        self.user_input.delete(0, tk.END)
        self.display_message("You", user_input)

        # Track user input
        self.user_questions.append(user_input)

        # Process the input
        if re.search(r"\b(bye|exit|quit)\b", user_input, re.IGNORECASE):
            self.handle_exit()
        elif re.search(r"\b(topics|topic|topic list|topics list)\b", user_input, re.IGNORECASE):
            self.show_topics()
        else:
            self.process_keywords(user_input)

    def process_keywords(self, user_input):
        found_keyword = False
        for keyword, responses in self.keyword_responses.items():
            if re.search(rf"\b{keyword}\b", user_input, re.IGNORECASE):
                self.keyword_tracker[keyword] += 1
                if isinstance(responses, dict) and self.agent_name in responses:
                    response = random.choice(responses[self.agent_name])
                    self.display_message(self.agent_name, response)
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
        login_window.geometry("300x150")

        ttk.Label(login_window, text="Username:").pack(pady=5)
        username_entry = ttk.Entry(login_window)
        username_entry.pack(pady=5)

        ttk.Label(login_window, text="Password:").pack(pady=5)
        password_entry = ttk.Entry(login_window, show="*")
        password_entry.pack(pady=5)

        def try_login():
            if username_entry.get() == "admin" and password_entry.get() == "admin123":
                login_window.destroy()
                self.show_config_mode()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        ttk.Button(login_window, text="Login", command=try_login).pack(pady=10)

    def show_config_mode(self):
        config_window = tk.Toplevel(self)
        config_window.title("Configuration Mode")
        config_window.geometry("600x400")

        # Create notebook for different operations
        notebook = ttk.Notebook(config_window)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # View topics tab
        view_frame = ttk.Frame(notebook)
        notebook.add(view_frame, text="View Topics")

        topics_display = scrolledtext.ScrolledText(view_frame)
        topics_display.pack(expand=True, fill="both", padx=5, pady=5)

        for topic, responses in self.keyword_responses.items():
            topics_display.insert(tk.END, f"Topic: {topic}\n")
            if isinstance(responses, dict):
                for personality, response_list in responses.items():
                    topics_display.insert(tk.END, f"  {personality}:\n")
                    for response in response_list:
                        topics_display.insert(tk.END, f"    - {response}\n")
            topics_display.insert(tk.END, "\n")

        # Add topic tab
        add_frame = ttk.Frame(notebook)
        notebook.add(add_frame, text="Add Topic")

        ttk.Label(add_frame, text="Topic name:").pack(pady=5)
        topic_entry = ttk.Entry(add_frame)
        topic_entry.pack(pady=5)

        def add_topic():
            topic = topic_entry.get().strip()
            if topic:
                if topic not in self.keyword_responses:
                    self.keyword_responses[topic] = {personality: [] for personality in self.personalities}
                    self.save_responses()
                    messagebox.showinfo("Success", f"Topic '{topic}' added successfully!")
                    topic_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", f"Topic '{topic}' already exists!")

        ttk.Button(add_frame, text="Add Topic", command=add_topic).pack(pady=10)

    def start_chat(self):
        welcome_msg = "Welcome to the University of Poppleton chat!"
        self.display_message("System", welcome_msg)

        intro_msg = f"I'm {self.agent_name}, and I'm {self.personalities[self.agent_name]}."
        self.display_message(self.agent_name, intro_msg)

        topics_msg = "Would you like to see the available topics? (yes/no)"
        self.display_message(self.agent_name, topics_msg)

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