import { create } from "zustand";

export interface CurrentUser {
  public_id: string;
  email: string;
  username: string | null;
  role: number;
  is_blocked: boolean;
  created_at: string;
}

interface UserState {
  currentUser: CurrentUser | null;
  setCurrentUser: (user: CurrentUser) => void;
  clearCurrentUser: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  currentUser: null,
  setCurrentUser: (user) => set({ currentUser: user }),
  clearCurrentUser: () => set({ currentUser: null }),
}));