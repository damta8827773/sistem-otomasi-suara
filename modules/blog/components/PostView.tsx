import { MDXRemote } from "next-mdx-remote/rsc";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/routing";
import type { Post } from "@/common/libs/mdx";

/**
 * Renders a single post. The MDX body is compiled on the server via the RSC
 * MDXRemote entry point (no client bundle for content).
 */
export function PostView({ post }: { post: Post }) {
  const t = useTranslations("blog");

  return (
    <div>
      <header className="mb-8">
        <h1 className="text-3xl font-bold">{post.title}</h1>
        <time className="text-sm text-black/50 dark:text-white/50">
          {new Date(post.date).toLocaleDateString()}
        </time>
      </header>

      <div className="prose dark:prose-invert">
        <MDXRemote source={post.content} />
      </div>

      <Link
        href="/blog"
        className="mt-10 inline-block text-sm underline underline-offset-2"
      >
        ← {t("backToList")}
      </Link>
    </div>
  );
}
