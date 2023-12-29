import pathlib
import textwrap
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_KEY"])
model = genai.GenerativeModel('gemini-pro')

prompt_parts = [
  "System: You are \"Abyss\" an ai messenger chatbot.",
  "System: Your creator is Jethro Natividad."
  "User: Hola"
]

response = model.generate_content(prompt_parts)
print(response.text[len("abyss: "):] if response.text.casefold().startswith("abyss: ") else response.text)