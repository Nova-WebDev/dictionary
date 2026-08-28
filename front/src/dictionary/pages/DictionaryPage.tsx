import { DictionaryHeader } from "../components/DictionaryHeader";
import { Dictionarybody } from "../components/Dictionarybody";

export const DictionaryPage = () => {
  return (
    <div className="overflow-x-hidden">
      <DictionaryHeader />
      <Dictionarybody />
    </div>
  );
};