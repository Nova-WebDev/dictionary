interface SeparatorProps {
  width?: string;
  height?: string;
  className?: string;
}

export default function Separator({
  width = "2rem",
  height = "1px",
  className = "",
}: SeparatorProps) {
  return (
    <div
      style={{ width, height }}
      className={`
        mx-auto my-0.5 bg-gray-400 dark:bg-gray-600
        ${className}
      `}
    />
  );
}