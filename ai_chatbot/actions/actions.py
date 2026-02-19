"""
EmpathicAI - Custom Actions
Implements sentiment analysis and empathetic response generation.
"""

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# VADER Sentiment Analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Ensure VADER lexicon is downloaded
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)


class SentimentAnalyzer:
    """
    Sentiment analyzer using VADER (Valence Aware Dictionary and sEntiment Reasoner).
    Provides compound scores and emotion detection.
    """
    
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        
        # Emotion keywords for more nuanced detection
        self.emotion_keywords = {
            'sadness': ['sad', 'depressed', 'unhappy', 'miserable', 'hopeless', 'cry', 'crying', 
                       'tears', 'grief', 'heartbroken', 'devastated', 'empty', 'worthless', 'down'],
            'anxiety': ['anxious', 'worried', 'nervous', 'panic', 'afraid', 'restless', 'uneasy',
                       'tense', 'overthinking', 'racing', 'dread', 'overwhelmed', 'freaking'],
            'stress': ['stressed', 'pressure', 'overwhelmed', 'exhausted', 'burnout', 'burnt out',
                      'overworked', 'deadline', 'too much', 'drowning', 'swamped'],
            'loneliness': ['lonely', 'alone', 'isolated', 'nobody', 'no one', 'abandoned', 
                          'disconnected', 'invisible', 'forgotten', 'outsider'],
            'anger': ['angry', 'furious', 'mad', 'frustrated', 'irritated', 'annoyed', 'rage',
                     'hate', 'pissed', 'fed up', 'enraged'],
            'fear': ['scared', 'terrified', 'frightened', 'fear', 'fearful', 'horrified',
                    'threatened', 'uncertain', 'insecure'],
            'joy': ['happy', 'joyful', 'excited', 'grateful', 'blessed', 'wonderful', 'amazing',
                   'great', 'fantastic', 'good', 'positive', 'hopeful', 'content']
        }
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment and detect primary emotion from text.
        
        Returns:
            Dict containing sentiment_score, emotion, and confidence
        """
        # Get VADER scores
        scores = self.analyzer.polarity_scores(text)
        compound_score = scores['compound']
        
        # Detect primary emotion based on keywords
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Determine primary emotion
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
        elif compound_score >= 0.05:
            primary_emotion = 'joy'
        elif compound_score <= -0.05:
            primary_emotion = 'sadness'
        else:
            primary_emotion = 'neutral'
        
        return {
            'sentiment_score': compound_score,
            'emotion': primary_emotion,
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'confidence': abs(compound_score)
        }


# Initialize global sentiment analyzer
sentiment_analyzer = SentimentAnalyzer()


class ActionAnalyzeSentiment(Action):
    """
    Analyzes user message sentiment and sets appropriate slots.
    This action runs sentiment analysis on the latest user message.
    """
    
    def name(self) -> Text:
        return "action_analyze_sentiment"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest user message
        user_message = tracker.latest_message.get('text', '')
        
        # Analyze sentiment
        analysis = sentiment_analyzer.analyze(user_message)
        
        # Return slot updates
        return [
            SlotSet("current_emotion", analysis['emotion']),
            SlotSet("sentiment_score", analysis['sentiment_score'])
        ]


class ActionEmpatheticResponse(Action):
    """
    Generates an empathetic response based on detected emotion and sentiment.
    """
    
    def name(self) -> Text:
        return "action_empathetic_response"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_emotion = tracker.get_slot("current_emotion")
        sentiment_score = tracker.get_slot("sentiment_score") or 0.0
        
        # Get user message for context
        user_message = tracker.latest_message.get('text', '')
        
        # Generate response based on emotion
        responses = {
            'sadness': [
                "I'm truly sorry you're experiencing this pain. Your feelings are completely valid, and it takes courage to share them.",
                "It sounds like you're going through a really difficult time. I'm here to listen and support you through this.",
                "I hear the sadness in your words. Please know that you don't have to face this alone."
            ],
            'anxiety': [
                "I understand that anxiety can feel overwhelming. Let's take a moment together. You're safe here with me.",
                "It sounds like your mind is carrying a heavy load right now. Would you like to try a calming technique together?",
                "Anxiety can make everything feel urgent and scary. Let's slow down and breathe together."
            ],
            'stress': [
                "It sounds like you're under tremendous pressure. Remember, it's okay to take things one step at a time.",
                "I hear how overwhelmed you're feeling. Your well-being matters more than any deadline.",
                "Stress can feel like it's consuming everything. Let's find a way to lighten that load together."
            ],
            'loneliness': [
                "Feeling lonely is incredibly painful. I want you to know that reaching out like this shows real strength.",
                "Loneliness can feel so isolating, but you're not alone right now. I'm here with you.",
                "I hear you, and I'm glad you chose to talk. Human connection matters, and so do you."
            ],
            'anger': [
                "Your frustration is completely understandable. It's okay to feel angry — your emotions are telling you something important.",
                "I can hear how upset you are. Sometimes anger is our heart's way of saying something needs to change.",
                "It's clear something has really affected you. I'm here to listen without judgment."
            ],
            'fear': [
                "Fear can feel paralyzing, but you've taken a brave step by reaching out. I'm here with you.",
                "It's completely natural to feel afraid, especially when things feel uncertain. You're not alone.",
                "I hear that you're scared. Whatever happens, we can face this moment together."
            ],
            'joy': [
                "I'm so glad to hear you're feeling good! It's wonderful to celebrate these positive moments.",
                "That's beautiful to hear! Positive feelings are precious — thank you for sharing them with me.",
                "Your happiness is contagious! I'd love to hear more about what's bringing you joy."
            ],
            'neutral': [
                "I'm here whenever you want to talk. Is there something specific on your mind?",
                "Thank you for reaching out. I'm here to listen — whatever you'd like to share.",
                "I'm here for you. Feel free to share whatever's on your heart."
            ]
        }
        
        # Select response based on emotion
        import random
        emotion_responses = responses.get(current_emotion, responses['neutral'])
        response = random.choice(emotion_responses)
        
        # Add intensity modifier for very negative sentiment
        if sentiment_score and sentiment_score < -0.6:
            response = "I can sense you're really struggling right now. " + response
        
        dispatcher.utter_message(text=response)
        return []


class ActionProvideCopingStrategy(Action):
    """
    Provides appropriate coping strategies based on the user's emotional state.
    """
    
    def name(self) -> Text:
        return "action_provide_coping_strategy"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_emotion = tracker.get_slot("current_emotion")
        
        strategies = {
            'sadness': """Here are some gentle strategies that might help:

