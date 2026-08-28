import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getUsers, type UserOrderField } from "../api/user";
import { useDebouncedValue } from "../../shared/hooks/useDebouncedValue";
import type { TableState } from "../../base/Table";
import type { UserEntity } from "../api/user";

const DEBOUNCE_MS = 400;

export function useUsersTable(): TableState<UserEntity> {
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [orderBy, setOrderBy] = useState<string | undefined>(undefined);
  const [deorder, setDeorder] = useState(false);
  const [search, setSearch] = useState("");

  const debouncedSearch = useDebouncedValue(search, DEBOUNCE_MS);

  const { data } = useQuery({
    queryKey: ["users", page, limit, debouncedSearch, orderBy, deorder],
    queryFn: () =>
      getUsers({
        page,
        limit,
        search: debouncedSearch,
        order_by: (orderBy as UserOrderField) ?? "email",
        descending: deorder,
        include_self: false,
      }).then((res) => res.data),
  });

  return {
    data: data?.users ?? [],
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