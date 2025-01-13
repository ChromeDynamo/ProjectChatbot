import random
import re
import json
from collections import Counter


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


def save_responses(filename, data):
    """Save keyword responses to a JSON file."""
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
            print("Responses saved successfully!")
    except Exception as e:
        print(f"Error: Could not save responses. {e}")


def get_confirmation(user_input):
    """
    Determines if the user's input is a 'yes' or 'no' response based on synonyms.
    Returns 'yes', 'no', or None if neither is detected.
    """
    yes_synonyms = {"yes", "yea", "yeah", "sure", "okay", "ok", "yep", "alright"}
    no_synonyms = {"no", "nah", "nope", "not really", "no thanks"}

    # Normalize input and check against synonyms
    normalized_input = user_input.strip().lower()
    if any(word in normalized_input for word in yes_synonyms):
        return "yes"
    elif any(word in normalized_input for word in no_synonyms):
        return "no"
    return None


def admin_login():
    """Handles admin login for configuration mode."""
    username = input("Enter admin username: ").strip()
    password = input("Enter admin password: ").strip()

    if username == "admin" and password == "admin123":
        print("Access granted. Welcome to Configuration Mode!")
        return True
    else:
        print("Access denied. Incorrect username or password.")
        return False


def configuration_mode(keyword_responses, filename):
    """
    Configuration mode to view, add, edit, or delete topics and responses.
    """
    personalities = ["Alex", "Jordan", "Taylor", "Morgan", "Casey"]  # List of chatbot personalities

    while True:
        print("\nConfiguration Mode Options:")
        print("1. View all topics and responses")
        print("2. Add a new topic")
        print("3. Add a new response to an existing topic")
        print("4. Delete a topic")
        print("5. Delete a specific response from a topic")
        print("6. Exit Configuration Mode")
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            print("\nTopics and Responses:")
            for topic, responses in keyword_responses.items():
                print(f"- {topic}:")
                if isinstance(responses, dict):
                    for personality, response_list in responses.items():
                        print(f"  {personality}:")
                        for response in response_list:
                            print(f"    - {response}")
                else:
                    print(f"  Responses: {responses}")
        elif choice == "2":
            new_topic = input("Enter the new topic keyword: ").strip()
            if new_topic in keyword_responses:
                print(f"Topic '{new_topic}' already exists!")
            else:
                # Initialize the topic with personality-based response dictionaries
                keyword_responses[new_topic] = {personality: [] for personality in personalities}
                print(f"Topic '{new_topic}' added successfully!")
        elif choice == "3":
            existing_topic = input("Enter the topic to add a response to: ").strip()
            if existing_topic in keyword_responses:
                print(f"Available personalities: {', '.join(personalities)}")
                personality = input("Enter the personality to add a response for: ").strip()
                if personality in personalities:
                    new_response = input(f"Enter the new response for '{existing_topic}' ({personality}): ").strip()
                    keyword_responses[existing_topic][personality].append(new_response)
                    print(f"Response added to topic '{existing_topic}' for {personality}!")
                else:
                    print(f"Invalid personality: {personality}")
            else:
                print(f"Topic '{existing_topic}' does not exist.")
        elif choice == "4":
            topic_to_delete = input("Enter the topic keyword to delete: ").strip()
            if topic_to_delete in keyword_responses:
                del keyword_responses[topic_to_delete]
                print(f"Topic '{topic_to_delete}' deleted successfully!")
            else:
                print(f"Topic '{topic_to_delete}' does not exist.")
        elif choice == "5":
            topic_to_edit = input("Enter the topic to delete a response from: ").strip()
            if topic_to_edit in keyword_responses:
                print(f"Available personalities: {', '.join(personalities)}")
                personality = input("Enter the personality to delete a response for: ").strip()
                if personality in personalities:
                    if personality in keyword_responses[topic_to_edit]:
                        print(f"Responses for '{topic_to_edit}' ({personality}):")
                        for i, response in enumerate(keyword_responses[topic_to_edit][personality], start=1):
                            print(f"{i}. {response}")
                        response_index = input("Enter the number of the response to delete: ").strip()
                        if response_index.isdigit() and 1 <= int(response_index) <= len(keyword_responses[topic_to_edit][personality]):
                            removed_response = keyword_responses[topic_to_edit][personality].pop(int(response_index) - 1)
                            print(f"Response '{removed_response}' deleted from topic '{topic_to_edit}' ({personality})!")
                        else:
                            print("Invalid response number.")
                    else:
                        print(f"No responses found for personality '{personality}'.")
                else:
                    print(f"Invalid personality: {personality}")
            else:
                print(f"Topic '{topic_to_edit}' does not exist.")
        elif choice == "6":
            save_responses(filename, keyword_responses)
            print("Exiting Configuration Mode...")
            break
        else:
            print("Invalid choice. Please try again.")


