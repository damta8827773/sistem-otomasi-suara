/**
 * Comment service — data access for the blog comment system.
 *
 * This layer is framework-agnostic (no React). Swap the in-memory stub for a
 * real backend (database, API route, or a headless CMS) without touching the
 * UI in modules/comment.
 */

export interface Comment {
  id: string;
  slug: string;
  name: string;
  message: string;
  createdAt: string; // ISO
}

export interface NewComment {
  slug: string;
  name: string;
  message: string;
}

const API_BASE = "/api/comments";

/** Fetch comments for a post. */
export async function getComments(slug: string): Promise<Comment[]> {
  const res = await fetch(`${API_BASE}?slug=${encodeURIComponent(slug)}`, {
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`Failed to load comments (${res.status})`);
  return (await res.json()) as Comment[];
}

/** Submit a new comment; returns the persisted record. */
export async function postComment(input: NewComment): Promise<Comment> {
  const res = await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!res.ok) throw new Error(`Failed to post comment (${res.status})`);
  return (await res.json()) as Comment;
}
