# EmpathicAI - Emotional Support AI Chatbot

**EmpathicAI** is a conversational agent built on the **Rasa** framework. Unlike traditional chatbots, this system integrates **Natural Language Processing (NLP)** and **Sentiment Analysis** to detect a user's emotional state in real-time, allowing it to provide compassionate, context-aware support.

---

## Key Features

* **Dynamic Sentiment Integration:** Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analysis to categorize user input (e.g., Sadness, Anxiety, Stress, Joy) and shift response tones accordingly.
* **Context-Aware Dialogue:** Leverages Rasa's machine learning-based dialogue management to maintain long-form, supportive conversations.
* **Empathetic Response Generation:** Custom actions generate contextually appropriate, empathetic responses based on detected emotions.
* **Coping Strategies:** Provides tailored coping techniques (breathing exercises, grounding techniques, journaling prompts) based on the user's emotional state.
* **Resource Sharing:** Offers professional mental health resources and crisis hotlines when needed.
* **Privacy-Focused:** Designed to provide a safe space for users to express feelings without judgment.

---

## Technologies & Tools

| Category | Technologies |
|----------|-------------|
| **Core Framework** | Rasa Open Source 3.x |
| **Language** | Python 3.8 - 3.10 |
| **NLP & ML** | SpaCy, NLTK, Scikit-learn |
| **Sentiment Analysis** | VADER (NLTK) |
| **Data Handling** | Pandas, NumPy |
| **Intent Classification** | DIET Classifier |
| **Dialogue Management** | TED Policy, Rule Policy |

---

## System Architecture

The chatbot follows a pipeline-based architecture to process text and manage state:

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                                │
└─────────────────────────┬───────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   NLU PIPELINE                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  Tokenizer   │→ │  Featurizers │→ │  DIET Classifier     │   │
│  └──────────────┘  └──────────────┘  │  (Intent + Entities) │   │
│                                       └──────────────────────┘   │
└─────────────────────────┬───────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                 DIALOGUE MANAGEMENT                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ Rule Policy  │  │ TED Policy   │  │ Memoization Policy   │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────┬───────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ACTION SERVER                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Sentiment Analysis (VADER)  →  Emotion Detection          │ │
│  │  Empathetic Response Generation                            │ │
│  │  Coping Strategy Recommendation                            │ │
│  │  Resource Provision                                        │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────┬───────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BOT RESPONSE                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Components:

1. **NLU (Natural Language Understanding):** Breaks down user phrases into intents and entities using the DIET classifier.
2. **Sentiment Analyzer:** VADER-based custom action that assigns sentiment scores and detects primary emotions (sadness, anxiety, stress, loneliness, anger, fear, joy).
3. **Dialogue Management:** Rasa Core decides the next best action based on the current sentiment score and conversation history.
4. **Action Server:** Executes custom Python actions to generate empathetic responses, provide coping strategies, and share resources.

---

## Project Structure

```
ai_chatbot/
├── actions/
│   ├── __init__.py
│   └── actions.py           # Custom actions with sentiment analysis
├── data/
│   ├── nlu.yml             # NLU training data (intents & examples)
│   ├── rules.yml           # Conversation rules
│   └── stories.yml         # Conversation stories
├── tests/
│   └── test_stories.yml    # Test conversation scenarios
├── config.yml              # Rasa pipeline configuration
├── credentials.yml         # Channel credentials
├── domain.yml              # Domain definition (intents, responses, slots)
├── endpoints.yml           # Endpoint configuration
└── requirements.txt        # Python dependencies
```

---

## Getting Started

### Prerequisites

