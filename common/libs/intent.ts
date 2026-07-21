import { COMMANDS, type ActionId } from "@/common/constants/commands";
import type { Locale } from "@/i18n/routing";

/** A recognized command ready to be executed. */
export interface Intent {
  action: ActionId;
  /** Captured argument (site name, search query), empty when none. */
  arg: string;
  /** The original spoken transcript. */
  raw: string;
}

/**
 * Turn a spoken transcript into an Intent by keyword matching against the
 * command table. Capture commands (buka, cari) must appear at the start of the
 * phrase; everything after the keyword becomes the argument.
 */
export function parseIntent(transcript: string, locale: Locale): Intent {
  const raw = transcript.trim();
  const text = raw.toLowerCase();

  for (const command of COMMANDS) {
    const keywords = command.keywords[locale] ?? command.keywords.en;
    for (const keyword of keywords) {
      const key = keyword.toLowerCase();
      if (command.captures) {
        if (text.startsWith(`${key} `)) {
          return { action: command.action, arg: raw.slice(key.length).trim(), raw };
        }
      } else if (text === key || text.includes(key)) {
        return { action: command.action, arg: "", raw };
      }
    }
  }

  return { action: "unknown", arg: "", raw };
}
