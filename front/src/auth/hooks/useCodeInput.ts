import { useRef, useState } from "react";

export function useCodeInput(length: number) {
  const [code, setCode] = useState<string[]>(Array(length).fill(""));
  const inputsRef = useRef<(HTMLInputElement | null)[]>([]);

  const setInputRef = (index: number) => (el: HTMLInputElement | null) => {
    inputsRef.current[index] = el;
  };

  const handleChange = (value: string, index: number) => {
    if (!/^[a-zA-Z0-9]?$/.test(value)) return;

    const lowerValue = value.toLowerCase();
    const newCode = [...code];
    newCode[index] = lowerValue;
    setCode(newCode);

    if (lowerValue && index < length - 1) {
      inputsRef.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>, index: number) => {
    if (e.key === "Backspace" && !code[index] && index > 0) {
      inputsRef.current[index - 1]?.focus();
    }
  };

  const reset = () => setCode(Array(length).fill(""));

  return {
    code,
    setInputRef,
    handleChange,
    handleKeyDown,
    reset,
    value: code.join(""),
  };
}