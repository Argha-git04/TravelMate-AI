/** Zustand store for itinerary state. Phase 4/5: expand with full state. */
import { create } from "zustand";

const useItineraryStore = create((set) => ({
  currentItinerary: null,
  savedItineraries: [],
  isLoading: false,
  error: null,

  setCurrentItinerary: (itinerary) => set({ currentItinerary: itinerary }),
  setSavedItineraries: (list) => set({ savedItineraries: list }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}));

export default useItineraryStore;
