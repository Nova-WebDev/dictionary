import { useEffect, useRef, useState, type ReactNode } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import Loader from "../base/Loader";
import { useAuthStore } from "../auth/store/authStore";
import { useAccessTokenScheduler } from "../auth/hooks/useAccessTokenScheduler";

interface AppProvidersProps {
  children: ReactNode;
}

export default function AppProviders({ children }: AppProvidersProps) {
  const navigate = useNavigate();
  const location = useLocation();

  const refreshToken = useAuthStore((state) => state.refreshToken);
  const [isReady, setIsReady] = useState(false);

  const navigateRef = useRef(navigate);
  const pathRef = useRef(location.pathname);

  useEffect(() => {
    navigateRef.current = navigate;
    pathRef.current = location.pathname;
  }, [navigate, location.pathname]);

  useAccessTokenScheduler();

  useEffect(() => {
    const path = location.pathname;

    if (refreshToken) {
      if (path.startsWith("/auth")) {
        navigateRef.current("/");
      }
    } else if (!path.startsWith("/auth")) {
      navigateRef.current("/auth/email");
    }

    setIsReady(true);
  }, [refreshToken, location.pathname]);

  useEffect(() => {
    const unsubscribe = useAuthStore.subscribe((state) => {
      if (state.refreshToken === null && !pathRef.current.startsWith("/auth")) {
        navigateRef.current("/auth/email");
      }
    });

    return unsubscribe;
  }, []);

  if (!isReady) {
    return <Loader />;
  }

  return <>{children}</>;
}