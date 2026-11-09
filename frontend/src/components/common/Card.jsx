export default function Card({ children, className = "", hover = false, padding = "md" }) {
  const paddings = {
    none: "",
    sm: "p-4",
    md: "p-5",
    lg: "p-6",
  };

  return (
    <div
      className={`
        bg-white rounded-xl border border-slate-200 shadow-card
        ${hover ? "hover:shadow-card-hover hover:-translate-y-0.5 transition-all duration-200 cursor-pointer" : ""}
        ${paddings[padding]}
        ${className}
      `}
    >
      {children}
    </div>
  );
}
