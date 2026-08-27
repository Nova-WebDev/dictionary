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
        className="px-3 py-2 bg-white dark:bg-[#182238] rounded-md flex items-center gap-2 text-sm text-gray-800 dark:text-gray-100 border border-indigo-200 dark:border-gray-700/40"
      >
        <span>Sort</span>
        <span className="inline-flex items-center justify-center w-5 h-5 ml-auto rounded-full">
          <FontAwesomeIcon
            icon={faChevronDown}
            className={`text-[11px] transition-transform ${
              open ? "rotate-180" : "rotate-0"
            } text-gray-500 dark:text-gray-400`}
          />
        </span>
      </button>

      {open && (
        <div className="absolute left-0 mt-2 w-52 bg-white dark:bg-[#0f1724] border border-indigo-200 dark:border-gray-700 rounded-xl shadow-xl z-50 overflow-hidden">
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
                    ? "bg-indigo-50 dark:bg-[#111a2b] text-indigo-700 dark:text-indigo-300"
                    : "text-gray-700 dark:text-gray-200 hover:bg-indigo-50 dark:hover:bg-[#111a2b]"
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
