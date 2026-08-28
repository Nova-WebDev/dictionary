import { useEffect, useState } from "react";

const RESEND_INTERVAL_SECONDS = 60;

export function useResendTimer() {
  const [secondsLeft, setSecondsLeft] = useState(RESEND_INTERVAL_SECONDS);

  useEffect(() => {
    if (secondsLeft === 0) return;
    const interval = setInterval(() => setSecondsLeft((s) => s - 1), 1000);
    return () => clearInterval(interval);
  }, [secondsLeft]);

  const reset = () => setSecondsLeft(RESEND_INTERVAL_SECONDS);

  return { secondsLeft, reset };
}