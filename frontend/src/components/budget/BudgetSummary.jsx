/**
 * BudgetSummary — displays AI-estimated budget breakdown.
 * All prices are labeled "(estimated)" because they come from IBM Granite.
 * Phase 4/8: implement full breakdown.
 */
import Badge from "../common/Badge";
import { formatPrice } from "../../utils/priceFormatter";

export default function BudgetSummary({ budget }) {
  if (!budget) return null;
  return (
    <div className="border rounded p-4">
      <div className="flex items-center gap-2 mb-3">
        <h3 className="font-semibold">Budget Estimate</h3>
        <Badge variant="estimated">AI estimated</Badge>
      </div>
      {/* Phase 4: render breakdown rows using formatPrice(amount, true) */}
      <p className="text-gray-400 text-sm">Budget breakdown — Phase 4</p>
    </div>
  );
}
