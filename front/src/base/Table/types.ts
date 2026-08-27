import type { ReactNode } from "react";

/**
 * یک ستون جدول. `orderBy` فقط وقتی بده که ستون قابل سورت باشه —
 * اسمش باید همون key ای باشه که بک‌اند برای order_by می‌فهمه.
 */
export interface TableColumn<T> {
  label: string;
  orderBy?: string;
  render: (row: T) => ReactNode;
}

/** یک اکشن روی هر ردیف (ویرایش، حذف، بلاک و...). */
export interface TableAction<T> {
  label: () => string;
  render: (row: T) => ReactNode;
}

/**
 * خروجی هوکی مثل usePersonnelTableData.
 * همون چیزی که به عنوان prop به نام `table` پاس داده می‌شه.
 */
export interface TableState<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  orderBy?: string;
  deorder: boolean;
  search: string;
  setPage: (page: number) => void;
  setLimit: (limit: number) => void;
  setOrderBy: (orderBy: string | undefined) => void;
  setDeorder: (deorder: boolean) => void;
  setSearch: (search: string) => void;
}

export interface TableProps<T> {
  columns: TableColumn<T>[];
  actions?: TableAction<T>[];
  table: TableState<T>;
}

export type TableBodyMode = "desktop" | "mobile";

export interface TableBodyProps<T> {
  data: T[];
  columns: TableColumn<T>[];
  actions?: TableAction<T>[];
  mode: TableBodyMode;
}

export interface TableHeaderProps<T> {
  columns: TableColumn<T>[];
  orderBy?: string;
  deorder: boolean;
  onSort: (orderBy: string) => void;
}

export interface TableSortSelectorProps<T> {
  columns: TableColumn<T>[];
  orderBy?: string;
  deorder: boolean;
  onSort: (orderBy: string) => void;
}

export interface TableSearchProps {
  value: string;
  onChange: (value: string) => void;
}

export interface TableLimitSelectorProps {
  limit: number;
  onChange: (limit: number) => void;
}

export interface TablePaginationProps {
  page: number;
  total: number;
  limit: number;
  onPageChange: (page: number) => void;
}

export interface TableContainerProps {
  children: ReactNode;
}
