# AI Emotional Support Chatbot

An AI-powered conversational chatbot built with **Rasa** and **Hugging Face Transformers** that provides emotional support and mental health assistance through natural, empathetic dialogue.

## 🌟 Features

- **Emotional Intelligence**: Uses sentiment analysis to understand user emotions and tailor responses accordingly
- **Natural Language Generation**: Leverages DistilGPT-2 for generating compassionate, context-aware responses
- **Mental Health Support**: Designed to provide emotional support for users experiencing sadness, anxiety, stress, or loneliness
- **Conversation Flow Management**: Implements multiple conversation paths based on user mood and intent
- **Intent Recognition**: Recognizes various user intents including greetings, farewells, mood expressions, and support-seeking

## 🏗️ Project Structure

```
ai_chatbot/
├── actions/
│   ├── __init__.py
│   └── actions.py              # Custom Rasa actions with AI response generation
├── data/
│   ├── nlu.yml                # NLU training data with user intents and examples
│   ├── rules.yml              # Conversation rules
│   └── stories.yml            # Conversation flow stories
├── models/                     # Trained Rasa models
├── tests/
│   └── test_stories.yml       # Test conversation scenarios
├── config.yml                  # Rasa NLU and Core configuration
├── domain.yml                  # Domain file with intents, actions, and responses
├── endpoints.yml               # Endpoint configuration
├── credentials.yml             # Credentials for messaging channels
└── rasa_env/                   # Python virtual environment
```

## 🤖 How It Works

### 1. **Intent Classification**
The bot recognizes the following intents:
- `greet` - User greetings
- `goodbye` - Farewells
- `mood_great` - Positive mood expressions
- `mood_unhappy` - Negative mood expressions
- `express_feeling` - Sharing emotions (sadness, stress, anxiety)
- `seek_support` - Asking for help or support
- `bot_challenge` - Questioning if it's a bot
- `affirm` / `deny` - Confirmations/denials

### 2. **Sentiment Analysis**
The custom action (`action_generate_response`) analyzes user messages using a sentiment analysis model to determine emotional tone (positive, negative, or neutral).

### 3. **Response Generation**
Based on sentiment analysis, the bot:
1. Provides an immediate empathetic response
2. Uses DistilGPT-2 to generate a thoughtful, supportive continuation
3. Combines both for a warm, coherent response

### 4. **Conversation Flows**
The bot follows predefined stories:
- **Happy Path**: User greets → expresses good mood → bot celebrates
- **Sad Path 1**: User greets → expresses sadness → bot provides support → user affirms help → bot encourages
- **Sad Path 2**: User greets → expresses sadness → bot provides support → user denies help → bot says goodbye
- **Support Seeking**: User seeks support → bot generates AI response
- **Express Feeling**: User shares feelings → bot acknowledges → generates supportive response

## 🛠️ Technologies Used

- **[Rasa Open Source](https://rasa.com/)** - Conversational AI framework
- **[Hugging Face Transformers](https://huggingface.co/transformers/)** - NLP models
  - `distilgpt2` - Text generation
  - `sentiment-analysis` - Emotion detection
- **Python 3.10** - Programming language
- **Rasa SDK** - Custom action development

## 📋 Prerequisites

- Python 3.7 - 3.10
- pip
- Virtual environment (included as `rasa_env/`)

## 🚀 Installation & Setup

### 1. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\rasa_env\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.\rasa_env\Scripts\activate.bat
```

### 2. Verify Installation
```bash
rasa --version
```

### 3. Train the Model
Train the Rasa model with your training data:
```bash
rasa train
```

This will create a trained model in the `models/` directory.

## 🎯 Usage

### Running the Chatbot

#### 1. Start the Action Server
In one terminal, start the custom actions server:
```bash
rasa run actions
```

#### 2. Start the Rasa Server
In another terminal, start the Rasa server:
```bash
rasa shell
```

Or for an interactive conversation:
```bash
rasa interactive
```

### Example Conversation

```
User: Hi there
Bot: Hey! How are you?

User: I feel sad today
Bot: I hear you, and I'm here for you.
Bot: I'm really sorry you're feeling this way. You're not alone, and I'm here for you.
     It's completely normal to have days like this. Sometimes talking about it helps.
     What's been on your mind?

User: Can you help me feel better?
Bot: I'm really sorry you're feeling this way. You're not alone, and I'm here for you.
     Of course! I'm here to support you. Remember that difficult feelings are temporary,
     and reaching out like this shows strength. What would help you most right now?
```

## 🧪 Testing

Run test conversations:
```bash
rasa test
```

Run specific test stories:
```bash
rasa test core --stories tests/test_stories.yml
```

## 🔧 Configuration

### Modifying Responses
Edit `domain.yml` to customize bot responses:
```yaml
responses:
  utter_greet:
  - text: "Hello! How can I support you today?"
```

### Adding New Intents
1. Add training examples in `data/nlu.yml`
2. Add the intent to `domain.yml`
3. Create conversation flows in `data/stories.yml`
4. Retrain the model with `rasa train`

### Adjusting AI Response Generation
Modify parameters in `actions/actions.py`:
```python
response = self.generator(
    prompt,
    max_length=150,      # Response length
    temperature=0.6,     # Creativity (0.0-1.0)
    top_k=30,           # Word selection diversity
    top_p=0.85          # Nucleus sampling
)
```

## 🌐 Deployment Options

### Connect to Messaging Platforms
Configure `credentials.yml` for:
- Telegram
- Slack
- Facebook Messenger
- Custom REST channel

### Deploy to Cloud
Options include:
- Docker container
- Rasa X (for conversation management)
- Cloud platforms (AWS, GCP, Azure)

## ⚠️ Important Notes

- This chatbot is designed for **emotional support**, not professional mental health treatment
- Users in crisis should be directed to professional resources
- Consider adding crisis helpline information to responses
- Ensure compliance with data privacy regulations when deploying

## 🤝 Contributing

To add new features:
1. Add training data in `data/nlu.yml`
2. Define conversation flows in `data/stories.yml` or `data/rules.yml`
3. Create custom actions in `actions/actions.py` if needed
4. Train and test the model
5. Document changes

## 📝 License

This project is for educational and research purposes.

## 📞 Support Resources

If you're in crisis, please contact:
- **National Suicide Prevention Lifeline (US)**: 988 or 1-800-273-8255
- **Crisis Text Line**: Text HOME to 741741
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

---

**Note**: This is an AI assistant designed for emotional support conversations. For professional mental health support, please consult qualified healthcare providers.
