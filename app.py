import requests
import google.generativeai as genai

# 🔵 Gemini setup
genai.configure(api_key="AIzaSyAkYj6EODs98Ea35gb6rQMhRM1D7BV_Xo8")

model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

# 🟢 Ollama setup
def ask_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "phi3", "prompt": prompt}
    )
    return response.json()["response"]

# 🔁 Smart router
def ask_ai(prompt):
    if len(prompt) < 100:
        return ask_ollama(prompt)
    else:
        return ask_gemini(prompt)

# 🚀 Run loop
while True:
    user_input = input("You: ")
    
    if user_input.lower() == "exit":
        break
    
    response = ask_ai(user_input)
    print("AI:", response)