def chatbot():
    # Load keyword responses from JSON file
    filename = "keywords.json"
    keyword_responses = load_responses(filename)
    if not keyword_responses:
        print("Chatbot cannot start without valid responses.")
        return

    # Initialize session data
    user_questions = []
    keyword_tracker = Counter()

    # Greet the user
    user_name = input("Welcome to the University of Poppleton chat! What's your name? ")
    print(f"Hello {user_name}, it's great to meet you!")

    # Assign a random agent name and personality
    personalities = {
        "Alex": "quirky and loves puns",
        "Jordan": "friendly and empathetic",
        "Taylor": "witty with a touch of sarcasm",
        "Morgan": "calm and professional",
        "Casey": "playful and loves jokes"
    }
    agent_names = list(personalities.keys())
    agent_name = random.choice(agent_names)
    print(f"My name is {agent_name}, and I’m {personalities[agent_name]}. Type 'bye' to exit the chat.")

    # Ask if the user wants a list of available topics
    print(f"{agent_name}: Would you like a list of available topics?")
    confirmation = input(f"{user_name}: ")
    if get_confirmation(confirmation) == "yes":
        print(f"{agent_name}: Here are the available topics:")
        for topic in keyword_responses.keys():  # Dynamically fetch topics from the current data
            print(f"- {topic}")
    else:
        print(f"{agent_name}: No problem! Let me know if there's anything else you'd like to discuss.")

    # Fallback responses
    fallback_responses = {
        "Alex": ["I'm not sure, but let's wing it!", "Oops, my brain froze! Ask me that again?", "Oh, this is tricky. Let me think!"],
        "Jordan": ["I'm not sure, but I'm here to help.", "That’s an interesting question! Let's figure it out.", "Hmm, let me dig deeper on that!"],
        "Taylor": ["You stumped me there, but I'll give it a go!", "Wow, tricky one. Let’s see...", "Can't guarantee brilliance, but I'll try!"],
        "Morgan": ["I'm not certain about that, but let's find a solution.", "Let me gather my thoughts on that.", "I'm here to assist. Let's refine your question."],
        "Casey": ["Whoa! That's above my pay grade, but I'll try!", "Hold up, let me boot my brain!", "Interesting! Let’s unpack that."]
    }

    # Chat loop
    while True:
        user_input = input(f"{user_name}: ")

        # Track user input
        user_questions.append(user_input)

        # Detect "bye", "exit", "quit" in the sentence
        if re.search(r"\b(bye|exit|quit)\b", user_input, re.IGNORECASE):
            print(f"{agent_name}: It sounds like you want to end the chat. Is that correct?")
            confirmation = input(f"{user_name}: ")
            if get_confirmation(confirmation) == "yes":
                print(f"{agent_name}: Goodbye {user_name}! Have a great day!")

                # Offer session summary
                print(f"{agent_name}: Would you like a summary of our chat session?")
                summary_confirmation = input(f"{user_name}: ")
                if get_confirmation(summary_confirmation) == "yes":
                    print(f"{agent_name}: Here's your session summary:")
                    print(f"- Total questions asked: {len(user_questions)}")
                    print(f"- Most frequent keywords: {', '.join([kw for kw, _ in keyword_tracker.most_common(3)])}")
                break
            else:
                print(f"{agent_name}: Alright, let's continue!")

        # Detect keywords for topics
        elif re.search(r"\b(topics|topic|topic list|topics list)\b", user_input, re.IGNORECASE):
            print(f"{agent_name}: Would you like me to show the topic list again?")
            confirmation = input(f"{user_name}: ")
            if get_confirmation(confirmation) == "yes":
                # Dynamically fetch the current list of topics
                print(f"{agent_name}: Here are the available topics:")
                for topic in keyword_responses.keys():
                    print(f"- {topic}")
            else:
                print(f"{agent_name}: No problem! Let me know if there's anything else you'd like to discuss.")

        # Detect keywords for configuration mode
        elif re.search(r"\b(admin|administrator|admin mode|config|configuration mode)\b", user_input, re.IGNORECASE):
            print(f"{agent_name}: Entering Configuration Mode requires authentication.")
            if admin_login():
                configuration_mode(keyword_responses, filename)
                # Reload responses after configuration mode to reflect changes
                keyword_responses = load_responses(filename)
            else:
                print(f"{agent_name}: Authentication failed. Returning to chat mode.")

        # Detect keywords from JSON
        else:
            found_keyword = False
            for keyword, responses in keyword_responses.items():
                if re.search(rf"\b{keyword}\b", user_input, re.IGNORECASE):
                    keyword_tracker[keyword] += 1
                    response_iter = iter(responses)  # Create an iterator for the responses

                    print(f"{agent_name}: {next(response_iter)}")  # Provide the first response
                    found_keyword = True

                    # Ask if the user wants to know more
                    while True:
                        print(f"{agent_name}: Would you like to know more about {keyword}?")
                        confirmation = input(f"{user_name}: ")
                        if get_confirmation(confirmation) == "yes":
                            try:
                                print(f"{agent_name}: {next(response_iter)}")  # Provide the next response
                            except StopIteration:
                                print(f"{agent_name}: Sorry, I've run out of information about {keyword}.")
                                break
                        else:
                            print(f"{agent_name}: No problem! Let me know if there's anything else you'd like to discuss.")
                            break
                    break

            # Fallback response if no keyword is found
            if not found_keyword:
                print(f"{agent_name}: {random.choice(fallback_responses[agent_name])}")

# Run the chatbot
if __name__ == "__main__":
    chatbot()