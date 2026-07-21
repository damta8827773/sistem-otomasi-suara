import { NextResponse } from "next/server";
import type { Comment, NewComment } from "@/services/comment";

/**
 * Comment API — in-memory stub so the UI works end-to-end in development.
 * Replace the `store` with a real database (e.g. Postgres, SQLite, or a
 * headless CMS) for production. Kept in app/api to stay 100% within Next.
 */
const store: Comment[] = [];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const slug = searchParams.get("slug");
  const items = slug ? store.filter((c) => c.slug === slug) : store;
  return NextResponse.json(items);
}

export async function POST(request: Request) {
  const body = (await request.json()) as Partial<NewComment>;

  if (!body.slug || !body.message?.trim()) {
    return NextResponse.json({ error: "slug and message are required" }, { status: 400 });
  }

  const comment: Comment = {
    id: crypto.randomUUID(),
    slug: body.slug,
    name: (body.name || "Anon").slice(0, 80),
    message: body.message.slice(0, 2000),
    createdAt: new Date().toISOString(),
  };
  store.push(comment);

  return NextResponse.json(comment, { status: 201 });
}
