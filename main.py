import random
import re


def chatbot():
    # Step 1: Greet the user and get their name
    user_name = input("Welcome to the University of Poppleton chat! What's your name? ")
    print(f"Hello {user_name}, it's great to meet you!")

    # Step 2: Generate a random agent name
    agent_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey"]
    agent_name = random.choice(agent_names)
    print(f"My name is {agent_name}. I'm here to help you! Type 'bye' to exit the chat.")

    # Step 3: Keyword responses
    keyword_responses = {
        "coffee": "The campus coffee shop is open from 8 AM to 8 PM daily.",
        "library": "The library is open 24/7 for students with a valid ID.",
        "courses": "You can explore our wide range of courses on our website.",
        "location": "The university is located in the heart of Poppleton."
    }

    # Fallback responses
    fallback_responses = [
        "I'm not sure about that, but I can find out for you.",
        "That's an interesting question. Let me think about it!",
        "Could you clarify your question?",
        "I'm here to help. Can you ask that another way?"
    ]

    # Step 4: Chat loop
    while True:
        user_input = input(f"{user_name}: ")
        if user_input.lower() in ["bye", "quit", "exit"]:
            print(f"{agent_name}: Goodbye {user_name}! Have a great day!")
            break

        # Detect keywords
        found_keyword = False
        for keyword, response in keyword_responses.items():
            if re.search(rf"\b{keyword}\b", user_input, re.IGNORECASE):
                print(f"{agent_name}: {response}")
                found_keyword = True
                break

        # Fallback response if no keyword is found
        if not found_keyword:
            print(f"{agent_name}: {random.choice(fallback_responses)}")


# Run the chatbot
if __name__ == "__main__":
    chatbot()