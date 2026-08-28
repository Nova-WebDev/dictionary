import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronDown, faSpinner } from "@fortawesome/free-solid-svg-icons";
import { useUpdateUserRole } from "../hooks/useUpdateUserRole";
import type { UserEntity } from "../api/user";

interface RoleSelectActionProps {
  row: UserEntity;
}

const ROLE_OPTIONS = [
  { value: 1, label: "Member", dotClass: "bg-slate-400 dark:bg-slate-500" },
  { value: 10, label: "Leader", dotClass: "bg-amber-500 dark:bg-amber-400" },
] as const;

function getRoleOption(role: number) {
  return ROLE_OPTIONS.find((opt) => opt.value === role) ?? null;
}

export function RoleSelectAction({ row }: RoleSelectActionProps) {
  const [open, setOpen] = useState(false);
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const buttonRef = useRef<HTMLButtonElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const mutation = useUpdateUserRole();

  useEffect(() => {
    function close(e: MouseEvent) {
      if (
        buttonRef.current &&
        !buttonRef.current.contains(e.target as Node) &&
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target as Node)
      ) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, []);

  const handleToggle = () => {
    if (!open && buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      setPosition({ top: rect.bottom + window.scrollY + 4, left: rect.left + window.scrollX });
    }
    setOpen((prev) => !prev);
  };

  const handleSelect = (value: number) => {
    setOpen(false);
    if (value === row.role) return;
    mutation.mutate({ publicId: row.public_id, newRole: value });
  };

  const currentOption = getRoleOption(row.role);

  return (
    <>
      <button
        ref={buttonRef}
        onClick={handleToggle}
        disabled={mutation.isPending}
        className="flex items-center gap-2 px-3 py-1.5 text-sm border rounded-lg cursor-pointer border-slate-300 bg-slate-50 text-slate-700 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-200 disabled:opacity-50"
      >
        {mutation.isPending ? (
          <FontAwesomeIcon icon={faSpinner} spin className="w-3.5 h-3.5" />
        ) : (
          <>
            <span
              className={`w-2 h-2 rounded-full shrink-0 ${
                currentOption?.dotClass ?? "bg-slate-300 dark:bg-slate-600"
              }`}
            />
            <span>{currentOption?.label ?? `Role ${row.role}`}</span>
          </>
        )}
        <FontAwesomeIcon
          icon={faChevronDown}
          className={`w-3 h-3 text-slate-400 transition-transform ${open ? "rotate-180" : ""}`}
        />
      </button>

      {open &&
        createPortal(
          <div
            ref={dropdownRef}
            style={{ position: "absolute", top: position.top, left: position.left }}
            className="z-50 w-32 overflow-hidden bg-white border rounded-lg shadow-xl border-slate-200 dark:bg-slate-800 dark:border-slate-700"
          >
            {ROLE_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                onClick={() => handleSelect(opt.value)}
                className={`w-full px-3 py-2 flex items-center gap-2 text-left text-sm ${
                  row.role === opt.value
                    ? "bg-cyan-50 dark:bg-slate-700 text-cyan-700 dark:text-cyan-300"
                    : "text-slate-700 dark:text-slate-200 hover:bg-cyan-50 dark:hover:bg-slate-700"
                }`}
              >
                <span className={`w-2 h-2 rounded-full shrink-0 ${opt.dotClass}`} />
                {opt.label}
              </button>
            ))}
          </div>,
          document.body
        )}
    </>
  );
}