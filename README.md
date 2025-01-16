Chatbot Documentation

Overview

The University of Poppleton Chatbot is a graphical user interface (GUI) application built using Python's Tkinter library. It is designed to assist users by simulating a conversation with a chatbot, offering topics for discussion, and allowing administrative configurations.

Features

User Interface

Responsive GUI with styled components.

Rounded corners for all major UI elements.

Scrolled chat display and input box for ease of interaction.

Chat Functionality

Personalized Greeting: The chatbot begins the interaction by asking for the user’s name.

Dynamic Topics: Users can inquire about predefined topics, and the chatbot provides information in an interactive manner.

Multiple Personalities: The chatbot simulates five distinct personalities, each with unique response styles.

Keyword Tracking: Tracks frequently used keywords for improved responses and summarization.

Exit Handling: Graceful exit with optional summary of the chat session.

Administration Mode

Add, Edit, and Delete Topics: Administrators can manage topics dynamically.

Modify Responses: Adjust chatbot responses for specific topics and personalities.

Authentication: Secure login required for configuration access.

Code Structure

Main Components

1. ChatbotGUI Class

Inherits from tk.Tk.

Initializes all necessary configurations, data structures, and GUI components.

Key Attributes:

keyword_responses: Stores topic-response mappings.

personalities: Defines unique response styles for different chatbot personalities.

user_questions: Logs all user interactions for summarization.

Key Methods:

create_widgets(): Constructs the GUI layout and binds events.

start_chat(): Initiates the chatbot interaction.

process_input(): Handles user input and generates responses.

process_keywords(): Matches user input with predefined keywords to provide topic-related responses.

show_admin_login(): Displays the admin login window.

show_config_mode(): Allows administrators to modify topics and responses.

load_responses() & save_responses(): Manages persistence of topic-response data.

handle_exit(): Handles chat termination and provides optional summaries.

2. Configuration Mode

Accessed via "Admin Mode".

Provides the following tabs:

View Topics: Displays all available topics and their associated responses.

Add Topic: Adds new topics to the chatbot’s knowledge base.

Edit Topic: Edits existing topics.

Edit Response: Modifies specific responses for a topic.

Delete Topic/Response: Removes topics or specific responses.

Dependencies

Python Libraries:

tkinter: For building the graphical interface.

random: For personality selection.

re: For keyword matching.

json: For data persistence.

collections.Counter: For tracking keyword usage.

File Structure

main.py: The entry point of the application, containing the ChatbotGUI class and all related methods.

keywords.json: Stores topic-response mappings.
