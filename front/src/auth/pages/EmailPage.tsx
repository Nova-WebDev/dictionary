import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEnvelope, faPaperPlane } from "@fortawesome/free-solid-svg-icons";

import { useSendCode } from "../hooks/useSendCode";
import { useTempEmailStore } from "../store/useTempEmailStore";

export default function EmailPage() {
  const [email, setEmail] = useState("");
  const { mutate, isPending, isSuccess, error } = useSendCode();

  const setTempEmail = useTempEmailStore((state) => state.setTempEmail);
  const navigate = useNavigate();

  const navigateRef = useRef(navigate);
  const setTempEmailRef = useRef(setTempEmail);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      mutate({ email });
    }
  };

  useEffect(() => {
    if (isSuccess) {
      setTempEmailRef.current(email);
      navigateRef.current("/auth/verify");
    }
  }, [isSuccess, email]);

  return (
    <div className="flex items-center justify-center min-h-screen px-4 transition-colors bg-slate-50 sm:px-6 dark:bg-slate-950">
      <div className="w-full max-w-sm mx-auto overflow-hidden bg-white border border-cyan-100 shadow-lg sm:max-w-md dark:bg-slate-900 dark:border-slate-800 rounded-xl">
        <div className="h-1.5 bg-cyan-600 dark:bg-cyan-500"></div>

        <div className="p-6 sm:p-8">
          <h1 className="mb-6 text-3xl font-semibold text-center text-cyan-700 dark:text-cyan-400">
            Sign in with email
          </h1>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block mb-1 text-sm text-slate-600 dark:text-slate-300">
                Email address
              </label>
              <div className="relative">
                <span className="absolute text-slate-400 -translate-y-1/2 left-3 top-1/2 dark:text-slate-500">
                  <FontAwesomeIcon icon={faEnvelope} className="w-5 h-5" />
                </span>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  className="w-full py-3 pr-4 text-slate-900 placeholder-slate-400 transition border border-slate-300 rounded-md pl-11 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 dark:text-slate-100 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isPending}
              className="w-full py-3 cursor-pointer rounded-md bg-cyan-600 hover:bg-cyan-700 dark:bg-cyan-500 dark:hover:bg-cyan-600 text-white font-semibold tracking-wide transition active:scale-[0.98] disabled:opacity-60 flex items-center justify-center gap-2"
            >
              <FontAwesomeIcon icon={faPaperPlane} className="w-4 h-4" />
              {isPending ? "Sending..." : "Send code"}
            </button>
          </form>

          {error && (
            <p className="mt-4 text-sm text-center text-red-600 dark:text-red-400">
              Something went wrong.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}