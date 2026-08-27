import { createPortal } from "react-dom";
import { HashLoader } from "react-spinners";

export default function Loader() {
  return createPortal(
    <div className="fixed inset-0 flex items-center justify-center backdrop-blur-sm bg-black/10 z-9999">
      <HashLoader size={60} color="#3b82f6" />
    </div>,
    document.body,
  );
}