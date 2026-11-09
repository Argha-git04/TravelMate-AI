# ✈️ TravelMate-AI

### AI-Powered Intelligent Travel Planning Assistant

**TravelMate-AI** is an intelligent travel planning application powered by IBM Granite and IBM watsonx.ai. It helps users create personalized travel itineraries based on their destination, travel duration, budget, number of travellers and personal interests.

The application combines generative AI with a modern web interface to simplify travel planning, provide destination recommendations and estimate trip expenses.

---

## 🌟 Key Features

- 🤖 **AI-Powered Itinerary Generation:** Generate personalized travel itineraries using IBM Granite.
- 🌍 **Personalized Travel Planning:** Customize travel plans according to destination, budget, duration and interests.
- 📅 **Day-Wise Scheduling:** Organize activities into morning, afternoon and evening schedules.
- 🏛️ **Destination Recommendations:** Discover attractions and places worth visiting.
- 🍽️ **Food Recommendations:** Get destination-specific food and dining suggestions.
- 🚌 **Transportation Suggestions:** Receive travel and local transportation recommendations.
- 🏨 **Accommodation Estimates:** View estimated accommodation expenses.
- 💰 **Budget Estimation:** Calculate estimated food, accommodation and transportation expenses.
- ⚡ **Interactive Interface:** Simple and responsive React-based application.
- 🛡️ **Error Handling:** Loading indicators, API error messages and retry functionality.

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Frontend | React.js 18 |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| Backend | Python 3.12 |
| API Framework | FastAPI |
| AI Platform | IBM watsonx.ai |
| AI Model | IBM Granite 4 H Small |
| AI Model ID | `ibm/granite-4-h-small` |
| API Communication | Axios, REST API |
| Data Validation | Pydantic |
| Testing | Pytest |
| Version Control | Git and GitHub |

---

## 🧠 IBM Granite AI Integration

TravelMate-AI integrates IBM Granite through the IBM watsonx.ai platform.

**Model:** `ibm/granite-4-h-small`

The AI model processes user-provided travel requirements and generates structured travel recommendations.

### AI Capabilities

1. Personalized travel itinerary generation.
2. Destination-specific recommendations.
3. Day-wise activity scheduling.
4. Estimated travel budget calculation.
5. Food and transportation suggestions.
6. Accommodation cost estimation.

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

Make sure the following are installed:

- Python 3.12
- Node.js and npm
- Git
- IBM Cloud account
- IBM watsonx.ai API Key
- IBM watsonx.ai Project ID

### Step 1: Clone the Repository

```bash
git clone https://github.com/Argha-git04/TravelMate-AI.git

cd TravelMate-AI
```

### Step 2: Backend Setup

Navigate to the backend directory:

```powershell
cd backend
```

Activate your existing Conda environment:

```powershell
conda activate travelmate
```

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

### Step 3: Configure IBM watsonx.ai

Create a `.env` file inside the backend directory.

```env
WATSONX_API_KEY=your_ibm_api_key
WATSONX_PROJECT_ID=your_ibm_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

Replace the placeholder values with your actual IBM watsonx.ai credentials.

Use the correct regional URL for your IBM Cloud project.

**Security:** Never upload your actual `.env` file or API credentials to GitHub.

### Step 4: Start the Backend Server

From the backend directory:

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Backend URL:

`http://localhost:8000`

Health check:

`http://localhost:8000/health`

Interactive API documentation:

`http://localhost:8000/docs`

### Step 5: Frontend Setup

Open another terminal and navigate to the frontend directory:

```powershell
cd G:\TravelMate-AI\frontend
```

Install frontend dependencies:

```powershell
npm install
```

Create a `.env` file inside the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Start the frontend development server:

```powershell
npm run dev
```

Frontend URL:

`http://localhost:5173`

---

## 🔌 API Endpoints

Base URL:

`http://localhost:8000/api/v1`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/ai/itinerary` | Generate personalized AI travel itineraries |
| POST | `/ai/recommend` | Generate destination and travel recommendations |
| POST | `/ai/budget` | Generate estimated travel expenses |

Additional endpoint:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check backend health |

Interactive API documentation:

`http://localhost:8000/docs`

---

## 🚀 How to Use TravelMate-AI

1. Start the FastAPI backend.
2. Start the React frontend.
3. Open `http://localhost:5173`.
4. Navigate to the Trip Planner.
5. Enter your travel destination.
6. Select the travel duration and number of travellers.
7. Set your estimated travel budget.
8. Choose your preferred travel interests.
9. Click **Generate AI Itinerary**.
10. Wait for IBM Granite to process your request.
11. Explore your personalized itinerary and estimated expenses.

### Example Demonstration

| Input | Example |
|---|---|
| Destination | Tokyo, Japan |
| Duration | 2 Days |
| Travellers | 2 |
| Budget | $1,500 |
| Travel Style | Mid-range |

The application generates a personalized itinerary with day-wise activities and estimated expenses.

---

## 🧪 Testing

### Backend Tests

Run the backend test suite:

```powershell
python -m pytest -v
```

### Frontend Production Build

Run:

```powershell
npm run build
```

The project includes tests for backend functionality, AI integration and API behavior.

---

## 🔐 Security

TravelMate-AI follows basic credential protection practices:

- IBM credentials are stored in backend environment variables.
- API keys are not embedded in frontend source code.
- Environment files are excluded from Git version control.
- `.env.example` contains placeholder values only.
- AI requests are processed through the FastAPI backend.

Never commit actual API keys, project credentials or other sensitive information to GitHub.

---

## 🎯 Project Objective

The primary objective of TravelMate-AI is to simplify travel planning using generative artificial intelligence.

By integrating IBM Granite with a modern full-stack web application, the project demonstrates how AI can transform user preferences into personalized travel plans, structured daily activities and estimated trip budgets.

---

## 🔮 Future Enhancements

Potential future improvements include:

- IBM Cloudant integration for itinerary storage.
- Real-time weather information.
- Interactive maps and location-based recommendations.
- User authentication and profile management.
- Saved trips and itinerary history.
- Enhanced destination discovery.

These are planned enhancements and are not claimed as completed functionality.

---

## 👨‍💻 Developer

**Arghadeep Saha**

GitHub: [Argha-git04](https://github.com/Argha-git04)

Project Repository: [TravelMate-AI](https://github.com/Argha-git04/TravelMate-AI)

---

## 📄 License

This project is developed for educational and demonstration purposes.

---

<div align="center">

**TravelMate-AI**

*Plan Smarter. Travel Better. ✈️*

**Powered by IBM Granite and watsonx.ai**

</div>