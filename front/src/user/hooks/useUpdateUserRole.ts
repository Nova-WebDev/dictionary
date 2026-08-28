import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateUserRole } from "../api/user";

export function useUpdateUserRole() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ publicId, newRole }: { publicId: string; newRole: number }) =>
      updateUserRole(publicId, newRole),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
}