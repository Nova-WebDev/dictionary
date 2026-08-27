import type { TableContainerProps } from "./types";

export default function TableContainer({ children }: TableContainerProps) {
  return <div className="pb-5 md:p-5">{children}</div>;
}
