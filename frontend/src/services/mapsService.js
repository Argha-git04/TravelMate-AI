/** Maps service — geocoding via Nominatim/OpenStreetMap proxy. */
import api from "./api";

// TODO Phase 6: implement
export const geocode = (query) => api.get("/maps/geocode", { params: { q: query } });
