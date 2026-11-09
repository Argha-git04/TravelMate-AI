/** Weather widget — shows live Open-Meteo data. Phase 6: implement. */
import Badge from "../common/Badge";

export default function WeatherWidget({ weather }) {
  if (!weather) return null;
  return (
    <div className="border rounded p-3 flex items-center gap-2 text-gray-400">
      <Badge variant="live">Live weather</Badge>
      <span>Weather Widget — Phase 6</span>
    </div>
  );
}
