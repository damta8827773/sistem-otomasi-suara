/**
 * Voice command vocabulary. Each spec maps trigger keywords (per locale) to an
 * action the automation service knows how to run. Keep this table as the single
 * place to add or tweak what the system understands.
 */

export type ActionId =
  | "open_site"
  | "search"
  | "time"
  | "date"
  | "scroll_down"
  | "scroll_up"
  | "toggle_theme"
  | "reload"
  | "back"
  | "help"
  | "unknown";

export interface CommandSpec {
  action: ActionId;
  /** Trigger keywords per locale, lower case. */
  keywords: { id: string[]; en: string[] };
  /**
   * When true the command captures the remaining words after the keyword as an
   * argument (for example the site name in "buka youtube").
   */
  captures?: boolean;
}

// Order matters: capture commands and specific phrases are listed first.
export const COMMANDS: CommandSpec[] = [
  { action: "open_site", keywords: { id: ["buka"], en: ["open"] }, captures: true },
  { action: "search", keywords: { id: ["cari", "carikan"], en: ["search", "find"] }, captures: true },
  { action: "time", keywords: { id: ["jam berapa", "jam"], en: ["what time", "time"] } },
  { action: "date", keywords: { id: ["tanggal berapa", "tanggal", "hari apa"], en: ["what date", "date", "what day"] } },
  { action: "scroll_down", keywords: { id: ["gulir bawah", "scroll bawah", "ke bawah"], en: ["scroll down"] } },
  { action: "scroll_up", keywords: { id: ["gulir atas", "scroll atas", "ke atas"], en: ["scroll up"] } },
  { action: "toggle_theme", keywords: { id: ["mode gelap", "mode terang", "ganti tema", "ubah tema"], en: ["dark mode", "light mode", "toggle theme"] } },
  { action: "reload", keywords: { id: ["muat ulang", "segarkan"], en: ["reload", "refresh"] } },
  { action: "back", keywords: { id: ["kembali"], en: ["go back"] } },
  { action: "help", keywords: { id: ["bantuan", "perintah apa saja"], en: ["help", "what can you do"] } },
];

/** Known site shortcuts for the open_site action. */
export const SITES: Record<string, string> = {
  youtube: "https://youtube.com",
  google: "https://google.com",
  github: "https://github.com",
  gmail: "https://mail.google.com",
  whatsapp: "https://web.whatsapp.com",
  instagram: "https://instagram.com",
  tiktok: "https://tiktok.com",
  maps: "https://maps.google.com",
};
