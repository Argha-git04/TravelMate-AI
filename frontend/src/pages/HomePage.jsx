import { Link } from "react-router-dom";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";

const destinations = [
  {
    name: "Paris, France",
    emoji: "🗼",
    tagline: "The City of Light",
    tags: ["Culture", "Food", "Art"],
    description: "Explore iconic landmarks, world-class cuisine, and timeless art in Europe's most romantic city.",
    gradient: "from-rose-500 to-pink-600",
  },
  {
    name: "Tokyo, Japan",
    emoji: "⛩️",
    tagline: "Where Tradition Meets Future",
    tags: ["Technology", "Food", "History"],
    description: "Experience ultra-modern skylines and ancient temples in one of the world's most fascinating cities.",
    gradient: "from-red-500 to-orange-500",
  },
  {
    name: "Bali, Indonesia",
    emoji: "🌴",
    tagline: "Island of the Gods",
    tags: ["Nature", "Wellness", "Beaches"],
    description: "Discover lush rice terraces, sacred temples, and pristine beaches in this tropical paradise.",
    gradient: "from-emerald-500 to-teal-600",
  },
  {
    name: "New York, USA",
    emoji: "🗽",
    tagline: "The City That Never Sleeps",
    tags: ["Urban", "Culture", "Nightlife"],
    description: "Experience iconic skylines, world-class museums, and the unstoppable energy of the Big Apple.",
    gradient: "from-blue-500 to-indigo-600",
  },
  {
    name: "Safari, Kenya",
    emoji: "🦁",
    tagline: "The Last Great Wilderness",
    tags: ["Adventure", "Wildlife", "Nature"],
    description: "Witness the awe-inspiring Great Migration and encounter Africa's magnificent wildlife up close.",
    gradient: "from-amber-500 to-yellow-600",
  },
  {
    name: "Santorini, Greece",
    emoji: "🏛️",
    tagline: "Jewel of the Aegean",
    tags: ["Beaches", "Romance", "History"],
    description: "Marvel at stunning caldera views, whitewashed villages, and breathtaking Aegean sunsets.",
    gradient: "from-sky-500 to-blue-600",
  },
];

const features = [
  {
    icon: "🤖",
    title: "AI-Powered Itineraries",
    description: "IBM Granite crafts personalized day-by-day travel plans tailored to your budget and interests.",
  },
  {
    icon: "💰",
    title: "Budget Estimation",
    description: "Get clear cost breakdowns for accommodation, food, transport, and activities — clearly labeled as estimates.",
  },
  {
    icon: "🌤️",
    title: "Live Weather Data",
    description: "Real-time weather forecasts from Open-Meteo so you can pack exactly right for your destination.",
  },
  {
    icon: "🗺️",
    title: "Interactive Maps",
    description: "Visualize your entire itinerary on an interactive map powered by OpenStreetMap and Leaflet.",
  },
  {
    icon: "💬",
    title: "Travel Assistant",
    description: "Chat with an AI travel expert anytime — ask about destinations, visa requirements, or local tips.",
  },
  {
    icon: "☁️",
    title: "Save & Access Anywhere",
    description: "Your itineraries are securely stored on IBM Cloudant, accessible from any device at any time.",
  },
];

export default function HomePage() {
  return (
    <div>
      {/* ── Hero ── */}
      <section className="relative bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 text-white overflow-hidden">
        {/* Background decoration */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-96 h-96 bg-blue-600 rounded-full opacity-10 blur-3xl" />
          <div className="absolute -bottom-20 -left-20 w-80 h-80 bg-sky-500 rounded-full opacity-10 blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <div className="max-w-3xl">
            <Badge variant="ai" size="md">
              ✨ Powered by IBM Granite on watsonx.ai
            </Badge>
            <h1 className="mt-6 text-4xl md:text-6xl font-bold leading-tight tracking-tight">
              Plan Your Perfect
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-sky-300">
                Dream Trip
              </span>
              with AI
            </h1>
            <p className="mt-6 text-lg md:text-xl text-slate-300 leading-relaxed max-w-2xl">
              TravelMate AI creates personalized, day-by-day travel itineraries in seconds.
              Just tell us where you want to go, your budget, and what you love — and IBM Granite does the rest.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row gap-4">
              <Link to="/planner">
                <Button size="lg" className="shadow-lg shadow-blue-900/30">
                  🗺️ Start Planning for Free
                </Button>
              </Link>
              <Link to="/chat">
                <Button variant="outline" size="lg" className="border-white/30 text-white hover:bg-white/10">
                  💬 Chat with AI Assistant
                </Button>
              </Link>
            </div>
            <p className="mt-6 text-sm text-slate-400">
              Free to use · No sign-up required · Powered by IBM Cloud
            </p>
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-14">
            <Badge variant="ai" size="md">Features</Badge>
            <h2 className="mt-4 text-3xl md:text-4xl font-bold text-slate-900">
              Everything you need to plan the perfect trip
            </h2>
            <p className="mt-4 text-slate-500 text-lg">
              From AI-generated itineraries to live weather — all in one place.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f) => (
              <Card key={f.title} padding="lg">
                <div className="text-3xl mb-4">{f.icon}</div>
                <h3 className="font-semibold text-slate-900 mb-2">{f.title}</h3>
                <p className="text-sm text-slate-500 leading-relaxed">{f.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* ── Popular Destinations ── */}
      <section className="py-20 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-14">
            <Badge variant="info" size="md">Popular Destinations</Badge>
            <h2 className="mt-4 text-3xl md:text-4xl font-bold text-slate-900">
              Where will you go next?
            </h2>
            <p className="mt-4 text-slate-500">
              Click any destination to start planning your AI-powered itinerary.
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {destinations.map((dest) => (
              <Link
                key={dest.name}
                to={`/planner?destination=${encodeURIComponent(dest.name)}`}
                className="group"
              >
                <Card hover padding="none" className="overflow-hidden">
                  {/* Color gradient header */}
                  <div className={`h-32 bg-gradient-to-br ${dest.gradient} flex items-center justify-center`}>
                    <span className="text-5xl">{dest.emoji}</span>
                  </div>
                  {/* Content */}
                  <div className="p-5">
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <div>
                        <h3 className="font-semibold text-slate-900 group-hover:text-blue-700 transition-colors">
                          {dest.name}
                        </h3>
                        <p className="text-xs text-slate-400 mt-0.5">{dest.tagline}</p>
                      </div>
                    </div>
                    <p className="text-sm text-slate-500 leading-relaxed mb-3">{dest.description}</p>
                    <div className="flex flex-wrap gap-1.5">
                      {dest.tags.map((tag) => (
                        <Badge key={tag} variant="default" size="xs">{tag}</Badge>
                      ))}
                    </div>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to plan your next adventure?
          </h2>
          <p className="text-blue-100 text-lg mb-10 max-w-2xl mx-auto">
            Let IBM Granite design a personalized itinerary in seconds. Free, fast, and tailored just for you.
          </p>
          <Link to="/planner">
            <Button size="lg" variant="secondary">
              🚀 Create My Itinerary Now
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}
