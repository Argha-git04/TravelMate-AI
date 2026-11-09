# ✈️ TravelMate-AI

### AI-Powered Intelligent Travel Planning Assistant

TravelMate-AI is an AI-powered travel planning application designed to make trip planning easier, smarter and more personalized. It uses **IBM watsonx.ai and IBM Granite** to generate personalized travel itineraries based on user preferences, destination, travel duration, budget and interests.

The application helps users discover destinations, organize daily activities and estimate travel expenses through an interactive web interface.

---

## 🌟 Key Features

- **AI-Powered Itinerary Generation:** Generate personalized travel plans using IBM Granite.
- **Personalized Travel Planning:** Customize itineraries according to destination, duration, budget and interests.
- **Day-Wise Scheduling:** Organize travel activities into morning, afternoon and evening schedules.
- **Travel Recommendations:** Get AI-generated recommendations for attractions, food and transportation.
- **Budget Estimation:** Estimate accommodation, food, transportation and overall trip expenses.
- **Interactive User Interface:** Simple and responsive React-based interface.
- **Error Handling:** Loading indicators, API error messages and retry functionality.
- **AI Integration:** Real-time communication with IBM watsonx.ai through a FastAPI backend.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Frontend | React.js, Vite |
| Styling | Tailwind CSS |
| Backend | Python, FastAPI |
| AI Integration | IBM watsonx.ai |
| AI Model | IBM Granite 4 H Small |
| API Communication | Axios, REST API |
| Data Validation | Pydantic |
| Testing | Pytest |
| Package Management | npm, pip |
| Version Control | Git, GitHub |

---

## 🧠 AI Model Integration

TravelMate-AI integrates **IBM Granite 4 H Small (`ibm/granite-4-h-small`)** through IBM watsonx.ai.

The model processes user travel requirements and generates structured travel recommendations.

### AI Capabilities

1. Personalized itinerary generation.
2. Destination-specific travel recommendations.
3. Day-wise activity scheduling.
4. Estimated travel budget calculation.
5. Food and transportation suggestions.

All AI-generated prices are estimates and should be independently verified before booking.

---

## 📁 Project Structure

```text
TravelMate-AI/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── ai.py
│   │   │       ├── chat.py
│   │   │       ├── itinerary.py
│   │   │       ├── weather.py
│   │   │       └── maps.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   │
│   │   ├── models/
│   │   ├── prompts/
│   │   ├── services/
│   │   │   ├── granite_service.py
│   │   │   ├── cloudant_service.py
│   │   │   ├── weather_service.py
│   │   │   └── maps_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── store/
│   │   └── utils/
│   │
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── render.yaml
├── .gitignore
└── README.md
```

---

## ⚙️ Installation and Setup

### Prerequisites

Install the following:

- Python 3.12
- Node.js and npm
- Git
- IBM Cloud account
- IBM watsonx.ai API Key
- IBM watsonx.ai Project ID

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/TravelMate-AI.git

cd TravelMate-AI
```

### Step 2: Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file inside the backend directory.

```env
WATSONX_API_KEY=your_ibm_watsonx_api_key
WATSONX_PROJECT_ID=your_ibm_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

Use the appropriate IBM Cloud region URL for your project.

**Security:** Never upload your actual `.env` file or API credentials to GitHub.

### Step 4: Start the Backend

From the backend directory:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend URL:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

### Step 5: Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create a `.env` file inside the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Start the development server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## 🔌 API Endpoints

Base URL:

```text
http://localhost:8000/api/v1
```

| Method | Endpoint | Description |
|---|---|---|
| POST | `/ai/itinerary` | Generate AI travel itinerary |
| POST | `/ai/recommend` | Generate travel recommendations |
| POST | `/ai/budget` | Estimate travel expenses |

Health check:

```text
GET /health
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

## 🚀 How to Use TravelMate-AI

1. Start the backend and frontend servers.
2. Open `http://localhost:5173`.
3. Navigate to the Trip Planner.
4. Enter your destination.
5. Select travel duration and number of travellers.
6. Set your estimated travel budget.
7. Choose your preferred travel interests.
8. Click **Generate AI Itinerary**.
9. Wait for IBM Granite to process your request.
10. Explore your personalized itinerary and estimated expenses.

---

## 🧪 Testing

Run backend tests:

```bash
pytest -v
```

Run frontend production build:

```bash
npm run build
```

The backend also includes tests for AI integration, API behavior and error handling.

---

## 🔐 Security

- IBM credentials are stored in backend environment variables.
- API keys are not embedded in frontend source code.
- Environment files are excluded from version control.
- API requests are handled through the FastAPI backend.
- Sensitive credentials should never be committed to GitHub.

---

## 🎯 Project Objective

The primary objective of TravelMate-AI is to simplify travel planning through artificial intelligence.

By integrating IBM Granite with a modern web application, the project demonstrates how generative AI can transform user preferences into structured, personalized travel plans.

---

## 🔮 Future Enhancements

Potential future improvements include:

- IBM Cloudant integration for itinerary storage.
- Real-time weather information.
- Interactive maps and location-based recommendations.
- User authentication and profile management.
- Saved trips and itinerary history.
- Improved destination discovery.

These are planned enhancements, not claims that all these features are currently implemented.

---

## 👨‍💻 Developer

**Developed as an AI-powered travel planning project using IBM watsonx.ai and IBM Granite.**

GitHub: https://github.com/YOUR_USERNAME

---

## 📄 License

This project is intended for educational and demonstration purposes. Add an appropriate open-source license before distributing it under specific reuse terms.

---

**TravelMate-AI | Plan Smarter. Travel Better. ✈️**

### Before uploading to GitHub

Replace:

* `YOUR_USERNAME` with your GitHub username.

* The GitHub repository URL with your actual repository URL.

* Confirm the listed features against the current implementation.

One important point: Your README should describe what actually works. Don't claim Cloudant, weather or maps are implemented just because their service files exist.
