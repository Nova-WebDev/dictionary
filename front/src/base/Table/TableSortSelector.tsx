import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faSort,
  faSortUp,
  faSortDown,
  faChevronDown,
} from "@fortawesome/free-solid-svg-icons";
import type { IconDefinition } from "@fortawesome/fontawesome-svg-core";
import type { TableColumn, TableSortSelectorProps } from "./types";

export default function TableSortSelector<T>({
  columns,
  orderBy,
  deorder,
  onSort,
}: TableSortSelectorProps<T>) {
  const [open, setOpen] = useState(false);

  const getIcon = (col: TableColumn<T>): IconDefinition => {
    if (!col.orderBy) return faSort;
    if (orderBy !== col.orderBy) return faSort;
    if (deorder === false) return faSortUp;
    return faSortDown;
  };

  const isActive = (col: TableColumn<T>) => orderBy === col.orderBy;

  return (
    <div className="relative mr-2 md:ml-3 md:hidden">
      <button
        onClick={() => setOpen(!open)}
        className="px-3 py-2 bg-white dark:bg-[#093752] rounded-md flex items-center gap-2 text-sm text-slate-800 dark:text-slate-100 border border-slate-200 dark:border-slate-700/40"
      >
        <span>Sort</span>
        <span className="inline-flex items-center justify-center w-5 h-5 ml-auto rounded-full">
          <FontAwesomeIcon
            icon={faChevronDown}
            className={`text-[11px] transition-transform ${
              open ? "rotate-180" : "rotate-0"
            } text-slate-500 dark:text-slate-400`}
          />
        </span>
      </button>

      {open && (
        <div className="absolute left-0 mt-2 w-52 bg-white dark:bg-[#062940] border border-slate-200 dark:border-slate-700 rounded-xl shadow-xl z-50 overflow-hidden">
          {columns
            .filter((c) => c.orderBy)
            .map((col, i) => (
              <button
                key={i}
                onClick={() => {
                  if (col.orderBy) onSort(col.orderBy);
                  setOpen(false);
                }}
                className={`w-full px-3 py-2 text-left flex items-center justify-between text-sm ${
                  isActive(col)
                    ? "bg-cyan-50 dark:bg-[#093752] text-cyan-700 dark:text-cyan-300"
                    : "text-slate-700 dark:text-slate-200 hover:bg-cyan-50 dark:hover:bg-[#093752]"
                }`}
              >
                <span>{col.label}</span>
                <FontAwesomeIcon icon={getIcon(col)} />
              </button>
            ))}
        </div>
      )}
    </div>
  );
}