import axios from "axios";
import { useAuthStore } from "../store/authStore";

const origin = window.location.origin;
const baseURL = `${origin}/api`;

interface PendingRequest {
  resolve: () => void;
  reject: (error: unknown) => void;
}

let isRefreshing = false;
let pendingQueue: PendingRequest[] = [];

function resolvePendingQueue(error: unknown | null) {
  pendingQueue.forEach(({ resolve, reject }) => {
    if (error) reject(error);
    else resolve();
  });
  pendingQueue = [];
}

export async function refreshAccessToken(): Promise<void> {
  const { refreshToken, setTokens, clearAuth } = useAuthStore.getState();

  if (!refreshToken) {
    clearAuth();
    throw new Error("No refresh token available");
  }

  if (isRefreshing) {
    return new Promise<void>((resolve, reject) => {
      pendingQueue.push({ resolve, reject });
    });
  }

  isRefreshing = true;

  try {
    const response = await axios.post<{
      refresh_token: string;
      access_token_expires_at: number;
    }>(
      `${baseURL}/auth/refresh/`,
      { refresh_token: refreshToken },
      { withCredentials: true }
    );

    setTokens(response.data.refresh_token, response.data.access_token_expires_at);
    resolvePendingQueue(null);
  } catch (error) {
    clearAuth();
    resolvePendingQueue(error);
    throw error;
  } finally {
    isRefreshing = false;
  }
}