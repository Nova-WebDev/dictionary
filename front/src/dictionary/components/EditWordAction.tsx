import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPen } from "@fortawesome/free-solid-svg-icons";
import type { WordEntryWithAuthor } from "../api/dictionary";

interface EditWordActionProps {
  row: WordEntryWithAuthor;
  onEdit: (row: WordEntryWithAuthor) => void;
}

export function EditWordAction({ row, onEdit }: EditWordActionProps) {
  return (
    <button
      onClick={() => onEdit(row)}
      className="flex items-center justify-center w-full gap-2 py-2 pl-4 pr-6 text-sm text-white rounded-md cursor-pointer bg-blue-600 md:w-auto hover:bg-blue-700 md:mr-1"
    >
      <FontAwesomeIcon icon={faPen} />
      Edit
    </button>
  );
}