import { CurrentUserProvider } from "../../user/providers/CurrentUserProvider";
import { Layout } from "../../shared/layout/Layout";
import { HomePage } from "../../dictionary/pages/HomePage";
import { DictionaryPage } from "../../dictionary/pages/DictionaryPage";
import { UserPage } from "../../user/pages/UserPage";

export const appRoutes = [
  {
    element: <CurrentUserProvider />,
    children: [
      {
        element: <Layout />,
        children: [
          { index: true, element: <HomePage /> },
          { path: "words", element: <DictionaryPage /> },
          { path: "users", element: <UserPage /> },
        ],
      },
    ],
  },
];