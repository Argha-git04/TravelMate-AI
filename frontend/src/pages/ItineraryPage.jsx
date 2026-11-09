import { useLocation, useParams, Link } from "react-router-dom";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import Button from "../components/common/Button";
import EmptyState from "../components/common/EmptyState";
import { formatPrice } from "../utils/priceFormatter";

// ── Sub-components ────────────────────────────────────────────────────────

function EstimatedPrice({ amount, className = "" }) {
  if (!amount && amount !== 0) return null;
  return (
    <span className={`text-sm font-medium text-slate-700 ${className}`}>
      {formatPrice(amount, true)}
    </span>
  );
}

function ActivityItem({ activity }) {
  return (
    <div className="flex items-start gap-3 py-3 border-b border-slate-100 last:border-0">
      {activity.time && (
        <span className="text-xs font-mono bg-slate-100 text-slate-600 px-2 py-1 rounded flex-shrink-0 mt-0.5">
          {activity.time}
        </span>
      )}
      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-2">
          <p className="text-sm font-medium text-slate-900">{activity.name}</p>
          <EstimatedPrice amount={activity.estimated_cost_usd} />
        </div>
        {activity.description && (
          <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">{activity.description}</p>
        )}
        {activity.location_name && (
          <p className="text-xs text-slate-400 mt-1">📍 {activity.location_name}</p>
        )}
      </div>
    </div>
  );
}

