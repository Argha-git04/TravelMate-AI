/** Weather service — proxies to Open-Meteo via the backend. Returns live data. */
import api from "./api";

// TODO Phase 6: implement
export const getWeather = (city) => api.get("/weather", { params: { city } });
