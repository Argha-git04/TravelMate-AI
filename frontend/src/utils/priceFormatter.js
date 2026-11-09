/**
 * priceFormatter.js
 *
 * All prices that come from IBM Granite are estimates.
 * The API response marks them with is_estimated: true.
 * This utility ensures every AI-generated price is clearly labeled
 * so users are never misled about the reliability of cost data.
 */

/**
 * Format a price value with an "(estimated)" label if it is AI-generated.
 *
 * @param {number} amount - The price amount in USD
 * @param {boolean} isEstimated - True if the price came from Granite AI
 * @param {string} currency - Currency code, default "USD"
 * @returns {string} e.g. "$1,200 (estimated)" or "$25"
 */
export function formatPrice(amount, isEstimated = true, currency = "USD") {
  const formatted = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(amount);

  return isEstimated ? `${formatted} (estimated)` : formatted;
}

/**
 * Format a price from an API PriceEstimate object.
 *
 * @param {{ amount_usd: number, is_estimated: boolean, currency?: string }} priceObj
 * @returns {string}
 */
export function formatPriceObject(priceObj) {
  return formatPrice(priceObj.amount_usd, priceObj.is_estimated, priceObj.currency ?? "USD");
}
