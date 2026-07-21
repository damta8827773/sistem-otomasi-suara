import { useTranslations } from "next-intl";
import { Link } from "@/i18n/routing";
import type { PostMeta } from "@/common/libs/mdx";

export function BlogList({ posts }: { posts: PostMeta[] }) {
  const t = useTranslations("blog");

  return (
    <section>
      <h1 className="text-3xl font-bold">{t("title")}</h1>
      <p className="mt-2 text-black/60 dark:text-white/60">{t("description")}</p>

      {posts.length === 0 ? (
        <p className="mt-8 text-black/60 dark:text-white/60">{t("empty")}</p>
      ) : (
        <ul className="mt-8 space-y-6">
          {posts.map((post) => (
            <li key={post.slug}>
              <Link href={`/blog/${post.slug}`} className="group block">
                <h2 className="text-xl font-semibold group-hover:underline">
                  {post.title}
                </h2>
                <time className="text-sm text-black/50 dark:text-white/50">
                  {new Date(post.date).toLocaleDateString()}
                </time>
                <p className="mt-1 text-black/70 dark:text-white/70">{post.summary}</p>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
