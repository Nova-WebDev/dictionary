import { useEffect } from "react";
import { useAuthStore } from "../store/authStore";
import { refreshAccessToken } from "../services/refreshService";

const REFRESH_BUFFER_SECONDS = 30;

export function useAccessTokenScheduler() {
  const refreshToken = useAuthStore((state) => state.refreshToken);
  const accessTokenExpiresAt = useAuthStore((state) => state.accessTokenExpiresAt);

  useEffect(() => {
    if (!refreshToken) return;

    if (!accessTokenExpiresAt) {
      refreshAccessToken().catch(() => {});
      return;
    }

    const now = Math.floor(Date.now() / 1000);
    const secondsUntilRefresh = accessTokenExpiresAt - now - REFRESH_BUFFER_SECONDS;

    if (secondsUntilRefresh <= 0) {
      refreshAccessToken().catch(() => {});
      return;
    }

    const timeoutId = setTimeout(() => {
      refreshAccessToken().catch(() => {});
    }, secondsUntilRefresh * 1000);

    return () => clearTimeout(timeoutId);
  }, [refreshToken, accessTokenExpiresAt]);
}