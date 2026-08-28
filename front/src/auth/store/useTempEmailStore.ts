import { create } from "zustand";

interface TempEmailState {
  tempEmail: string | null;
  setTempEmail: (email: string) => void;
  clearTempEmail: () => void;
}

export const useTempEmailStore = create<TempEmailState>((set) => ({
  tempEmail: null,
  setTempEmail: (email) => set({ tempEmail: email }),
  clearTempEmail: () => set({ tempEmail: null }),
}));