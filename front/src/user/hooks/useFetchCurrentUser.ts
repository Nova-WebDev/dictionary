import { useQuery } from "@tanstack/react-query";
import { getMyProfile } from "../api/user";

export function useFetchCurrentUser() {
  return useQuery({
    queryKey: ["currentUser"],
    queryFn: () => getMyProfile().then((res) => res.data),
    retry: false,
  });
}