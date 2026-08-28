import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { searchEnglishToPersian, searchPersianToEnglish } from "../api/dictionary";
import { useDebouncedValue } from "../../shared/hooks/useDebouncedValue";

export type SearchDirection = "en-to-fa" | "fa-to-en";

const DEBOUNCE_MS = 400;

export function useWordSearch() {
  const [direction, setDirection] = useState<SearchDirection>("en-to-fa");
  const [query, setQuery] = useState("");

  const debouncedQuery = useDebouncedValue(query, DEBOUNCE_MS);

  const searchFn = direction === "en-to-fa" ? searchEnglishToPersian : searchPersianToEnglish;

  const { data, isFetching, isError } = useQuery({
    queryKey: ["word-search", direction, debouncedQuery],
    queryFn: () => searchFn(debouncedQuery).then((res) => res.data),
    enabled: debouncedQuery.trim().length > 0,
  });

  const toggleDirection = () => {
    setDirection((prev) => (prev === "en-to-fa" ? "fa-to-en" : "en-to-fa"));
    setQuery("");
  };

  const results = useMemo(() => data ?? [], [data]);

  return {
    direction,
    query,
    setQuery,
    toggleDirection,
    results,
    isFetching,
    isError,
    hasQuery: debouncedQuery.trim().length > 0,
  };
}