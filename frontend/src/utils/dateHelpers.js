/** Date helper utilities for itinerary display. */

/**
 * Format an ISO date string (e.g. "2026-06-01") to a readable form.
 * @param {string} isoDate
 * @returns {string} e.g. "June 1, 2026"
 */
export function formatDate(isoDate) {
  if (!isoDate) return "";
  return new Date(isoDate).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

/**
 * Add days to an ISO date string.
 * @param {string} isoDate  — start date, e.g. "2026-06-01"
 * @param {number} days     — number of days to add
 * @returns {string}        — resulting ISO date string
 */
export function addDays(isoDate, days) {
  const date = new Date(isoDate);
  date.setDate(date.getDate() + days);
  return date.toISOString().split("T")[0];
}
