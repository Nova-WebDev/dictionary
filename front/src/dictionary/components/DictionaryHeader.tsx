import { useState } from "react";
import { CreateWordModal } from "./CreateWordModal";

export function DictionaryHeader() {
  const [openCreateModal, setOpenCreateModal] = useState(false);

  return (
    <div className="flex items-center justify-between w-full mx-4 my-6 mt-8 md:mt-10 md:my-2 md:mx-13">
      <button
        onClick={() => setOpenCreateModal(true)}
        className="px-6 py-2.5 text-sm font-medium text-white transition rounded-lg cursor-pointer bg-indigo-600 hover:bg-indigo-700 whitespace-nowrap"
      >
        Add word
      </button>

      {openCreateModal && (
        <CreateWordModal open={openCreateModal} onClose={() => setOpenCreateModal(false)} />
      )}
    </div>
  );
}