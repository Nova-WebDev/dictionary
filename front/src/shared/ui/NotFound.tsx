import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCompass, faHome, faRotate } from "@fortawesome/free-solid-svg-icons";

export default function NotFound() {
  return (
    <div className="fixed inset-0 flex items-center justify-center overflow-hidden bg-teal-50 dark:bg-[#0b1020]">
      <div className="absolute inset-0 pointer-events-none">
        <div
          className="absolute -left-32 -top-32 w-[55vmax] h-[55vmax] rounded-full blur-[90px] opacity-50 dark:opacity-30"
          style={{
            background:
              "radial-gradient(circle at 30% 30%, rgba(20,184,166,0.35), transparent 40%), radial-gradient(circle at 70% 70%, rgba(45,212,191,0.28), transparent 45%)",
          }}
        />
        <div
          className="absolute -right-32 -bottom-32 w-[50vmax] h-[50vmax] rounded-full blur-[80px] opacity-45 dark:opacity-25"
          style={{
            background:
              "radial-gradient(circle at 20% 20%, rgba(13,148,136,0.3), transparent 35%), radial-gradient(circle at 80% 80%, rgba(15,118,110,0.24), transparent 40%)",
          }}
        />
      </div>

      <div className="relative z-10 flex flex-col items-center gap-10 px-6">
        <div
          className="
    relative flex items-center justify-center
    w-[clamp(200px,30vmin,250px)]
    h-[clamp(200px,30vmin,250px)]
    rounded-full
    bg-white/70 dark:bg-white/12
    backdrop-blur-[22px]
    border border-teal-200/70 dark:border-white/15
    shadow-[0_30px_90px_rgba(13,148,136,0.25)] dark:shadow-[0_30px_90px_rgba(0,0,0,0.45)]
    animate-pulse-slow
  "
        >
          <div className="absolute inset-0 rounded-full pointer-events-none opacity-80 dark:opacity-45" />
          <FontAwesomeIcon
            icon={faCompass}
            className="relative text-[clamp(48px,10vmin,70px)] text-teal-700 dark:text-gray-200 drop-shadow-[0_10px_30px_rgba(13,148,136,0.3)] dark:drop-shadow-[0_10px_30px_rgba(0,0,0,0.45)]"
          />
        </div>

        <div className="mt-5 text-center">
          <h1 className="text-5xl font-extrabold tracking-tight text-teal-900 md:text-6xl dark:text-gray-100">
            404
          </h1>
          <p className="mt-2 text-sm text-teal-700/80 md:text-base dark:text-gray-300">
            Page not found
          </p>
        </div>

        <div className="flex gap-4">
          <Link
            to="/"
            className="inline-flex items-center gap-2 px-6 py-3 text-teal-900 transition border border-teal-300 cursor-pointer rounded-xl bg-teal-500/15 dark:bg-teal-500/10 dark:text-gray-100 backdrop-blur-md dark:border-teal-500/20 hover:bg-teal-500/25 dark:hover:bg-teal-500/20"
          >
            <FontAwesomeIcon icon={faHome} />
            Home
          </Link>

          <button
            onClick={() => window.location.reload()}
            className="inline-flex items-center gap-2 px-6 py-3 text-teal-900 transition border border-teal-300 cursor-pointer rounded-xl bg-teal-500/15 dark:bg-teal-500/10 dark:text-gray-200 hover:bg-teal-500/25 dark:hover:bg-teal-500/20 backdrop-blur-md"
          >
            <FontAwesomeIcon icon={faRotate} />
            Retry
          </button>
        </div>
      </div>

      <style>{`
        @keyframes pulse-slow {
          0% { transform: scale(1); box-shadow: 0 30px 90px rgba(13,148,136,0.25); }
          50% { transform: scale(1.04); box-shadow: 0 40px 110px rgba(13,148,136,0.35); }
          100% { transform: scale(1); box-shadow: 0 30px 90px rgba(13,148,136,0.25); }
        }
        .animate-pulse-slow {
          animation: pulse-slow 4s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
}