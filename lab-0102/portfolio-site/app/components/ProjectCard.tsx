interface ProjectCardProps {
  title: string; description: string; technologies: string[]; link?: string;
}

export default function ProjectCard({ title, description, technologies, link }: ProjectCardProps) {
  return (
    <div className="bg-white border rounded-xl p-6 hover:shadow-lg transition-all border-gray-200">
      <h3 className="text-xl font-bold mb-2 text-gray-800">{title}</h3>
      <p className="text-gray-600 mb-4 text-sm">{description}</p>
      <div className="flex flex-wrap gap-2 mb-4">
        {technologies.map(tech => (
          <span key={tech} className="bg-blue-50 text-blue-600 px-2 py-1 rounded text-xs font-medium">
            {tech}
          </span>
        ))}
      </div>
      {link && <a href={link} className="text-blue-600 font-semibold hover:text-blue-800 text-sm">Смотреть проект →</a>}
    </div>
  )
}