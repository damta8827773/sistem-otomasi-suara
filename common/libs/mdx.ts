import fs from "node:fs/promises";
import path from "node:path";
import matter from "gray-matter";

/**
 * MDX content helpers. Blog posts live as .mdx files under /contents/blog and
 * carry frontmatter parsed by gray-matter. These run on the server only.
 */

const CONTENTS_DIR = path.join(process.cwd(), "contents", "blog");

export interface PostFrontmatter {
  title: string;
  date: string; // ISO
  summary: string;
  lang?: string;
  tags?: string[];
}

export interface PostMeta extends PostFrontmatter {
  slug: string;
}

export interface Post extends PostMeta {
  content: string; // raw MDX body
}

/** Return metadata for every post, newest first. */
export async function getAllPosts(): Promise<PostMeta[]> {
  let files: string[];
  try {
    files = await fs.readdir(CONTENTS_DIR);
  } catch {
    return []; // no contents directory yet
  }

  const posts: PostMeta[] = [];
  for (const file of files) {
    if (!file.endsWith(".mdx")) continue;
    const slug = file.replace(/\.mdx$/, "");
    const raw = await fs.readFile(path.join(CONTENTS_DIR, file), "utf8");
    const { data } = matter(raw);
    posts.push({ slug, ...(data as PostFrontmatter) });
  }

  return posts.sort((a, b) => (a.date < b.date ? 1 : -1));
}

/** Load a single post (frontmatter + body) by slug, or null if missing. */
export async function getPostBySlug(slug: string): Promise<Post | null> {
  try {
    const raw = await fs.readFile(path.join(CONTENTS_DIR, `${slug}.mdx`), "utf8");
    const { data, content } = matter(raw);
    return { slug, content, ...(data as PostFrontmatter) };
  } catch {
    return null;
  }
}
