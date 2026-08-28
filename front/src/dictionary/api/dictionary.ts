import api from "../../shared/lib/axios";

export type WordOrderField = "persian_word" | "english_word" | "created_at";

export interface WordEntry {
  public_id: string;
  persian_word: string;
  english_word: string;
  author_id: string | null;
  created_at: string;
}

export interface WordEntryWithAuthor {
  public_id: string;
  persian_word: string;
  english_word: string;
  author_name: string | null;
  created_at: string;
}

export interface GetWordsParams {
  page?: number;
  limit?: number;
  search?: string;
  order_by?: WordOrderField;
  descending?: boolean;
}

export interface GetWordsResponse {
  words: WordEntryWithAuthor[];
  total_count: number;
}

export function searchPersianToEnglish(query: string) {
  return api.get<WordEntry[]>("/words/search/persian-to-english", {
    params: { q: query },
  });
}

export function searchEnglishToPersian(query: string) {
  return api.get<WordEntry[]>("/words/search/english-to-persian", {
    params: { q: query },
  });
}

export function getWords(params: GetWordsParams) {
  return api.get<GetWordsResponse>("/words/", { params });
}

export function createWord(persianWord: string, englishWord: string) {
  return api.post<WordEntry>("/words/", {
    persian_word: persianWord,
    english_word: englishWord,
  });
}

export function editWord(
  publicId: string,
  persianWord: string,
  englishWord: string
) {
  return api.patch<WordEntry>(`/words/${publicId}`, {
    persian_word: persianWord,
    english_word: englishWord,
  });
}

export function deleteWord(publicId: string) {
  return api.delete<{ detail: string }>(`/words/${publicId}`);
}