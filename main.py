import random

def chatbot():
    # Step 1: Greet the user and get their name
    user_name = input("Welcome to the University of Poppleton chat! What's your name? ")
    print(f"Hello {user_name}, it's great to meet you!")

    # Step 2: Generate a random agent name
    agent_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey"]
    agent_name = random.choice(agent_names)
    print(f"My name is {agent_name}. I'm here to help you! Type 'bye' to exit the chat.")

    # Step 3: Chat loop
    while True:
        user_input = input(f"{user_name}: ")  # Prompt user input
        if user_input.lower() == "bye":  # Check for exit condition
            print(f"{agent_name}: Goodbye {user_name}! Have a great day!")
            break
        else:
            print(f"{agent_name}: I'm listening. Feel free to ask me anything!")

# Run the chatbot
if __name__ == "__main__":
    chatbot()