function DayCard({ day }) {
  return (
    <Card padding="none" className="overflow-hidden">
      {/* Day header */}
      <div className="flex items-center justify-between px-5 py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
        <div>
          <span className="text-sm font-medium opacity-80">Day {day.day_number}</span>
          <h3 className="font-semibold text-lg leading-tight">{day.title || `Day ${day.day_number}`}</h3>
        </div>
        <div className="text-right">
          <p className="text-xs opacity-70">Estimated total</p>
          <p className="font-semibold">
            {day.day_estimated_total_usd > 0
              ? `$${day.day_estimated_total_usd.toLocaleString()}`
              : "—"}
          </p>
        </div>
      </div>

      <div className="p-5 space-y-5">
        {/* Activities */}
        {day.activities && day.activities.length > 0 && (
          <div>
            <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">Activities</h4>
            <div>
              {day.activities.map((act, i) => (
                <ActivityItem key={i} activity={act} />
              ))}
            </div>
          </div>
        )}

        {/* Accommodation + Transport row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {day.accommodation && (
            <div className="bg-slate-50 rounded-lg p-3">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1.5">🏨 Accommodation</p>
              <p className="text-sm font-medium text-slate-800">
                {day.accommodation.name || "Hotel"}
                {day.accommodation.type && (
                  <span className="text-xs text-slate-500 font-normal ml-1.5 capitalize">
                    ({day.accommodation.type})
                  </span>
                )}
              </p>
              <EstimatedPrice amount={day.accommodation.estimated_cost_usd} className="block mt-1" />
            </div>
          )}
          {day.transport && (
            <div className="bg-slate-50 rounded-lg p-3">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1.5">🚌 Transport</p>
              <p className="text-sm font-medium text-slate-800 capitalize">
                {day.transport.type || "Local transport"}
              </p>
              {day.transport.description && (
                <p className="text-xs text-slate-500 mt-0.5">{day.transport.description}</p>
              )}
              <EstimatedPrice amount={day.transport.estimated_cost_usd} className="block mt-1" />
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}

// ── Main page ──────────────────────────────────────────────────────────────

export default function ItineraryPage() {
  const { id } = useParams();
  const location = useLocation();
  const itinerary = location.state?.itinerary;
  const form = location.state?.form;

  // Empty state — no data passed (direct URL navigation)
  if (!itinerary) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <EmptyState
          icon="🗺️"
          title="No itinerary found"
          description="Please use the planner to generate a new AI itinerary."
          action={
            <Link to="/planner">
              <Button>Go to Planner</Button>
            </Link>
          }
        />
      </div>
    );
  }

  const totalCost = itinerary.total_estimated_cost_usd || 0;
  const days = itinerary.days || [];

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">

      {/* ── Header ── */}
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-8">
        <div>
          <div className="flex flex-wrap items-center gap-2 mb-3">
            <Badge variant="ai">✨ IBM Granite</Badge>
            <Badge variant="estimated">All prices estimated</Badge>
            {itinerary.travel_style && (
              <Badge variant="info">{itinerary.travel_style}</Badge>
            )}
          </div>
          <h1 className="text-3xl font-bold text-slate-900">
            {itinerary.destination}
          </h1>
          <p className="text-slate-500 mt-1">
            {itinerary.duration_days} day{itinerary.duration_days !== 1 ? "s" : ""}
            {form?.startDate ? ` · Starting ${form.startDate}` : ""}
          </p>
          <p className="text-xs text-slate-400 mt-1">
            Generated by <span className="font-medium">{itinerary.granite_model || "ibm/granite-4-h-small"}</span>
          </p>
        </div>

        <div className="flex gap-2 flex-shrink-0">
          <Link to="/planner">
            <Button variant="secondary" size="sm">← Edit Plan</Button>
          </Link>
          <Button variant="primary" size="sm" disabled title="Phase 5: Save to Cloudant">
            💾 Save
          </Button>
        </div>
      </div>

      {/* ── Budget summary ── */}
      {totalCost > 0 && (
        <Card padding="md" className="mb-8 bg-gradient-to-r from-blue-50 to-sky-50 border-blue-200">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <p className="text-xs font-semibold text-blue-500 uppercase tracking-wide">Estimated Total Budget</p>
              <p className="text-3xl font-bold text-slate-900 mt-1">
                ${totalCost.toLocaleString()}
                <span className="text-base font-normal text-slate-500 ml-2">USD</span>
              </p>
              <Badge variant="estimated" size="xs" className="mt-1">AI estimate — not a guaranteed price</Badge>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-center">
              <div className="bg-white rounded-lg px-3 py-2 border border-blue-100">
                <p className="text-xs text-slate-400">Days</p>
                <p className="font-semibold text-slate-900">{itinerary.duration_days}</p>
              </div>
              <div className="bg-white rounded-lg px-3 py-2 border border-blue-100">
                <p className="text-xs text-slate-400">Per day</p>
                <p className="font-semibold text-slate-900">
                  ${Math.round(totalCost / itinerary.duration_days).toLocaleString()}
                </p>
              </div>
              <div className="bg-white rounded-lg px-3 py-2 border border-blue-100">
                <p className="text-xs text-slate-400">Style</p>
                <p className="font-semibold text-slate-900 capitalize">{itinerary.travel_style || "—"}</p>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* ── Interests ── */}
      {form?.interests && form.interests.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-8">
          <span className="text-xs text-slate-400 self-center mr-1">Interests:</span>
          {form.interests.map((i) => (
            <Badge key={i} variant="default" size="xs">{i}</Badge>
          ))}
        </div>
      )}

      {/* ── Day-by-day itinerary ── */}
      {days.length > 0 ? (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-slate-900">Day-by-Day Itinerary</h2>
          {days.map((day) => (
            <DayCard key={day.day_number} day={day} />
          ))}
        </div>
      ) : (
        <Card padding="lg" className="text-center py-12">
          <div className="text-4xl mb-4">🤖</div>
          <p className="text-slate-500">
            The AI returned an itinerary without day details. Try regenerating.
          </p>
          <Link to="/planner" className="mt-4 inline-block">
            <Button variant="secondary" size="sm">Try Again</Button>
          </Link>
        </Card>
      )}

      {/* ── Disclaimer ── */}
      <div className="mt-10 p-4 rounded-lg bg-amber-50 border border-amber-200">
        <p className="text-xs text-amber-800">
          <strong>⚠️ Important disclaimer:</strong> All prices, hotel names, and cost estimates
          above are generated by IBM Granite AI (<em>ibm/granite-4-h-small</em>) and are for
          planning purposes only. They are <strong>not verified live prices</strong> and may not
          reflect actual availability or current market rates. Always verify independently before booking.
        </p>
      </div>
    </div>
  );
}
