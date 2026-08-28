import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createWord } from "../api/dictionary";

export function useCreateWord() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      persianWord,
      englishWord,
    }: {
      persianWord: string;
      englishWord: string;
    }) => createWord(persianWord, englishWord),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["words"] });
    },
  });
}