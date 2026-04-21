import json

def load_data():
    with open("data.json", "r") as file:
        return json.load(file)

data = load_data()

def get_answer(query):
    query = query.lower()

    if any(word in query for word in ["price", "pricing", "plan", "cost"]):
        response = ""
        for plan in data["plans"]:
            response += f"{plan['name']} Plan: {plan['price']}, Features: {', '.join(plan['features'])}\n"
        return response

    elif "refund" in query or "policy" in query:
        return "\n".join(data["policies"])

    return "Sorry, I couldn't find that information."