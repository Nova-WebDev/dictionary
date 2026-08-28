import { useState } from "react";
import Modal from "../../base/Modal";
import { useCreateWord } from "../hooks/useCreateWord";

interface CreateWordModalProps {
  open: boolean;
  onClose: () => void;
}

export function CreateWordModal({ open, onClose }: CreateWordModalProps) {
  const [persianWord, setPersianWord] = useState("");
  const [englishWord, setEnglishWord] = useState("");
  const [error, setError] = useState("");

  const { mutate, isPending } = useCreateWord();

  const validate = () => {
    if (!persianWord.trim() || !englishWord.trim()) {
      setError("Both fields are required.");
      return false;
    }
    setError("");
    return true;
  };

  const handleSubmit = () => {
    if (!validate()) return;

    mutate(
      { persianWord: persianWord.trim(), englishWord: englishWord.trim() },
      {
        onSuccess: () => {
          setPersianWord("");
          setEnglishWord("");
          onClose();
        },
        onError: () => {
          setError("Failed to create word.");
        },
      }
    );
  };

  return (
    <Modal open={open} title="Add word" onClose={onClose}>
      <div className="p-4 space-y-4">
        <div>
          <label className="block mb-1 text-sm text-slate-600 dark:text-slate-300">
            Persian
          </label>
          <input
            type="text"
            value={persianWord}
            onChange={(e) => setPersianWord(e.target.value)}
            className="w-full px-3 py-2 text-slate-800 border border-slate-300 rounded-lg bg-slate-50 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
          />
        </div>

        <div>
          <label className="block mb-1 text-sm text-slate-600 dark:text-slate-300">
            English
          </label>
          <input
            type="text"
            value={englishWord}
            onChange={(e) => setEnglishWord(e.target.value)}
            className="w-full px-3 py-2 text-slate-800 border border-slate-300 rounded-lg bg-slate-50 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
          />
        </div>

        {error && (
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        )}
      </div>

      <div className="flex justify-end gap-3 p-4">
        <button
          onClick={onClose}
          className="px-4 py-2 text-sm font-medium rounded-lg cursor-pointer text-slate-700 bg-slate-100 hover:bg-slate-200 dark:bg-slate-700 dark:text-slate-200 dark:hover:bg-slate-600 transition"
        >
          Cancel
        </button>

        <button
          onClick={handleSubmit}
          disabled={isPending}
          className="px-4 py-2 text-sm font-medium text-white transition rounded-lg cursor-pointer bg-cyan-600 hover:bg-cyan-700 disabled:opacity-50"
        >
          {isPending ? "Creating..." : "Create"}
        </button>
      </div>
    </Modal>
  );
}