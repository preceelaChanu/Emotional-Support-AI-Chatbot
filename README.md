# Emotionally support AI chatbot, EmpathicAI

**EmpathicAI** is a conversational agent built on the **Rasa** framework. Unlike traditional chatbots, this system integrates **Natural Language Processing (NLP)** and **Sentiment Analysis** to detect a user's emotional state in real-time, allowing it to provide compassionate, context-aware support.


## Key Features
* **Dynamic Sentiment Integration:** Uses a custom sentiment analysis pipeline to categorize user input (e.g., Sadness, Anxiety, Joy) and shift response tones accordingly.
* **Context-Aware Dialogue:** Leverages Rasa’s machine learning-based dialogue management to maintain long-form, supportive conversations.
* **Empathetic Dataset Training:** Trained on curated emotional support datasets to ensure responses are grounded in active listening techniques.
* **Privacy-Focused:** Designed to provide a safe space for users to express feelings without judgment.

---

## Technologies & Tools
* **Core Framework:** Rasa Open Source
* **Language:** Python 3.8+
* **NLP & ML:** Spacy, NLTK, Scikit-learn
* **Sentiment Analysis:** VADER / Transformer-based models (e.g., BERT)
* **Data Handling:** Pandas, NumPy

---

## System Architecture
The chatbot follows a pipeline-based architecture to process text and manage state:

1.  **NLU (Natural Language Understanding):** Breaks down user phrases into intents and entities.
2.  **Sentiment Analyzer:** A custom component in the Rasa pipeline that assigns an "emotion score" to every message.
3.  **Dialogue Management:** Rasa Core decides the next best action based on the current sentiment score and conversation history.
4.  **Action Server:** Executes custom Python code to fetch specific supportive resources or dynamic responses.

[Image of Rasa architecture diagram including NLU, Dialogue Management, and Custom Actions]

---

## Getting Started

### Prerequisites
* Python installed (3.8 - 3.10 recommended)
* Virtual environment tool (`venv` or `conda`)

### Installation
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/preceelaChanu/Emotional-Support-AI-Chatbot/tree/main/ai_chatbot](https://github.com/preceelaChanu/Emotional-Support-AI-Chatbot/tree/main/ai_chatbot)
    cd empathic-ai-chatbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Train the model:**
    ```bash
    rasa train
    ```

4.  **Run the chatbot:**
    ```bash
    rasa shell
    ```

---

## Dataset & Training
The model was trained on a combination of:
* **