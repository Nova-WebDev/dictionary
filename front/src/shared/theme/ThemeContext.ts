import { createContext } from "react";

export interface ThemeContextValue {
  theme: "light" | "dark";
  changeTheme: (theme: "light" | "dark") => void;
}

export const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);