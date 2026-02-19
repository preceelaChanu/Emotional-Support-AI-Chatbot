from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from transformers import pipeline

class ActionGenerateResponse(Action):
    def name(self):
        return "action_generate_response"

    # Load models once for efficiency
    generator = pipeline("text-generation", model="distilgpt2")
    sentiment_analyzer = pipeline("sentiment-analysis")

    def get_sentiment_response(self, user_message):
        """Analyzes sentiment and provides an initial supportive response."""
        sentiment = self.sentiment_analyzer(user_message)[0]
        
        if sentiment["label"] == "NEGATIVE":
            return "I'm really sorry you're feeling this way. You're not alone, and I'm here for you. "
        elif sentiment["label"] == "POSITIVE":
            return "That’s great to hear! I’m happy for you! "
        else:
            return "I hear you, and I'm here to listen. "

    def run(self, dispatcher, tracker, domain):
        """Generates an emotionally supportive response based on user input."""
        
        # Get the latest user message
        user_message = tracker.latest_message.get("text", "How can I support you?")
        
        # Generate sentiment-based response first
        sentiment_response = self.get_sentiment_response(user_message)
        
        # Improved prompt for better coherence and warmth
        prompt = f"You are a compassionate AI supporting someone who says '{user_message}'. Respond with kindness, understanding, and encouragement."

        # Generate a response using DistilGPT-2
        response = self.generator(
            prompt,
            max_length=150,  # Allowing longer responses for engagement
            num_return_sequences=1,
            temperature=0.6,  # Lowered for more coherent responses
            top_k=30,         # Focusing on meaningful words
            top_p=0.85        # Balancing diversity and fluency
        )[0]["generated_text"]

        # Clean response by removing prompt
        response = response.replace(prompt, "").strip()

        # Ensure fallback response in case of poor generation
        if not response or len(response) < 15:
            response = "I'm here for you. You are not alone, and I want to support you. Would you like to share more?"

        # Final message combines sentiment response + generated response
        final_response = sentiment_response + response

        # Send response to the user
        dispatcher.utter_message(text=final_response)
        return []
