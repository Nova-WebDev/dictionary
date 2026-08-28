import type { TableBodyProps } from "./types";

export default function TableBody<T>({ data, columns, actions, mode }: TableBodyProps<T>) {
  if (mode === "desktop") {
    return (
      <>
        {data.map((row, idx) => (
          <tr key={idx} className="group">
            {columns.map((col, i) => (
              <td
                key={i}
                className={`
                  px-4 py-4 align-middle whitespace-nowrap
                  bg-slate-100 dark:bg-slate-800
                  text-slate-800 dark:text-slate-100
                  transition-colors duration-200
                  group-hover:bg-slate-200 dark:group-hover:bg-slate-700
                  first:rounded-l-xl
                `}
              >
                <div className="flex items-center h-12">
                  <div className="w-full">{col.render(row)}</div>
                </div>
              </td>
            ))}

            {actions && (
              <td
                className={`
                  px-4 py-4 align-middle whitespace-nowrap
                  bg-slate-100 dark:bg-slate-800
                  text-slate-800 dark:text-slate-100
                  transition-colors duration-200
                  group-hover:bg-slate-200 dark:group-hover:bg-slate-700
                  last:rounded-r-xl
                `}
              >
                <div className="flex items-center gap-2">
                  {actions.map((action, i) => (
                    <div key={i}>{action.render(row)}</div>
                  ))}
                </div>
              </td>
            )}
          </tr>
        ))}
      </>
    );
  }

  return (
    <div className="pt-3 space-y-4 md:hidden">
      {data.map((row, idx) => (
        <article
          key={idx}
          className="
            bg-slate-100 dark:bg-slate-800
            rounded-2xl p-4
            shadow-sm
            transition-all duration-200
            hover:shadow-md
            hover:bg-slate-200 dark:hover:bg-slate-700
            focus-within:shadow-md
            flex flex-col gap-3
            ring-0 outline-none
          "
          tabIndex={0}
        >
          {columns.map((col, i) => (
            <div
              key={i}
              className="flex flex-col gap-1 px-1 py-0.5"
              aria-label={`field-${col.label.toLowerCase().replace(/\s+/g, "-")}`}
            >
              <div className="text-[11px] leading-4 text-slate-500 dark:text-slate-300">
                {col.label}
              </div>

              <div className="p-2 text-sm font-normal leading-5 text-slate-800 wrap-break-word dark:text-slate-100">
                {col.render(row)}
              </div>

              {i !== columns.length - 1 && (
                <div className="w-full h-px mt-2 bg-slate-200/60 dark:bg-white/6" />
              )}
            </div>
          ))}

          {actions && (
            <div className="flex flex-col gap-2 pt-2 mt-1 border-t border-slate-300/30 dark:border-slate-600/30">
              {actions.map((action, i) => (
                <div key={i} className="w-full">
                  <div className="flex items-center justify-center w-full">
                    {action.render(row)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </article>
      ))}
    </div>
  );
}