import Table from "../../base/Table";
import type { TableColumn, TableAction } from "../../base/Table";
import { useUsersTable } from "../hooks/useUsersTable";
import { ToggleBlockAction } from "./ToggleBlockAction";
import { RoleSelectAction } from "./RoleSelectAction";
import type { UserEntity } from "../api/user";

const columns: TableColumn<UserEntity>[] = [
  {
    label: "Username",
    orderBy: "username",
    render: (row) => row.username ?? "—",
  },
  {
    label: "Email",
    orderBy: "email",
    render: (row) => row.email,
  },

  {
    label: "Role",
    render: (row) => <RoleSelectAction row={row} />,
  },
];

const actions: TableAction<UserEntity>[] = [
  {
    label: () => "Block",
    render: (row) => <ToggleBlockAction row={row} />,
  },
];

export const UserBody = () => {
  const table = useUsersTable();

  return (
    <div className="mx-4 overflow-hidden md:mx-8">
      <Table columns={columns} actions={actions} table={table} />
    </div>
  );
};