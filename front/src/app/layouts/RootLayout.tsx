import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Outlet } from "react-router-dom";

import { ThemeProvider } from "../../shared/theme";
import AppProviders from "../AppProviders";

const queryClient = new QueryClient();

export default function RootLayout() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AppProviders>
          <Outlet />
        </AppProviders>
      </ThemeProvider>
    </QueryClientProvider>
  );
}