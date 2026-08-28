import { NavLink } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faHouse,
  faBookOpen,
  faUsers,
  faRightFromBracket,
} from "@fortawesome/free-solid-svg-icons";
import Separator from "../../base/Separator";
import { useLogout } from "../../auth/hooks/useLogout";
import { useAuthStore } from "../../auth/store/authStore";
import { useUserStore } from "../../user/store/userStore";

interface MenuItem {
  to: string;
  label: string;
  icon: typeof faHouse;
  minRole: number;
}

const menu: MenuItem[] = [
  { to: "/", label: "Home", icon: faHouse, minRole: 0 },
  { to: "/words", label: "Dictionary", icon: faBookOpen, minRole: 10 },
  { to: "/users", label: "Users", icon: faUsers, minRole: 20 },
];

export function SidebarMenu() {
  const refreshToken = useAuthStore((state) => state.refreshToken);
  const currentUser = useUserStore((state) => state.currentUser);
  const { mutate: logoutMutate, isPending } = useLogout();

  const visibleMenu = menu.filter((item) => (currentUser?.role ?? 0) >= item.minRole);

  const handleLogout = () => {
    if (!refreshToken) return;
    logoutMutate({ refresh_token: refreshToken });
  };

  return (
    <div className="flex flex-col w-full h-full px-3 pt-5 pb-4 bg-white dark:bg-slate-900">
      <div className="flex items-center gap-2 px-2 mb-4">
        <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-linear-to-br from-cyan-500 to-cyan-700 shadow-sm">
          <FontAwesomeIcon icon={faBookOpen} className="w-4 h-4 text-white" />
        </div>
        <span className="text-lg font-bold tracking-tight text-slate-800 dark:text-slate-100">
          Dictionary
        </span>
      </div>

      <Separator width="100%" />

      <div className="mt-2 mb-3 text-xs font-semibold tracking-wide uppercase text-slate-400 dark:text-slate-500 px-2">
        Main Menu
      </div>

      <nav className="flex flex-col gap-1">
        {visibleMenu.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              `group flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                isActive
                  ? "bg-linear-to-r from-cyan-500 to-cyan-600 text-white shadow-sm shadow-cyan-500/30"
                  : "text-slate-600 dark:text-slate-300 hover:bg-cyan-50 dark:hover:bg-slate-800 hover:text-cyan-700 dark:hover:text-cyan-400"
              }`
            }
          >
            <FontAwesomeIcon icon={item.icon} className="w-4 h-4" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="flex-1" />

      <Separator width="100%" />

      <button
        onClick={handleLogout}
        disabled={isPending}
        className="flex items-center gap-3 px-3 py-2.5 mt-3 rounded-lg text-sm font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-500/10 transition-all duration-150 disabled:opacity-60 cursor-pointer"
      >
        <FontAwesomeIcon icon={faRightFromBracket} className="w-4 h-4" />
        <span>{isPending ? "Logging out..." : "Log out"}</span>
      </button>
    </div>
  );
}