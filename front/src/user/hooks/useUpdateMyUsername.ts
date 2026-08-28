import { useMutation } from "@tanstack/react-query";
import { updateMyUsername } from "../api/user";
import { useUserStore } from "../store/userStore";

export function useUpdateMyUsername() {
  const setCurrentUser = useUserStore((state) => state.setCurrentUser);

  return useMutation({
    mutationFn: (username: string) => updateMyUsername(username),
    onSuccess: (response) => {
      setCurrentUser(response.data);
    },
  });
}