import api from "../../shared/lib/axios";

export type UserOrderField = "username" | "email" | "created_at" | "role";

export interface UserEntity {
  public_id: string;
  email: string;
  username: string | null;
  role: number;
  is_blocked: boolean;
  created_at: string;
}

export interface GetUsersParams {
  page?: number;
  limit?: number;
  search?: string;
  order_by?: UserOrderField;
  descending?: boolean;
  include_self?: boolean;
}

export interface GetUsersResponse {
  users: UserEntity[];
  total_count: number;
}

export function getMyProfile() {
  return api.get<UserEntity>("/users/me");
}

export function getUserProfile(publicId: string) {
  return api.get<UserEntity>(`/users/${publicId}`);
}

export function getUsers(params: GetUsersParams) {
  return api.get<GetUsersResponse>("/users/", { params });
}

export function updateMyUsername(username: string) {
  return api.patch<UserEntity>("/users/me/username", { username });
}

export function blockOrUnblockUser(publicId: string, block: boolean) {
  return api.patch<UserEntity>(`/users/${publicId}/block`, { block });
}

export function updateUserRole(publicId: string, newRole: number) {
  return api.patch<UserEntity>(`/users/${publicId}/role`, {
    new_role: newRole,
  });
}