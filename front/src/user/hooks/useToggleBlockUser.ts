import { useMutation, useQueryClient } from "@tanstack/react-query";
import { blockOrUnblockUser } from "../api/user";
import type { GetUsersResponse } from "../api/user";

export function useToggleBlockUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ publicId, block }: { publicId: string; block: boolean }) =>
      blockOrUnblockUser(publicId, block),
    onSuccess: (response, variables) => {
      queryClient.setQueriesData<GetUsersResponse>(
        { queryKey: ["users"] },
        (old) => {
          if (!old) return old;
          return {
            ...old,
            users: old.users.map((u) =>
              u.public_id === variables.publicId
                ? { ...u, is_blocked: response.data.is_blocked }
                : u
            ),
          };
        }
      );
    },
  });
}