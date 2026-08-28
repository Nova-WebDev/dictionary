import { SidebarMenu } from "./SidebarMenu";

interface SidebarProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

export function Sidebar({ isOpen, setIsOpen }: SidebarProps) {
  return (
    <>
      <div className="hidden h-screen border-r md:block w-72 min-w-72 border-slate-200 dark:border-slate-800">
        <SidebarMenu />
      </div>

      <div
        className={`fixed h-screen inset-y-0 left-0 w-72 min-w-72 border-r border-slate-200 dark:border-slate-800 transform transition-transform duration-300 ease-in-out z-50 md:hidden ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <SidebarMenu />
      </div>

      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/30 backdrop-blur-sm md:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
}