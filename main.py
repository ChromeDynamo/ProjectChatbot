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


def chatbot():
    # Load keyword responses from JSON file
    keyword_responses = load_responses("keywords.json")
    if not keyword_responses:
        print("Chatbot cannot start without valid responses.")
        return

    # List of available topics
    available_topics = ["Cafe hours", "Library services", "Course details", "Campus location"]

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
        for topic in available_topics:
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

        # Detect "topics" and its synonyms
        elif re.search(r"\b(topics|topic|topic list|topics list)\b", user_input, re.IGNORECASE):
            print(f"{agent_name}: Would you like me to show the topic list again?")
            confirmation = input(f"{user_name}: ")
            if get_confirmation(confirmation) == "yes":
                print(f"{agent_name}: Here are the available topics:")
                for topic in available_topics:
                    print(f"- {topic}")
            else:
                print(f"{agent_name}: No problem! Let me know if there's anything else you'd like to discuss.")

        # Detect keywords from JSON
        else:
            found_keyword = False
            for keyword, responses in keyword_responses.items():
                if re.search(rf"\b{keyword}\b", user_input, re.IGNORECASE):
                    keyword_tracker[keyword] += 1
                    personality_responses = responses.get(agent_name, [])
                    response_iter = iter(personality_responses)  # Create an iterator for the responses

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