# ChaiBot - AI-Powered College Virtual Assistant

ChaiBot is a smart AI chatbot designed to assist students and faculty with college-related queries by offering real-time responses and context-aware conversations. Built using Rasa, the chatbot integrates a custom frontend with real-time data retrieval from structured JSON sources.

---

## 🌐 Front-End Technologies

### HTML/CSS

- Provides the layout and styling of the chatbot interface.
- Custom styles define avatars, background, fonts, etc.

### JavaScript

- Loads and initializes the Rasa WebChat client.
- Connects to the Rasa backend via WebSocket.
- Sends initial payload and language settings.

### Rasa WebChat

- Embedded web client for Rasa, enabling real-time chat.
- Connects to backend via `http://localhost:5005`.

---

## 🧠 Back-End Technologies

### Rasa

- Handles intent recognition, entity extraction, and dialogue management.
- Powers the main NLP functionalities.

### Rasa SDK

- Defines custom actions using Python.
- Integrates college data from `x.json` to answer queries.

### Python

- Used to write and execute custom logic via Rasa SDK.

### Flask

- Used to host an intermediary backend if needed.

---

## 💾 Data and Storage

### JSON

- Uses `x.json` to store and fetch department and academic details.

---

## 🔧 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/akhilalle/chaibot.git
cd chaibot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the Rasa Model

```bash
rasa train
```

### 5. Start Rasa Action Server

```bash
rasa run actions --debug
```

### 6. Start Rasa Server

```bash
rasa run -m models --enable-api --cors "*"
```

### 7. Serve the Frontend

- Open the `index.html` file in your browser.
- Make sure Rasa is running at `http://localhost:5005`.

---

## 📂 File Structure

```
chaibot/
├── actions/
│   └── actions.py
├── data/
│   ├── nlu.yml
│   └── rules.yml
├── domain.yml
├── config.yml
├── models/
├── academics.json
├── index.html
├── requirements.txt
└── README.md
```

---

## 🗣 Example Interaction

> **User**: Tell me about the Civil Engineering department.  
> **Bot**: The Civil Engineering department focuses on sustainable design and offers both UG and PG programs...
