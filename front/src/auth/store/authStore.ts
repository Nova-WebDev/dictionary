import { create } from "zustand";

interface AuthState {
  refreshToken: string | null;
  accessTokenExpiresAt: number | null;
  setTokens: (refreshToken: string, expiresAt: number) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  refreshToken: localStorage.getItem("refresh_token"),
  accessTokenExpiresAt: (() => {
    const stored = localStorage.getItem("access_token_expires_at");
    return stored ? Number(stored) : null;
  })(),
  setTokens: (refreshToken, expiresAt) => {
    localStorage.setItem("refresh_token", refreshToken);
    localStorage.setItem("access_token_expires_at", String(expiresAt));
    set({ refreshToken, accessTokenExpiresAt: expiresAt });
  },
  clearAuth: () => {
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("access_token_expires_at");
    set({ refreshToken: null, accessTokenExpiresAt: null });
  },
}));