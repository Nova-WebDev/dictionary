import { useMutation } from "@tanstack/react-query";
import { verifyCode } from "../api/auth";

export function useVerifyCode() {
  return useMutation({
    mutationFn: ({ email, code }: { email: string; code: string }) =>
      verifyCode(email, code),
  });
}