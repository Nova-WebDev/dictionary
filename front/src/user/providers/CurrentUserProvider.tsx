import { useEffect, type ReactNode } from "react";
import { Outlet } from "react-router-dom";

import Loader from "../../base/Loader";
import { useFetchCurrentUser } from "../hooks/useFetchCurrentUser";
import { useUserStore } from "../store/userStore";

interface CurrentUserProviderProps {
  children?: ReactNode;
}

export function CurrentUserProvider({ children }: CurrentUserProviderProps) {
  const { data, isLoading, isError } = useFetchCurrentUser();
  const setCurrentUser = useUserStore((state) => state.setCurrentUser);
  const clearCurrentUser = useUserStore((state) => state.clearCurrentUser);

  useEffect(() => {
    if (data) {
      setCurrentUser(data);
    }
  }, [data, setCurrentUser]);

  useEffect(() => {
    if (isError) {
      clearCurrentUser();
    }
  }, [isError, clearCurrentUser]);

  if (isLoading) {
    return <Loader />;
  }

  return children ? <>{children}</> : <Outlet />;
}