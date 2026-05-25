import { notFound } from 'next/navigation'
import { blogPosts } from '../data'
import Link from 'next/link'

export async function generateStaticParams() {
  return blogPosts.map((post) => ({ slug: post.slug }))
}

// В Next.js 15 params — это Promise
export default async function BlogPostPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = blogPosts.find(p => p.slug === slug);
  
  if (!post) notFound();

  return (
    <article className="max-w-3xl mx-auto py-10">
      <Link href="/blog" className="text-blue-500 hover:underline mb-8 block">← Назад в блог</Link>
      <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
      <div className="flex gap-4 text-gray-500 mb-8 border-b pb-4">
        <span>{post.date}</span>
        <span>Автор: {post.author}</span>
      </div>
      <div className="prose lg:prose-xl text-gray-700 leading-relaxed">
        <p className="font-semibold text-lg mb-4">{post.excerpt}</p>
        <p>{post.content}</p>
      </div>
    </article>
  )
}