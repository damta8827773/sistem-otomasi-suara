"use client";

import { useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { useNotif } from "@/hooks/useNotif";
import { getComments, postComment, type Comment } from "@/services/comment";

/**
 * Comment system for a blog post ("Tanya / komentar"). Client component: it
 * fetches existing comments, lets a visitor submit a new one, and surfaces
 * success/error via the useNotif toast hook.
 */
export function CommentSection({ slug }: { slug: string }) {
  const t = useTranslations("comment");
  const { notifs, success, error } = useNotif();

  const [comments, setComments] = useState<Comment[]>([]);
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");
  const [sending, setSending] = useState(false);

  useEffect(() => {
    let active = true;
    getComments(slug)
      .then((data) => active && setComments(data))
      .catch(() => active && error(t("error")));
    return () => {
      active = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [slug]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!message.trim()) return;
    setSending(true);
    try {
      const created = await postComment({ slug, name: name.trim() || "Anon", message });
      setComments((prev) => [...prev, created]);
      setMessage("");
      success(t("success"));
    } catch {
      error(t("error"));
    } finally {
      setSending(false);
    }
  }

  return (
    <section className="mt-16 border-t border-black/10 pt-8 dark:border-white/10">
      <h2 className="text-xl font-semibold">{t("title")}</h2>

      <ul className="mt-6 space-y-4">
        {comments.length === 0 ? (
          <li className="text-black/60 dark:text-white/60">{t("empty")}</li>
        ) : (
          comments.map((c) => (
            <li key={c.id} className="rounded-md bg-black/5 p-3 dark:bg-white/5">
              <div className="text-sm font-medium">{c.name}</div>
              <p className="text-black/80 dark:text-white/80">{c.message}</p>
            </li>
          ))
        )}
      </ul>

      <form onSubmit={handleSubmit} className="mt-6 space-y-3">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder={t("namePlaceholder")}
          className="w-full rounded-md border border-black/15 bg-transparent px-3 py-2 text-sm dark:border-white/15"
        />
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder={t("placeholder")}
          rows={3}
          className="w-full rounded-md border border-black/15 bg-transparent px-3 py-2 text-sm dark:border-white/15"
        />
        <button
          type="submit"
          disabled={sending}
          className="rounded-md border border-black/20 px-4 py-2 text-sm font-medium hover:bg-black/5 disabled:opacity-50 dark:border-white/20 dark:hover:bg-white/5"
        >
          {sending ? t("sending") : t("submit")}
        </button>
      </form>

      {/* Minimal inline toast rendering driven by useNotif. */}
      <div className="mt-4 space-y-2" role="status" aria-live="polite">
        {notifs.map((n) => (
          <div
            key={n.id}
            className={
              n.type === "error"
                ? "text-sm text-red-600 dark:text-red-400"
                : "text-sm text-green-600 dark:text-green-400"
            }
          >
            {n.message}
          </div>
        ))}
      </div>
    </section>
  );
}
