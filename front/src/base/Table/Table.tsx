import type { TableProps } from "./types";
import TableContainer from "./TableContainer";
import TableHeader from "./TableHeader";
import TableBody from "./TableBody";
import TableSearch from "./TableSearch";
import TableSortSelector from "./TableSortSelector";
import TableLimitSelector from "./TableLimitSelector";
import TablePagination from "./TablePagination";

export default function Table<T>({ columns, actions, table }: TableProps<T>) {
  const handleSort = (col: string) => {
    if (table.orderBy !== col) {
      table.setOrderBy(col);
      table.setDeorder(false);
      table.setPage(1);
      return;
    }
    table.setDeorder(!table.deorder);
    table.setPage(1);
  };

  const handleSearch = (value: string) => {
    table.setSearch(value);
    table.setOrderBy(undefined);
    table.setDeorder(false);
    table.setPage(1);
  };

  const handleLimit = (value: number) => {
    table.setLimit(value);
    table.setPage(1);
  };

  const handlePage = (value: number) => {
    table.setPage(value);
  };

  return (
    <TableContainer>
      <div className="flex">
        <TableSearch value={table.search} onChange={handleSearch} />
        <TableSortSelector
          columns={columns}
          orderBy={table.orderBy}
          deorder={table.deorder}
          onSort={handleSort}
        />
      </div>

      <div className="overflow-x-auto">
        <table
          className="hidden w-full text-sm md:table"
          style={{ borderCollapse: "separate", borderSpacing: "0 12px" }}
        >
          <TableHeader
            columns={columns}
            orderBy={table.orderBy}
            deorder={table.deorder}
            onSort={handleSort}
          />
          <tbody>
            <TableBody
              data={table.data}
              columns={columns}
              actions={actions}
              mode="desktop"
            />
          </tbody>
        </table>

        <div className="md:hidden">
          <TableBody
            data={table.data}
            columns={columns}
            actions={actions}
            mode="mobile"
          />
        </div>
      </div>

      <div className="flex items-center justify-between mt-4">
        <TablePagination
          page={table.page}
          total={table.total}
          limit={table.limit}
          onPageChange={handlePage}
        />
        <TableLimitSelector limit={table.limit} onChange={handleLimit} />
      </div>
    </TableContainer>
  );
}
