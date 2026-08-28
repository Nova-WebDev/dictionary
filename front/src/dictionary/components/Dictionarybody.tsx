import { useState } from "react";
import Table from "../../base/Table";
import type { TableColumn, TableAction } from "../../base/Table";
import { useDictionaryTable } from "../hooks/useDictionaryTable";
import { EditWordAction } from "./EditWordAction";
import { DeleteWordAction } from "./DeleteWordAction";
import { EditWordModal } from "./EditWordModal";
import type { WordEntryWithAuthor } from "../api/dictionary";

const columns: TableColumn<WordEntryWithAuthor>[] = [
{
    label: "English",
    orderBy: "english_word",
    render: (row) => row.english_word,
  },
  {
    label: "Persian",
    orderBy: "persian_word",
    render: (row) => row.persian_word,
  },
  {
    label: "Author",
    render: (row) => row.author_name ?? "—",
  },
];

export const Dictionarybody = () => {
  const table = useDictionaryTable();
  const [editingWord, setEditingWord] = useState<WordEntryWithAuthor | null>(null);

  const actions: TableAction<WordEntryWithAuthor>[] = [
    {
      label: () => "Edit",
      render: (row) => <EditWordAction row={row} onEdit={setEditingWord} />,
    },
    {
      label: () => "Delete",
      render: (row) => <DeleteWordAction row={row} />,
    },
  ];

  return (
    <div className="mx-4 overflow-hidden md:mx-8">
      <Table columns={columns} actions={actions} table={table} />

      <EditWordModal
        open={editingWord !== null}
        onClose={() => setEditingWord(null)}
        word={editingWord}
      />
    </div>
  );
};