import api from "../../shared/lib/axios";

export interface SendCodeResponse {
  email: string;
  sent: boolean;
}

export interface RefreshTokenResponse {
  refresh_token: string;
  access_token_expires_at: number;
}

export function sendCode(email: string) {
  return api.post<SendCodeResponse>("/auth/send-code/", { email });
}

export function verifyCode(email: string, code: string) {
  return api.post<RefreshTokenResponse>("/auth/verify-code/", { email, code });
}

export function refreshToken(refreshToken: string) {
  return api.post<RefreshTokenResponse>("/auth/refresh/", {
    refresh_token: refreshToken,
  });
}

export function logout(refreshToken: string) {
  return api.post<{ detail: string }>("/auth/log-out/", {
    refresh_token: refreshToken,
  });
}

