import { Outlet, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";

import { Sidebar } from "../components/Sidebar";
import { Header } from "../components/Header";

export function Layout() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    setIsOpen(false);
  }, [location.pathname]);

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar isOpen={isOpen} setIsOpen={setIsOpen} />

      <div className="flex flex-col flex-1 h-full min-w-0">
        <div className="shrink-0">
          <Header isOpen={isOpen} setIsOpen={setIsOpen} />
        </div>

        <div className="flex-1 overflow-y-auto bg-gray-50/25 dark:bg-[#0d1528]">
          <Outlet />
        </div>
      </div>
    </div>
  );
}