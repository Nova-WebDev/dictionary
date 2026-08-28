import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getWords, type WordOrderField } from "../api/dictionary";
import { useDebouncedValue } from "../../shared/hooks/useDebouncedValue";
import type { TableState } from "../../base/Table";

const DEBOUNCE_MS = 400;

export function useDictionaryTable(): TableState<import("../api/dictionary").WordEntryWithAuthor> {
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [orderBy, setOrderBy] = useState<string | undefined>(undefined);
  const [deorder, setDeorder] = useState(false);
  const [search, setSearch] = useState("");

  const debouncedSearch = useDebouncedValue(search, DEBOUNCE_MS);

  const { data } = useQuery({
    queryKey: ["words", page, limit, debouncedSearch, orderBy, deorder],
    queryFn: () =>
      getWords({
        page,
        limit,
        search: debouncedSearch,
        order_by: (orderBy as WordOrderField) ?? "created_at",
        descending: deorder,
      }).then((res) => res.data),
  });

  return {
    data: data?.words ?? [],
    total: data?.total_count ?? 0,
    page,
    limit,
    orderBy,
    deorder,
    search,
    setPage,
    setLimit,
    setOrderBy,
    setDeorder,
    setSearch,
  };
}