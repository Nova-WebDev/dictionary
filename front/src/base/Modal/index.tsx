import { createPortal } from "react-dom";
import type { ReactNode } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTimes } from "@fortawesome/free-solid-svg-icons";

export interface ModalProps {
  open?: boolean;
  title: string;
  onClose: () => void;
  children: ReactNode;
}

export default function Modal({ open = false, title, onClose, children }: ModalProps) {
  if (!open) return null;

  return createPortal(
    <div className="fixed inset-0 z-50 flex items-center justify-center px-3 bg-black/40 dark:bg-black/50 backdrop-blur-sm">
      <div className="w-full max-w-md rounded-lg shadow-xl bg-[#F4F4F5] dark:bg-[#0D1525] border border-gray-300 dark:border-gray-700">
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
            {title}
          </h2>

          <button
            onClick={onClose}
            className="text-gray-500 cursor-pointer dark:text-gray-300 hover:text-red-600 dark:hover:text-red-500"
          >
            <FontAwesomeIcon icon={faTimes} className="w-5 h-5" />
          </button>
        </div>

        {children}
      </div>
    </div>,
    document.body,
  );
}
