import { createBrowserRouter } from "react-router-dom";
import RootLayout from "../layouts/RootLayout";
import NotFound from "../../shared/ui/NotFound";

import { authRoutes } from "../../auth/routes/authRoutes";
import { appRoutes } from "./appRoutes";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    children: [
      ...authRoutes,
      ...appRoutes,
      { path: "*", element: <NotFound /> },
    ],
  },
]);

export default router;