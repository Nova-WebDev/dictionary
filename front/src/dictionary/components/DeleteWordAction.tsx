import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash, faSpinner } from "@fortawesome/free-solid-svg-icons";
import { useDeleteWord } from "../hooks/useDeleteWord";
import type { WordEntryWithAuthor } from "../api/dictionary";

interface DeleteWordActionProps {
  row: WordEntryWithAuthor;
}

export function DeleteWordAction({ row }: DeleteWordActionProps) {
  const mutation = useDeleteWord();
  const isLoading = mutation.isPending;

  const handleClick = () => {
    mutation.mutate(row.public_id);
  };

  return (
    <button
      disabled={isLoading}
      onClick={handleClick}
      className={`
        flex items-center justify-center gap-2
        w-full md:w-auto
        pl-3 pr-4 py-2 rounded-lg text-sm font-medium
        transition-all duration-200 shadow-sm
        bg-red-600 hover:bg-red-700 text-white cursor-pointer
        ${isLoading ? "opacity-40 cursor-not-allowed" : ""}
      `}
    >
      {isLoading ? (
        <>
          <FontAwesomeIcon icon={faSpinner} spin />
          <span className="animate-pulse">Deleting...</span>
        </>
      ) : (
        <>
          <FontAwesomeIcon icon={faTrash} />
          <span>Delete</span>
        </>
      )}
    </button>
  );
}