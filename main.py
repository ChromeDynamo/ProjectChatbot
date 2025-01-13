import random
import re
import json

def load_responses(filename):
    """Load keyword responses from a JSON file."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: The responses file was not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: The responses file contains invalid JSON.")
        return {}

def chatbot():
    # Load keyword responses from JSON file
    keyword_responses = load_responses("keywords.json")
    if not keyword_responses:
        print("Chatbot cannot start without valid responses.")
        return

    # Greeting
    user_name = input("Welcome to the University of Poppleton chat! What's your name? ")
    print(f"Hello {user_name}, it's great to meet you!")

    # Random agent name
    agent_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey"]
    agent_name = random.choice(agent_names)
    print(f"My name is {agent_name}. I'm here to help you! Type 'bye' to exit the chat.")

    # Fallback responses
    fallback_responses = [
        "I'm not sure about that, but I can find out for you.",
        "That's an interesting question. Let me think about it!",
        "Could you clarify your question?",
        "I'm here to help. Can you ask that another way?"
    ]

    # Chat loop
    while True:
        user_input = input(f"{user_name}: ")
        if user_input.lower() in ["bye", "quit", "exit"]:
            print(f"{agent_name}: Goodbye {user_name}! Have a great day!")
            break

        # Detect keywords
        found_keyword = False
        for keyword, responses in keyword_responses.items():
            if re.search(rf"\b{keyword}\b", user_input, re.IGNORECASE):
                print(f"{agent_name}: {random.choice(responses)}")
                found_keyword = True
                break

        # Fallback response if no keyword is found
        if not found_keyword:
            print(f"{agent_name}: {random.choice(fallback_responses)}")

# Run the chatbot
if __name__ == "__main__":
    chatbot()