"use client";

import { useCallback, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { useSpeechRecognition } from "@/hooks/useSpeechRecognition";
import { parseIntent } from "@/common/libs/intent";
import { executeIntent } from "@/services/automation";
import type { Locale } from "@/i18n/routing";
import { TranscriptLog, type LogEntry } from "./TranscriptLog";

/**
 * The entire user interface: a microphone button, live status, and a log of
 * recognized commands. Input is voice only. Pressing the button just grants
 * permission and starts or stops listening.
 */
export function VoiceControl() {
  const t = useTranslations("voice");
  const locale = useLocale() as Locale;
  const lang = locale === "id" ? "id-ID" : "en-US";

  const [log, setLog] = useState<LogEntry[]>([]);

  const handleFinal = useCallback(
    (transcript: string) => {
      const intent = parseIntent(transcript, locale);
      const result = executeIntent(intent, locale);
      setLog((prev) =>
        [{ id: Date.now(), transcript, result: result.message, ok: result.ok }, ...prev].slice(0, 20),
      );
    },
    [locale],
  );

  const { supported, listening, interim, error, start, stop } = useSpeechRecognition({
    lang,
    onFinal: handleFinal,
  });

  if (!supported) {
    return (
      <p className="max-w-md rounded-lg border border-amber-400/40 bg-amber-50 p-4 text-sm text-amber-800 dark:bg-amber-950/40 dark:text-amber-200">
        {t("unsupported")}
      </p>
    );
  }

  return (
    <div className="flex w-full flex-col items-center gap-6">
      <button
        type="button"
        onClick={listening ? stop : start}
        aria-pressed={listening}
        aria-label={listening ? t("stop") : t("start")}
        className={`flex h-24 w-24 items-center justify-center rounded-full border transition ${
          listening
            ? "mic-listening border-red-500 bg-red-500 text-white"
            : "border-black/15 bg-black/5 text-black hover:bg-black/10 dark:border-white/15 dark:bg-white/10 dark:text-white dark:hover:bg-white/20"
        }`}
      >
        <MicIcon />
      </button>

      <p className="text-sm font-medium">{listening ? t("listening") : t("idle")}</p>

      <p className="min-h-6 max-w-md text-center text-lg text-black/70 dark:text-white/70">
        {interim || (log[0]?.transcript ?? "")}
      </p>

      {error && (
        <p className="text-sm text-red-600 dark:text-red-400">
          {t("error")}: {error}
        </p>
      )}

      <TranscriptLog entries={log} emptyLabel={t("empty")} />

      <details className="w-full max-w-md text-sm text-black/60 dark:text-white/60">
        <summary className="cursor-pointer font-medium">{t("commandsTitle")}</summary>
        <p className="mt-2 leading-6">{t("commands")}</p>
      </details>
    </div>
  );
}

function MicIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="32"
      height="32"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
      <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
      <line x1="12" y1="19" x2="12" y2="22" />
    </svg>
  );
}