🌿 **Grounding Exercise**: Place your feet firmly on the ground. Notice the sensation. You are here, in this moment.

📝 **Journaling**: Write down three things you're feeling without judgment. Sometimes putting words to emotions helps process them.

🤗 **Self-Compassion**: Place your hand on your heart and say "This is hard, and it's okay to feel this way."

💬 **Reach Out**: Consider talking to a trusted friend, family member, or professional.""",
            
            'anxiety': """Let's try some calming techniques together:

🌬️ **Box Breathing**: Breathe in for 4 counts, hold for 4, breathe out for 4, hold for 4. Repeat 4 times.

👐 **5-4-3-2-1 Grounding**: Name 5 things you see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.

🧊 **Cold Water Technique**: Splash cold water on your face or hold an ice cube. This activates your dive reflex and slows your heart rate.

🚶 **Gentle Movement**: A short walk, even for 5 minutes, can help release anxious energy.""",
            
            'stress': """Here are some strategies to help manage overwhelm:

📋 **Brain Dump**: Write down everything on your mind. Getting it out of your head can provide relief.

🎯 **One Thing Focus**: Pick just ONE task for the next 30 minutes. Everything else can wait.

⏸️ **Permission to Pause**: Set a timer for 10 minutes and do absolutely nothing. Rest is productive.

🌳 **Nature Break**: If possible, step outside for fresh air. Even looking at nature through a window helps.""",
            
            'loneliness': """Connection strategies that might help:

💬 **Reach Out**: Send a simple "thinking of you" message to someone. Small connections matter.

🌐 **Community**: Consider joining an online community around something you enjoy.

📱 **Video Call**: A face-to-face conversation, even virtual, can feel more connecting than text.

🐾 **Companion Time**: If you have a pet, spend some quality time with them. If not, watching animal videos can boost mood.""",
            
            'anger': """Healthy ways to process anger:

🏃 **Physical Release**: Exercise, punch a pillow, or do jumping jacks to release the physical energy of anger.

📝 **Write It Out**: Write an angry letter you'll never send. Let it all out on paper.

⏰ **Time Out**: If in a conflict, say "I need 20 minutes to calm down before we continue."

🌊 **Cold Water**: Splash cold water on your face — it activates your parasympathetic nervous system.""",
            
            'fear': """Strategies to work through fear:

