import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import Button from "../components/common/Button";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import ErrorMessage from "../components/common/ErrorMessage";
import { generateItinerary } from "../services/aiService";

const INTEREST_OPTIONS = [
  "Culture & History", "Food & Cuisine", "Adventure & Outdoors",
  "Art & Museums", "Beach & Relaxation", "Nightlife",
  "Shopping", "Nature & Wildlife", "Architecture", "Photography",
];

const TRAVEL_STYLES = [
  { value: "budget", label: "Budget", desc: "Hostels, street food, public transport", emoji: "🎒" },
  { value: "mid-range", label: "Mid-Range", desc: "3-star hotels, local restaurants", emoji: "🏨" },
  { value: "luxury", label: "Luxury", desc: "5-star hotels, fine dining, private tours", emoji: "✨" },
];

export default function PlannerPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    destination: searchParams.get("destination") || "",
    days: 5,
    budget: 1500,
    travelStyle: "mid-range",
    startDate: "",
    interests: [],
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInterestToggle = (interest) => {
    setForm((prev) => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter((i) => i !== interest)
        : [...prev.interests, interest],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!form.destination.trim()) {
      setError("Please enter a destination.");
      return;
    }
    if (form.interests.length === 0) {
      setError("Please select at least one interest.");
      return;
    }

    setLoading(true);
    try {
      const response = await generateItinerary({
        destination: form.destination.trim(),
        days: form.days,
        budgetUsd: form.budget,
        interests: form.interests,
        travelStyle: form.travelStyle,
        startDate: form.startDate || null,
      });

      // Navigate to the itinerary page passing the AI response
      navigate("/itinerary/result", {
        state: {
          itinerary: response.data,
          form,
        },
      });
    } catch (err) {
      const status = err?.response?.status;
      const detail = err?.response?.data?.detail;

      if (status === 503) {
        setError(
          "The AI service is not available right now. IBM watsonx.ai credentials may not be configured on the server. Please try again later."
        );
      } else if (status === 422) {
        setError("Invalid request. Please check your inputs and try again.");
      } else if (status === 429) {
        setError("Too many requests. Please wait a moment and try again.");
      } else if (status === 504) {
        setError("The AI took too long to respond. Please try again — complex itineraries may need a few retries.");
      } else if (detail) {
        setError(detail);
      } else {
        setError("Something went wrong generating your itinerary. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-8">
        <Badge variant="ai" size="md">✨ IBM Granite AI</Badge>
        <h1 className="mt-3 text-3xl font-bold text-slate-900">Plan Your Trip</h1>
        <p className="mt-2 text-slate-500">
          Fill in your preferences and IBM Granite (<code className="bg-slate-100 px-1.5 py-0.5 rounded text-xs">ibm/granite-4-h-small</code>) will craft a personalized itinerary.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Destination */}
        <Card padding="lg">
          <label className="block text-sm font-semibold text-slate-800 mb-2">
            🌍 Destination <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={form.destination}
            onChange={(e) => setForm((p) => ({ ...p, destination: e.target.value }))}
            placeholder="e.g. Paris, France · Tokyo, Japan · Bali, Indonesia"
            className="w-full px-4 py-3 rounded-lg border border-slate-300 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            disabled={loading}
          />
        </Card>

        {/* Duration & Budget */}
        <Card padding="lg">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-slate-800 mb-2">
                📅 Duration (days)
              </label>
              <input
                type="number"
                min="1"
                max="30"
                value={form.days}
                onChange={(e) => setForm((p) => ({ ...p, days: Math.max(1, Math.min(30, Number(e.target.value))) }))}
                className="w-full px-4 py-3 rounded-lg border border-slate-300 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                disabled={loading}
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-800 mb-2">
                💰 Total Budget (USD)
              </label>
              <input
                type="number"
                min="100"
                step="100"
                value={form.budget}
                onChange={(e) => setForm((p) => ({ ...p, budget: Number(e.target.value) }))}
                className="w-full px-4 py-3 rounded-lg border border-slate-300 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                disabled={loading}
              />
            </div>
          </div>
          <div className="mt-4">
            <label className="block text-sm font-semibold text-slate-800 mb-2">
              🗓️ Start Date <span className="text-slate-400 font-normal">(optional)</span>
            </label>
            <input
              type="date"
              value={form.startDate}
              onChange={(e) => setForm((p) => ({ ...p, startDate: e.target.value }))}
              className="w-full sm:w-auto px-4 py-3 rounded-lg border border-slate-300 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              disabled={loading}
            />
          </div>
        </Card>

        {/* Travel Style */}
        <Card padding="lg">
          <label className="block text-sm font-semibold text-slate-800 mb-3">
            🏨 Travel Style
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {TRAVEL_STYLES.map(({ value, label, desc, emoji }) => (
              <button
                key={value}
                type="button"
                onClick={() => !loading && setForm((p) => ({ ...p, travelStyle: value }))}
                disabled={loading}
                className={`p-3 rounded-lg border-2 text-left transition-all disabled:opacity-50 ${
                  form.travelStyle === value
                    ? "border-blue-600 bg-blue-50"
                    : "border-slate-200 hover:border-slate-300"
                }`}
              >
                <div className="font-medium text-sm text-slate-900">{emoji} {label}</div>
                <div className="text-xs text-slate-500 mt-0.5">{desc}</div>
              </button>
            ))}
          </div>
        </Card>

        {/* Interests */}
        <Card padding="lg">
          <label className="block text-sm font-semibold text-slate-800 mb-3">
            ❤️ Interests <span className="text-red-500">*</span>
            <span className="text-slate-400 font-normal ml-2">Select all that apply</span>
          </label>
          <div className="flex flex-wrap gap-2">
            {INTEREST_OPTIONS.map((interest) => {
              const selected = form.interests.includes(interest);
              return (
                <button
                  key={interest}
                  type="button"
                  onClick={() => !loading && handleInterestToggle(interest)}
                  disabled={loading}
                  className={`px-3 py-1.5 rounded-full text-sm font-medium border transition-all disabled:opacity-50 ${
                    selected
                      ? "bg-blue-600 text-white border-blue-600"
                      : "bg-white text-slate-600 border-slate-300 hover:border-blue-400"
                  }`}
                >
                  {interest}
                </button>
              );
            })}
          </div>
          {form.interests.length > 0 && (
            <p className="text-xs text-slate-400 mt-2">{form.interests.length} selected</p>
          )}
        </Card>

        {/* Error */}
        {error && <ErrorMessage message={error} onRetry={() => setError(null)} />}

        {/* AI Notice */}
        <div className="flex items-start gap-3 p-4 rounded-lg bg-amber-50 border border-amber-200">
          <span className="text-amber-500 flex-shrink-0">💡</span>
          <p className="text-sm text-amber-800">
            <strong>Note:</strong> All prices in your itinerary are{" "}
            <strong>AI estimates</strong> generated by IBM Granite. They are clearly labeled
            and may not reflect current market rates. Always verify prices before booking.
          </p>
        </div>

        {/* Loading state info */}
        {loading && (
          <div className="flex items-center gap-3 p-4 rounded-lg bg-blue-50 border border-blue-200">
            <span className="animate-spin inline-block w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full flex-shrink-0" />
            <p className="text-sm text-blue-800">
              IBM Granite is crafting your personalized itinerary — this may take 15–30 seconds…
            </p>
          </div>
        )}

        {/* Submit */}
        <Button
          type="submit"
          size="lg"
          fullWidth
          disabled={loading}
        >
          {loading ? "Generating your itinerary…" : "✨ Generate AI Itinerary"}
        </Button>
      </form>
    </div>
  );
}
