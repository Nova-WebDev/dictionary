import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRightLeft, faSpinner } from "@fortawesome/free-solid-svg-icons";
import { useWordSearch } from "../hooks/useWordSearch";

export const HomePage = () => {
  const {
    direction,
    query,
    setQuery,
    toggleDirection,
    results,
    isFetching,
    isError,
    hasQuery,
  } = useWordSearch();

  const sourceLabel = direction === "en-to-fa" ? "English" : "Persian";
  const targetLabel = direction === "en-to-fa" ? "Persian" : "English";

  return (
    <div className="max-w-3xl px-4 py-10 mx-auto mt-8">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex-1 px-4 py-3 text-sm font-medium text-center rounded-lg bg-cyan-50 text-cyan-700 dark:bg-slate-800 border border-cyan-200 dark:border-cyan-900  dark:text-slate-300">
          {sourceLabel}
        </div>

        <button
          onClick={toggleDirection}
          className="flex items-center justify-center w-10 h-10 text-cyan-600 transition rounded-full cursor-pointer bg-cyan-50 hover:bg-cyan-100 border dark:border-cyan-900 border-cyan-200 dark:bg-slate-800 dark:text-cyan-400 dark:hover:bg-slate-700 shrink-0"
        >
          <FontAwesomeIcon icon={faRightLeft} className="w-4 h-4" />
        </button>

        <div className="flex-1 px-4 py-3 text-sm font-medium text-center rounded-lg bg-cyan-50 text-cyan-700 dark:bg-slate-800 border border-cyan-200 dark:border-cyan-900 dark:text-slate-300">
          {targetLabel}
        </div>
      </div>

      <div className="relative mb-8 mt-8">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={`Type a word in ${sourceLabel}...`}
          className="w-full px-4 py-3 text-lg border rounded-xl border-slate-300 bg-white dark:bg-slate-800 dark:border-slate-700 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
        />

        {isFetching && (
          <FontAwesomeIcon
            icon={faSpinner}
            className="absolute w-5 h-5 -translate-y-1/2 text-cyan-500 animate-spin right-4 top-1/2"
          />
        )}
      </div>

      {isError && (
        <p className="text-sm text-center text-red-600 dark:text-red-400">
          Something went wrong. Try again.
        </p>
      )}

      {!isFetching && hasQuery && results.length === 0 && !isError && (
        <p className="text-sm text-center text-slate-500 dark:text-slate-400">
          No results found.
        </p>
      )}

      {results.length > 0 && (
        <div className="overflow-hidden border rounded-xl border-slate-300 dark:border-slate-700">
          {results.map((word, index) => (
            <div
              key={word.public_id}
              className={`flex items-center justify-between px-5 py-4 bg-white dark:bg-slate-800 ${
                index !== 0 ? "border-t border-slate-300 dark:border-slate-700" : ""
              }`}
            >
              <span className="text-lg font-medium text-slate-800 dark:text-slate-100">
                {direction === "en-to-fa" ? word.english_word : word.persian_word}
              </span>
              <span className="text-lg text-cyan-700 dark:text-cyan-400">
                {direction === "en-to-fa" ? word.persian_word : word.english_word}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};