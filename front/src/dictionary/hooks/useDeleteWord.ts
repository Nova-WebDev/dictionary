import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deleteWord } from "../api/dictionary";

export function useDeleteWord() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (publicId: string) => deleteWord(publicId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["words"] });
    },
  });
}