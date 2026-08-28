import EmailPage from "../pages/EmailPage";
import VerifyPage from "../pages/VerifyPage";

export const authRoutes = [
  { path: "/auth", element: <EmailPage /> },
  { path: "/auth/email", element: <EmailPage /> },
  { path: "/auth/verify", element: <VerifyPage /> },
];