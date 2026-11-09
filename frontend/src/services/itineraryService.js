/** Itinerary service — CRUD operations backed by IBM Cloudant. */
import api from "./api";

// TODO Phase 5: implement these functions
export const listItineraries = () => api.get("/itineraries");
export const getItinerary = (id) => api.get(`/itineraries/${id}`);
export const saveItinerary = (itinerary) => api.post("/itineraries", itinerary);
export const deleteItinerary = (id) => api.delete(`/itineraries/${id}`);
