import { useEffect, useRef } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUserPen } from "@fortawesome/free-solid-svg-icons";

interface ProfileDropdownProps {
  open: boolean;
  setOpen: (open: boolean) => void;
  onEditUsername: () => void;
}

export default function ProfileDropdown({
  open,
  setOpen,
  onEditUsername,
}: ProfileDropdownProps) {
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }

    if (open) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open, setOpen]);

  if (!open) return null;



  return (
    <div
      ref={dropdownRef}
      className="absolute right-0 z-50 mt-3 overflow-hidden bg-white border border-slate-200 rounded-lg shadow-xl w-48 dark:bg-slate-800 dark:border-slate-700"
    >
      <button
        onClick={() => {
          onEditUsername();
          setOpen(false);
        }}
        className="flex items-center w-full gap-2 px-4 py-3 text-sm text-slate-700 transition cursor-pointer dark:text-slate-200 hover:bg-cyan-50 dark:hover:bg-slate-700"
      >
        <FontAwesomeIcon icon={faUserPen} className="w-4 h-4 text-cyan-600 dark:text-cyan-400" />
        <span>Edit username</span>
      </button>

    </div>
  );
}