* Python 3.8 - 3.10 (3.10 recommended)
* pip (Python package manager)
* Virtual environment tool (`venv` or `conda`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/preceelaChanu/Emotional-Support-AI-Chatbot.git
   cd Emotional-Support-AI-Chatbot/ai_chatbot
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate (Windows)
   .\venv\Scripts\activate
   
   # Activate (macOS/Linux)
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data:**
   ```python
   python -c "import nltk; nltk.download('vader_lexicon')"
   ```

5. **Train the model:**
   ```bash
   rasa train
   ```

---

## Usage

### Running the Chatbot

1. **Start the Action Server** (in one terminal):
   ```bash
   rasa run actions
   ```

2. **Start the Chatbot** (in another terminal):
   ```bash
   rasa shell
   ```

### Interactive Training

For interactive learning and model improvement:
```bash
rasa interactive
```

### Testing

Run test stories:
```bash
rasa test
```

---

## Supported Emotions & Intents

| Emotion | Intent | Example Phrases |
|---------|--------|-----------------|
| Sadness | `express_sadness` | "I feel so sad", "I'm depressed", "I feel empty" |
| Anxiety | `express_anxiety` | "I'm having a panic attack", "I can't stop worrying" |
| Stress | `express_stress` | "I'm overwhelmed", "Work is killing me" |
| Loneliness | `express_loneliness` | "I feel so alone", "I have no one to talk to" |
| Anger | `express_anger` | "I'm so frustrated", "I'm furious" |
| Fear | `express_fear` | "I'm scared", "I'm terrified about the future" |
| Joy | `express_joy` | "I'm so happy!", "Things are going great" |

---

## Example Conversation

```
User: Hi
Bot: Hello! I'm EmpathicAI, and I'm here to listen and support you. 
     How are you feeling today?

User: I've been feeling really anxious lately
Bot: I understand that anxiety can feel overwhelming. Let's take a moment 
     together. You're safe here. Would you like to talk more about this, 
     or is there something else on your mind?

User: How can I calm down?
Bot: Let's try some calming techniques together:

     🌬️ **Box Breathing**: Breathe in for 4 counts, hold for 4, 
        breathe out for 4, hold for 4. Repeat 4 times.
     
     👐 **5-4-3-2-1 Grounding**: Name 5 things you see, 4 you can touch, 
        3 you can hear, 2 you can smell, 1 you can taste.
     
     🧊 **Cold Water Technique**: Splash cold water on your face or hold 
        an ice cube. This activates your dive reflex and slows your heart rate.

User: Thank you, that helps
Bot: You're welcome. I'm always here if you need to talk.
```

---

## Customization

### Adding New Intents

1. Add training examples in `data/nlu.yml`
2. Add intent to `domain.yml`
3. Create stories in `data/stories.yml`
4. Retrain: `rasa train`

### Modifying Responses

Edit `domain.yml` to customize bot responses:
```yaml
responses:
  utter_greet:
    - text: "Your custom greeting here"
```

### Adding Custom Actions

Create new actions in `actions/actions.py`:
```python
class ActionCustom(Action):
    def name(self) -> Text:
        return "action_custom"
    
    def run(self, dispatcher, tracker, domain):
        # Your custom logic here
        dispatcher.utter_message(text="Custom response")
        return []
```

---

## Deployment

### REST API

Start the Rasa server:
```bash
rasa run --enable-api --cors "*"
```

### Docker (Optional)

```dockerfile
FROM rasa/rasa:3.6.0-full
WORKDIR /app
COPY . /app
RUN rasa train
CMD ["run", "--enable-api", "--cors", "*"]
```

---

## Important Disclaimer

⚠️ **This chatbot is designed for emotional support and is NOT a substitute for professional mental health treatment.**

If you or someone you know is in crisis, please contact:
- **National Suicide Prevention Lifeline (US):** 988 or 1-800-273-8255
- **Crisis Text Line:** Text HOME to 741741
- **International Association for Suicide Prevention:** https://www.iasp.info/resources/Crisis_Centres/

---

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Additional training data
- New coping strategies
- Bug fixes
- Documentation improvements

---

## License

This project is for educational and research purposes.

---

## Acknowledgments

- [Rasa Open Source](https://rasa.com/) - Conversational AI Framework
- [NLTK VADER](https://www.nltk.org/howto/sentiment.html) - Sentiment Analysis
- Mental health resources and hotlines for crisis support information

---

**Remember: You are not alone. Seeking help is a sign of strength. 💙**
