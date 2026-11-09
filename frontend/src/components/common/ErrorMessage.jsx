export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="rounded-xl border border-red-200 bg-red-50 p-5 flex items-start gap-3">
      <span className="text-red-500 text-xl flex-shrink-0">⚠️</span>
      <div className="flex-1">
        <p className="text-sm font-medium text-red-800">Something went wrong</p>
        <p className="text-sm text-red-600 mt-0.5">{message}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="mt-3 text-sm font-medium text-red-700 underline hover:no-underline"
          >
            Try again
          </button>
        )}
      </div>
    </div>
  );
}
