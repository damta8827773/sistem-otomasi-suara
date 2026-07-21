"use client";

import { useCallback, useState } from "react";

/**
 * Lightweight toast/notification hook. Keeps an in-memory queue of transient
 * messages that auto-dismiss. UI is rendered by the consumer (e.g. a toast
 * container); this hook only owns state.
 */

export type NotifType = "info" | "success" | "error";

export interface Notif {
  id: number;
  type: NotifType;
  message: string;
}

let counter = 0;

export function useNotif(defaultTimeout = 3000) {
  const [notifs, setNotifs] = useState<Notif[]>([]);

  const dismiss = useCallback((id: number) => {
    setNotifs((prev) => prev.filter((n) => n.id !== id));
  }, []);

  const notify = useCallback(
    (message: string, type: NotifType = "info", timeout = defaultTimeout) => {
      const id = ++counter;
      setNotifs((prev) => [...prev, { id, type, message }]);
      if (timeout > 0) {
        setTimeout(() => dismiss(id), timeout);
      }
      return id;
    },
    [defaultTimeout, dismiss],
  );

  return {
    notifs,
    notify,
    dismiss,
    success: (m: string) => notify(m, "success"),
    error: (m: string) => notify(m, "error"),
    info: (m: string) => notify(m, "info"),
  };
}
