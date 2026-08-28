import { useMutation, useQueryClient } from "@tanstack/react-query";
import { editWord } from "../api/dictionary";

export function useEditWord() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      publicId,
      persianWord,
      englishWord,
    }: {
      publicId: string;
      persianWord: string;
      englishWord: string;
    }) => editWord(publicId, persianWord, englishWord),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["words"] });
    },
  });
}