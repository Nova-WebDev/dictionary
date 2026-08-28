import { useNavigate } from "react-router-dom";
import { useRef } from "react";

import { useVerifyCode } from "./useVerifyCode";
import { useTempEmailStore } from "../store/useTempEmailStore";
import { useAuthStore } from "../store/authStore";

export function useVerifyCodeForm(email: string | null) {
  const { mutate, isPending, error } = useVerifyCode();

  const clearTempEmail = useTempEmailStore((state) => state.clearTempEmail);
  const setTokens = useAuthStore((state) => state.setTokens);

  const navigate = useNavigate();
  const navigateRef = useRef(navigate);

  const submit = (code: string) => {
    if (!email) return;

    mutate(
      { email, code },
      {
        onSuccess: (response) => {
          setTokens(
            response.data.refresh_token,
            response.data.access_token_expires_at
          );
          clearTempEmail();
          navigateRef.current("/");
        },
      }
    );
  };

  return { submit, isPending, error };
}