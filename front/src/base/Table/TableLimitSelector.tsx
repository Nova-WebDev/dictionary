import { useState, useRef, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronDown } from "@fortawesome/free-solid-svg-icons";
import type { TableLimitSelectorProps } from "./types";

const options = [20, 30, 50] as const;

export default function TableLimitSelector({ limit, onChange }: TableLimitSelectorProps) {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function close(e: MouseEvent | TouchEvent) {
      if (!rootRef.current) return;
      if (!rootRef.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", close);
    document.addEventListener("touchstart", close);
    return () => {
      document.removeEventListener("mousedown", close);
      document.removeEventListener("touchstart", close);
    };
  }, []);

  return (
    <div className="relative ml-2 md:ml-3" ref={rootRef}>
      <button
        onClick={() => setOpen(!open)}
        className="
          px-3 py-2 rounded-md flex items-center gap-2 text-sm
          bg-slate-100 dark:bg-[#093752]
          text-slate-800 dark:text-slate-200
          border border-slate-200 dark:border-slate-700/40
        "
      >
        <span>{limit}</span>

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
        <div
          className="
            absolute right-0 bottom-full mb-2 w-40 rounded-md shadow-xl z-50 overflow-hidden
            bg-slate-100 dark:bg-[#093752]
            border border-slate-200 dark:border-slate-700
          "
        >
          {options.map((opt) => (
            <button
              key={opt}
              onClick={() => {
                onChange(opt);
                setOpen(false);
              }}
              className={`
                w-full px-3 py-2 text-left text-sm flex items-center justify-between
                ${
                  limit === opt
                    ? "bg-slate-200 dark:bg-slate-800 text-slate-800 dark:text-slate-200"
                    : "text-slate-600 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-[#062940]"
                }
              `}
            >
              <span>{opt}</span>

              {limit === opt && (
                <span className="inline-block w-2 h-2 rounded-full bg-cyan-600 dark:bg-cyan-400" />
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}