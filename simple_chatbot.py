import tkinter as tk
from tkinter import scrolledtext
import spacy
import random

class AdvancedChatbot:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Chatbot")
        self.master.geometry("500x600")
        
        # Load the spaCy model
        self.nlp = spacy.load("en_core_web_sm")

        # Create the chat window
        self.chat_window = scrolledtext.ScrolledText(self.master, state='disabled', wrap='word', font=("Arial", 12))
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create the user input field
        self.user_input = tk.Entry(self.master, font=("Arial", 12))
        self.user_input.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.user_input.bind("<Return>", self.send_message)

        # Add a send button
        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack(pady=(0, 10))

        # Display initial greeting
        self.display_message("Chatbot: Hello! How can I assist you today? Type 'help' for options.")

    def send_message(self, event=None):
        user_text = self.user_input.get()
        if user_text:
            self.display_message(f"You: {user_text}")
            self.user_input.delete(0, tk.END)
            response = self.chatbot_response(user_text)
            self.display_message(f"Chatbot: {response}")

    def display_message(self, message):
        self.chat_window.configure(state='normal')
        self.chat_window.insert(tk.END, message + '\n')
        self.chat_window.configure(state='disabled')
        self.chat_window.yview(tk.END)  # Auto-scroll to the bottom

    def chatbot_response(self, user_input):
        user_input = user_input.lower()
        doc = self.nlp(user_input)

        # Identify intent based on keywords
        if any(token.lemma_ in ["hello", "hi", "greetings"] for token in doc):
            return "Hello! How can I assist you today? If you're unsure, type 'help' for options."

        elif "help" in user_input:
            return ("I can assist you with the following topics:\n"
                    "1. General inquiries\n"
                    "2. Product information\n"
                    "3. Support issues\n"
                    "4. Feedback\n"
                    "5. Exit\n"
                    "Please type the number of your choice.")

        elif any(token.lemma_ in ["general", "inquiry", "question"] for token in doc):
            return "What would you like to know about? You can ask me about our services, hours, or location."

        elif any(token.lemma_ in ["product", "information"] for token in doc):
            return "We offer a variety of products. Are you looking for specific items or categories?"

        elif any(token.lemma_ in ["support", "issue", "problem"] for token in doc):
            return "Please describe the issue you're facing, and I'll do my best to help you."

        elif any(token.lemma_ in ["feedback", "suggestion"] for token in doc):
            return "We appreciate your feedback! Please share your thoughts, and I'll forward them to the team."

        elif any(token.lemma_ in ["bye", "exit", "quit"] for token in doc):
            return "Goodbye! Have a great day!"

        else:
            return "I'm sorry, I don't understand that. Can you please be more specific?"

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = AdvancedChatbot(root)
    root.mainloop()

