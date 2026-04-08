export interface BlogPost {
  id: number; title: string; slug: string; excerpt: string; content: string; date: string; author: string;
}

export const blogPosts: BlogPost[] = [
  {
    id: 1,
    title: 'Введение в Next.js',
    slug: 'introduction-to-nextjs',
    excerpt: 'Основы Next.js и преимущества серверного рендеринга.',
    content: 'Next.js — это мощный фреймворк, который делает разработку на React еще быстрее...',
    date: '2026-04-01',
    author: 'Кирилл'
  },
  {
    id: 2,
    title: '3D моделирование для веба',
    slug: '3d-modeling-web',
    excerpt: 'Как использовать модели из Blender в браузерных приложениях.',
    content: 'Использование Three.js и React Three Fiber позволяет оживить интерфейсы...',
    date: '2026-04-05',
    author: 'Кирилл'
  },
  {
    id: 3,
    title: 'Почему кастомные клавиатуры — это круто',
    slug: 'custom-keyboards',
    excerpt: 'Разбор механики переключателей и строения корпусов.',
    content: 'От тактильных ощущений до звука — каждая деталь имеет значение...',
    date: '2026-04-06',
    author: 'Кирилл'
  }
];