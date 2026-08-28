import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBan, faUnlock, faSpinner } from "@fortawesome/free-solid-svg-icons";
import { useToggleBlockUser } from "../hooks/useToggleBlockUser";
import type { UserEntity } from "../api/user";

interface ToggleBlockActionProps {
  row: UserEntity;
}

export function ToggleBlockAction({ row }: ToggleBlockActionProps) {
  const mutation = useToggleBlockUser();
  const isLoading = mutation.isPending;

  const handleClick = () => {
    mutation.mutate({ publicId: row.public_id, block: !row.is_blocked });
  };

  return (
    <button
      disabled={isLoading}
      onClick={handleClick}
      className={`
        flex items-center justify-center gap-2
        w-full md:w-auto
        pl-5 pr-3 py-2 rounded-lg text-sm font-medium
        transition-all duration-200
        ${
          row.is_blocked
            ? "bg-emerald-600 hover:bg-emerald-700 text-white cursor-pointer"
            : "bg-orange-600 hover:bg-orange-700 text-white cursor-pointer"
        }
        ${isLoading ? "opacity-40 cursor-not-allowed" : ""}
      `}
    >
      {isLoading ? (
        <FontAwesomeIcon icon={faSpinner} spin />
      ) : (
        <>
          <FontAwesomeIcon icon={row.is_blocked ? faUnlock : faBan} />
          <span>{row.is_blocked ? "Unblock" : "Block"}</span>
        </>
      )}
    </button>
  );
}