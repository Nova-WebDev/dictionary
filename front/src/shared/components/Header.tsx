import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faMoon, faSun, faUser } from "@fortawesome/free-solid-svg-icons";

import { useTheme } from "../theme";
import { useUserStore } from "../../user/store/userStore";
import ProfileDropdown from "./ProfileDropdown";
import EditUsernameModal from "../../user/components/EditUsernameModal";

interface HeaderProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

export function Header({ isOpen, setIsOpen }: HeaderProps) {
  const { theme, changeTheme } = useTheme();
  const currentUser = useUserStore((state) => state.currentUser);

  const [openDropdown, setOpenDropdown] = useState(false);
  const [openEditModal, setOpenEditModal] = useState(false);

  const toggleTheme = () => {
    changeTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <>
      <div className="flex items-center justify-between px-6 py-4 border-b border-cyan-500/20 bg-linear-to-r from-cyan-700 to-cyan-600 dark:from-slate-900 dark:to-slate-900 dark:border-slate-800">
        <div className="flex items-center gap-3">
          <button
            className="text-lg text-white md:hidden dark:text-slate-200"
            onClick={() => setIsOpen(!isOpen)}
          >
            <FontAwesomeIcon icon={faBars} className="w-5 h-5" />
          </button>

          <h1 className="hidden text-lg font-bold text-white md:block dark:text-slate-100">
            Dictionary
          </h1>
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={toggleTheme}
            className="flex items-center justify-center w-10 h-10 text-white transition rounded-full cursor-pointer bg-white/15 hover:bg-white/25 dark:bg-slate-800 dark:hover:bg-slate-700"
          >
            <FontAwesomeIcon
              icon={theme === "dark" ? faSun : faMoon}
              className="w-4 h-4"
            />
          </button>

          <div className="relative">
            <button
              onClick={() => setOpenDropdown((prev) => !prev)}
              className="flex items-center gap-2.5 py-1.5 pl-1.5 pr-3 text-white transition rounded-full cursor-pointer select-none bg-white/15 hover:bg-white/25 dark:bg-slate-800 dark:hover:bg-slate-700"
            >
              <div className="flex items-center justify-center w-7 h-7 rounded-full bg-white/20 dark:bg-slate-700">
                <FontAwesomeIcon icon={faUser} className="w-3.5 h-3.5" />
              </div>

              {currentUser?.username ? (
                <span className="text-sm font-medium sm:inline dark:text-slate-200">
                  {currentUser.username}
                </span>
              ) : null}
            </button>

            <ProfileDropdown
              open={openDropdown}
              setOpen={setOpenDropdown}
              onEditUsername={() => setOpenEditModal(true)}
            />
          </div>
        </div>
      </div>

      <EditUsernameModal open={openEditModal} onClose={() => setOpenEditModal(false)} />
    </>
  );
}