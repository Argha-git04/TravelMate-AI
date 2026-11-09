/**
 * AI service — calls IBM Granite endpoints on the FastAPI backend.
 *
 * IBM credentials are NEVER in this file.
 * The frontend only calls its own backend (VITE_API_BASE_URL).
 * The backend holds all IBM secrets.
 */
import api from "./api";

/**
 * Generate a full travel itinerary using IBM Granite.
 * @param {Object} params
 * @param {string} params.destination
 * @param {number} params.days
 * @param {number} params.budgetUsd
 * @param {string[]} params.interests
 * @param {string} params.travelStyle
 * @param {string|null} params.startDate
 * @returns {Promise<Object>} ItineraryResponse with is_estimated=true on all costs
 */
export const generateItinerary = ({ destination, days, budgetUsd, interests, travelStyle, startDate }) =>
  api.post("/ai/itinerary", {
    destination,
    days,
    budget_usd: budgetUsd,
    interests,
    travel_style: travelStyle,
    start_date: startDate || null,
  });

/**
 * Get AI destination recommendations.
 * @param {Object} params
 * @param {string[]} params.interests
 * @param {number} params.budgetUsd
 * @param {number} params.days
 * @returns {Promise<Object>} RecommendResponse
 */
export const getRecommendations = ({ interests, budgetUsd, days }) =>
  api.post("/ai/recommend", {
    interests,
    budget_usd: budgetUsd,
    days,
  });

/**
 * Estimate trip budget using IBM Granite.
 * @param {Object} params
 * @param {string} params.destination
 * @param {number} params.days
 * @param {string} params.travelStyle
 * @returns {Promise<Object>} BudgetResponse with is_estimated=true
 */
export const estimateBudget = ({ destination, days, travelStyle }) =>
  api.post("/ai/budget", {
    destination,
    days,
    travel_style: travelStyle,
  });
