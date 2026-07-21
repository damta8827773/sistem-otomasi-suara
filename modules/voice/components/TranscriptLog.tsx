export interface LogEntry {
  id: number;
  transcript: string;
  result: string;
  ok: boolean;
}

/** Read-only list of recognized commands and their spoken results. */
export function TranscriptLog({
  entries,
  emptyLabel,
}: {
  entries: LogEntry[];
  emptyLabel: string;
}) {
  if (entries.length === 0) {
    return <p className="text-sm text-black/50 dark:text-white/50">{emptyLabel}</p>;
  }

  return (
    <ul className="w-full max-w-md space-y-2">
      {entries.map((entry) => (
        <li
          key={entry.id}
          className="rounded-lg border border-black/10 p-3 text-left dark:border-white/10"
        >
          <p className="text-sm font-medium">&ldquo;{entry.transcript}&rdquo;</p>
          <p
            className={
              entry.ok
                ? "text-sm text-green-600 dark:text-green-400"
                : "text-sm text-red-600 dark:text-red-400"
            }
          >
            {entry.result}
          </p>
        </li>
      ))}
    </ul>
  );
}
