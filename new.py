import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyD20lbYsJVsDHt5CdZYp4n8r6CIqCZ7uVo')
# List available models
models = genai.list_models()

for model in models:
    print(f"Model ID: {model.name}, Display Name: {model.display_name}")

