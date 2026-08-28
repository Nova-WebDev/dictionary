import { useEffect, useState } from "react";
import Modal from "../../base/Modal";
import { useUpdateMyUsername } from "../hooks/useUpdateMyUsername";
import { useUserStore } from "../store/userStore";

interface EditUsernameModalProps {
  open: boolean;
  onClose: () => void;
}

export default function EditUsernameModal({ open, onClose }: EditUsernameModalProps) {
  const currentUser = useUserStore((state) => state.currentUser);
  const [username, setUsername] = useState("");

  const { mutate, isPending, isError, reset } = useUpdateMyUsername();

  useEffect(() => {
    if (open) {
      setUsername(currentUser?.username ?? "");
      reset();
    }
  }, [open, currentUser?.username, reset]);

  const trimmed = username.trim();
  const isUnchanged = trimmed === (currentUser?.username ?? "");
  const isDisabled = isPending || !trimmed || isUnchanged;

  const handleSave = () => {
    if (!trimmed) return;

    mutate(trimmed, {
      onSuccess: () => onClose(),
    });
  };

  return (
    <Modal open={open} title="Edit Username" onClose={onClose}>
      <div className="p-4 space-y-3">
        <label className="text-sm text-slate-600 dark:text-slate-300">
          Username
        </label>

        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full px-3 py-2 text-slate-800 border border-slate-300 rounded-lg bg-slate-50 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500"
        />

        {isError && (
          <p className="text-sm text-red-600 dark:text-red-400">
            Failed to save. Try again.
          </p>
        )}
      </div>

      <div className="flex gap-3 p-4 ">
        <button
          onClick={onClose}
          className="px-4 py-2 text-sm font-medium rounded-lg cursor-pointer text-slate-700 bg-slate-100 hover:bg-slate-200 dark:bg-slate-700 dark:text-slate-200 dark:hover:bg-slate-600 transition"
        >
          Cancel
        </button>

        <button
          onClick={handleSave}
          disabled={isDisabled}
          className="px-4 py-2 text-sm font-medium text-white transition rounded-lg cursor-pointer bg-cyan-600 hover:bg-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isPending ? "Saving..." : "Save"}
        </button>
      </div>
    </Modal>
  );
}