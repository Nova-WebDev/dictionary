import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { logout } from "../api/auth";
import { useAuthStore } from "../store/authStore";

export function useLogout() {
  const clearAuth = useAuthStore((state) => state.clearAuth);
  const navigate = useNavigate();

  return useMutation({
    mutationFn: ({ refresh_token }: { refresh_token: string }) => logout(refresh_token),
    onSuccess: () => {
      clearAuth();
      navigate("/auth/email");
    },
    onError: () => {
      clearAuth();
      navigate("/auth/email");
    },
  });
}