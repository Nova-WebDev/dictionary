import { useTempEmailStore } from "../store/useTempEmailStore";
import { useVerifyCodeForm } from "../hooks/useVerifyCodeForm";
import { useSendCode } from "../hooks/useSendCode";
import { useCodeInput } from "../hooks/useCodeInput";
import { useResendTimer } from "../hooks/useResendTimer";

const CODE_LENGTH = 5;

export default function VerifyPage() {
  const email = useTempEmailStore((state) => state.tempEmail);

  const { code, setInputRef, handleChange, handleKeyDown, value } =
    useCodeInput(CODE_LENGTH);
  const { secondsLeft, reset: resetTimer } = useResendTimer();
  const { submit, isPending, error } = useVerifyCodeForm(email);
  const { mutate: resendMutate, isPending: isResending } = useSendCode();

  const handleResend = () => {
    if (!email) return;
    resendMutate({ email });
    resetTimer();
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    submit(value);
  };

  return (
    <div className="flex items-center justify-center min-h-screen px-4 transition-colors bg-slate-50 sm:px-6 dark:bg-slate-950">
      <div className="w-full max-w-sm mx-auto overflow-hidden bg-white border border-cyan-100 shadow-lg sm:max-w-md dark:bg-slate-900 dark:border-slate-800 rounded-xl">
        <div className="h-1.5 bg-cyan-600 dark:bg-cyan-500"></div>

        <div className="p-6 sm:p-8">
          <h1 className="mb-2 text-3xl font-semibold text-center text-cyan-700 dark:text-cyan-400">
            Verify code
          </h1>

          <p className="mb-6 text-sm text-center text-slate-600 dark:text-slate-300">
            We sent a 5-character code to
            <span className="font-semibold text-cyan-700 dark:text-cyan-400">
              {" "}
              {email}
            </span>
          </p>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="flex justify-center gap-2 sm:gap-4">
              {code.map((char, index) => (
                <input
                  key={index}
                  ref={setInputRef(index)}
                  maxLength={1}
                  value={char}
                  inputMode="text"
                  onChange={(e) => handleChange(e.target.value, index)}
                  onKeyDown={(e) => handleKeyDown(e, index)}
                  className="w-10 h-10 text-xl text-center lowercase border border-slate-300 rounded-md sm:w-12 sm:h-12 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                />
              ))}
            </div>

            <button
              type="submit"
              disabled={isPending}
              className="w-full py-3 rounded-md bg-cyan-600 hover:bg-cyan-700 dark:bg-cyan-500 dark:hover:bg-cyan-600 text-white font-semibold tracking-wide transition active:scale-[0.98] disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
            >
              {isPending ? "Verifying..." : "Verify"}
            </button>
          </form>

          <div className="mt-4 text-center">
            {secondsLeft > 0 ? (
              <p className="text-sm text-slate-600 dark:text-slate-300">
                You can resend the code in{" "}
                <span className="font-semibold text-cyan-700 dark:text-cyan-400">
                  {secondsLeft}s
                </span>
              </p>
            ) : (
              <button
                onClick={handleResend}
                disabled={isResending}
                className="text-sm font-semibold text-cyan-700 transition cursor-pointer hover:text-cyan-800 dark:text-cyan-400 dark:hover:text-cyan-300 disabled:cursor-not-allowed"
              >
                {isResending ? "Sending..." : "Resend code"}
              </button>
            )}
          </div>

          {error && (
            <p className="mt-4 text-sm text-center text-red-600 dark:text-red-400">
              Invalid code.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}