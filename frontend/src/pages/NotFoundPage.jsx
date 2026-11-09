import { Link } from "react-router-dom";
import Button from "../components/common/Button";

export default function NotFoundPage() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center px-4 text-center">
      <div className="text-7xl mb-6">✈️</div>
      <h1 className="text-6xl font-bold text-slate-900 mb-3">404</h1>
      <h2 className="text-xl font-semibold text-slate-700 mb-2">Page Not Found</h2>
      <p className="text-slate-500 max-w-sm mb-8">
        Looks like this destination doesn't exist on our map. Let's get you back on course.
      </p>
      <div className="flex gap-3">
        <Link to="/">
          <Button>🏠 Go Home</Button>
        </Link>
        <Link to="/planner">
          <Button variant="secondary">Plan a Trip</Button>
        </Link>
      </div>
    </div>
  );
}
