export default function Badge({ children, variant = "default", size = "sm" }) {
  const variants = {
    default:    "bg-slate-100 text-slate-600 ring-slate-200",
    estimated:  "bg-amber-50 text-amber-700 ring-amber-200",
    live:       "bg-emerald-50 text-emerald-700 ring-emerald-200",
    ai:         "bg-blue-50 text-blue-700 ring-blue-200",
    info:       "bg-sky-50 text-sky-700 ring-sky-200",
    success:    "bg-green-50 text-green-700 ring-green-200",
    warning:    "bg-orange-50 text-orange-700 ring-orange-200",
    error:      "bg-red-50 text-red-700 ring-red-200",
  };

  const sizes = {
    xs: "text-xs px-2 py-0.5",
    sm: "text-xs px-2.5 py-1",
    md: "text-sm px-3 py-1",
  };

  return (
    <span
      className={`
        inline-flex items-center font-medium rounded-full ring-1
        ${variants[variant]} ${sizes[size]}
      `}
    >
      {children}
    </span>
  );
}
