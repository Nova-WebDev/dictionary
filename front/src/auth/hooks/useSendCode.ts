import { useMutation } from "@tanstack/react-query";
import { sendCode } from "../api/auth";

export function useSendCode() {
  return useMutation({
    mutationFn: ({ email }: { email: string }) => sendCode(email),
  });
}