import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faAngleDoubleLeft,
  faChevronLeft,
  faChevronRight,
  faAngleDoubleRight,
} from "@fortawesome/free-solid-svg-icons";
import type { TablePaginationProps } from "./types";

export default function TablePagination({
  page,
  total,
  limit,
  onPageChange,
}: TablePaginationProps) {
  const totalPages = Math.max(1, Math.ceil(total / Math.max(1, limit)));

  const goFirst = () => onPageChange(1);
  const goPrev = () => onPageChange(Math.max(1, page - 1));
  const goNext = () => onPageChange(Math.min(totalPages, page + 1));
  const goLast = () => onPageChange(totalPages);

  const base =
    "inline-flex items-center justify-center rounded-lg transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-offset-1";
  const enabled =
    "bg-indigo-100 dark:bg-[#152036] hover:bg-indigo-200 dark:hover:bg-[#1a2742]";
  const disabled =
    "bg-indigo-100/60 dark:bg-[#152036]/60 cursor-not-allowed opacity-20";
  const txt = "text-gray-800 dark:text-gray-200";

  return (
    <nav className="flex items-center gap-2" aria-label="pagination">
      <div className="items-center hidden gap-2 sm:flex">
        <button
          onClick={goFirst}
          disabled={page === 1}
          aria-label="first"
          className={`${base} text-sm px-3 py-2 ${page === 1 ? disabled : enabled} ${txt}`}
        >
          <FontAwesomeIcon icon={faAngleDoubleRight} />
        </button>

        <button
          onClick={goPrev}
          disabled={page === 1}
          aria-label="prev"
          className={`${base} px-3 text-sm py-2 ${page === 1 ? disabled : enabled} ${txt}`}
        >
          <FontAwesomeIcon icon={faChevronRight} />
        </button>

        <div className="px-3 py-2 rounded-lg bg-indigo-50 dark:bg-[#0b1a2b] text-sm flex items-center gap-2">
          <span className="font-medium text-gray-800 dark:text-gray-200">{page}</span>
          <span className="text-gray-400">/</span>
          <span className="text-gray-500 dark:text-gray-300">{totalPages}</span>
        </div>

        <button
          onClick={goNext}
          disabled={page === totalPages}
          aria-label="next"
          className={`${base} px-3 text-sm py-2 ${page === totalPages ? disabled : enabled} ${txt}`}
        >
          <FontAwesomeIcon icon={faChevronLeft} />
        </button>

        <button
          onClick={goLast}
          disabled={page === totalPages}
          aria-label="last"
          className={`${base} px-3 text-sm py-2 ${page === totalPages ? disabled : enabled} ${txt}`}
        >
          <FontAwesomeIcon icon={faAngleDoubleLeft} />
        </button>
      </div>

      <div className="flex items-center gap-2 sm:hidden">
        <button
          onClick={goPrev}
          disabled={page === 1}
          aria-label="prev"
          className={`${base} px-3 py-2 ${page === 1 ? disabled : enabled} ${txt}`}
        >
          <FontAwesomeIcon icon={faChevronRight} />
        </button>

        <div className="px-3 py-2 rounded-lg bg-indigo-100 dark:bg-[#152036] text-sm text-center min-w-22">
          <span className="text-gray-600 dark:text-gray-300">
            {" "}
            {page} / {totalPages}{" "}
          </span>
        </div>

        <button
          onClick={goNext}
          disabled={page === totalPages}
          aria-label="next"
          className={`${base} px-3 py-2 ${page === totalPages ? disabled : enabled} ${txt}`}
        >
          <FontAwesomeIcon icon={faChevronLeft} />
        </button>
      </div>
    </nav>
  );
}