🌬️ **Breath Work**: Slow, deep breaths signal to your brain that you're safe. Try breathing out longer than you breathe in.

💭 **Name It**: Say "I notice I'm feeling fear." Naming emotions reduces their intensity.

📊 **Reality Check**: Ask yourself "What's the evidence for and against my feared outcome?"

👣 **Small Step**: If fear is blocking action, ask "What's the smallest possible step I could take?" """,
            
            'joy': """Ways to savor positive emotions:

📸 **Capture It**: Take a photo or write about this moment to revisit later.

🙏 **Gratitude**: Take a moment to appreciate what's contributing to your happiness.

📢 **Share It**: Telling others about good news can amplify positive feelings.

🎉 **Celebrate**: Allow yourself to fully experience the joy without dismissing it."""
        }
        
        strategy = strategies.get(current_emotion, """Here are some general wellness strategies:

🌬️ **Deep Breathing**: Take 5 slow, deep breaths.
🚶 **Movement**: A short walk can shift your state.
💧 **Hydrate**: Drink a glass of water.
🌿 **Nature**: Spend a few minutes outdoors if possible.""")
        
        dispatcher.utter_message(text=strategy)
        return []


class ActionProvideResources(Action):
    """
    Provides mental health resources and hotlines.
    """
    
    def name(self) -> Text:
        return "action_provide_resources"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        resources = """Here are some professional resources that can help:

📞 **Crisis Hotlines:**
• National Suicide Prevention Lifeline (US): 988 or 1-800-273-8255
• Crisis Text Line: Text HOME to 741741
• International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

🌐 **Online Resources:**
• 7 Cups (Free Online Chat): https://www.7cups.com
• BetterHelp (Online Therapy): https://www.betterhelp.com
• Psychology Today Therapist Finder: https://www.psychologytoday.com/us/therapists

📱 **Mental Health Apps:**
• Calm - Meditation & Sleep
• Headspace - Mindfulness
• Woebot - AI Therapy Chatbot
• Daylio - Mood Tracking

📚 **Self-Help Resources:**
• NAMI (National Alliance on Mental Illness): https://www.nami.org
• Mind (UK): https://www.mind.org.uk
• Beyond Blue (Australia): https://www.beyondblue.org.au

Remember: Seeking professional help is a sign of strength, not weakness. You deserve support. 💙"""
        
        dispatcher.utter_message(text=resources)
        return []


class ActionActiveListening(Action):
    """
    Provides active listening responses to make user feel heard.
    """
    
    def name(self) -> Text:
        return "action_active_listening"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        import random
        
        responses = [
            "I'm here, and I'm listening. Take all the time you need — there's no rush.",
            "I'm giving you my full attention. Please share whatever feels right.",
            "This is your space to express yourself freely. I'm here to listen without judgment.",
            "I hear you. Sometimes we just need someone to listen. Go ahead, I'm here.",
            "You have my undivided attention. Share what's on your heart."
        ]
        
        dispatcher.utter_message(text=random.choice(responses))
        return []


class ActionValidateFeelings(Action):
    """
    Validates user's feelings to help them feel understood.
    """
    
    def name(self) -> Text:
        return "action_validate_feelings"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        import random
        
        validations = [
            "Your feelings are completely valid. Whatever you're experiencing is real and matters.",
            "It's okay to feel the way you feel. There's no right or wrong way to experience emotions.",
            "Thank you for trusting me with your feelings. They deserve to be heard and acknowledged.",
            "What you're feeling makes complete sense given what you're going through.",
            "Your emotions are valid. It takes courage to acknowledge and share them."
        ]
        
        dispatcher.utter_message(text=random.choice(validations))
        return []


class ActionSessionSummary(Action):
    """
    Provides a supportive session summary before ending conversation.
    """
    
    def name(self) -> Text:
        return "action_session_summary"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_emotion = tracker.get_slot("current_emotion") or "your feelings"
        
        summary = f"""Thank you for sharing with me today. Here's what I want you to remember:

💙 **You matter.** Your feelings about {current_emotion} are valid.
💪 **You're not alone.** Reaching out takes courage, and you did that today.
🌱 **Small steps count.** Even talking about how you feel is progress.
🔄 **I'm always here.** Come back anytime you need support.

Take care of yourself. You deserve kindness — especially from yourself. 💙"""
        
        dispatcher.utter_message(text=summary)
        return []
