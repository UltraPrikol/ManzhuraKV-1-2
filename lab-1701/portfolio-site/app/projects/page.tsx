import ProjectCard from '../components/ProjectCard'

const projects = [
  {
    title: 'Keyboard Simulator',
    description: 'Симулятор сборки механических клавиатур на Unreal Engine 5.',
    technologies: ['C++', 'UE5', '3D Design'],
  },
  {
    title: 'Ultra-light Mouse Shell',
    description: 'Дизайн облегченного корпуса для мыши с Voronoi-паттерном.',
    technologies: ['Fusion 360', 'SLA Printing', 'Blender'],
  }
];

export default function ProjectsPage() {
  return (
    <div className="py-8">
      <h1 className="text-3xl font-bold mb-8">Мои проекты</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {projects.map(p => <ProjectCard key={p.title} {...p} />)}
      </div>
    </div>
  )
}