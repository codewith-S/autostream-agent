from intent import detect_intent
from rag import get_answer
from tools import mock_lead_capture
from state import state

def chat():
    print("🤖 AutoStream Agent: Hi! How can I help you?\n")

    while True:
        user_input = input("You: ")

        intent = detect_intent(user_input)
        state["intent"] = intent

        # Greeting
        if intent == "greeting":
            print("Agent: Hello! Ask me about our plans or pricing.")

        # Pricing → RAG
        elif intent == "pricing":
            answer = get_answer(user_input)
            print(f"Agent:\n{answer}")

        # High Intent → Start lead capture
        elif intent == "high_intent":
            print("Agent: Great! Let's get you started. What's your name?")
            state["step"] = "name"

        # Lead capture flow
        elif state["step"] == "name":
            state["name"] = user_input
            print("Agent: Please provide your email.")
            state["step"] = "email"

        elif state["step"] == "email":
            state["email"] = user_input
            print("Agent: Which platform do you create content on?")
            state["step"] = "platform"

        elif state["step"] == "platform":
            state["platform"] = user_input

            mock_lead_capture(
                state["name"],
                state["email"],
                state["platform"]
            )

            print("Agent: You're all set! We'll reach out soon.")
            state["step"] = None

        else:
            print("Agent: I'm not sure how to help with that. Try asking about pricing.")

if __name__ == "__main__":
    chat()