export default function AboutPage() {
  const skills = ["React & Next.js", "TypeScript", "Tailwind CSS", "3D Modeling (Blender/Fusion 360)", "C++ & Python"];

  return (
    <div className="max-w-3xl mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Обо мне</h1>
      
      <div className="bg-white p-6 rounded-xl shadow-md mb-6 border border-gray-100">
        <h2 className="text-xl font-semibold mb-4 text-blue-600">Навыки</h2>
        <ul className="grid grid-cols-2 gap-2">
          {skills.map(skill => (
            <li key={skill} className="flex items-center gap-2 text-gray-700">
              <span className="text-blue-500">✔</span> {skill}
            </li>
          ))}
        </ul>
      </div>
      
      <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100">
        <h2 className="text-xl font-semibold mb-4 text-blue-600">Опыт и образование</h2>
        <div className="space-y-6">
          <div className="border-l-4 border-blue-500 pl-4">
            <h3 className="font-bold">Студент СКФУ</h3>
            <p className="text-sm text-gray-500">2024 — Настоящее время</p>
            <p className="text-gray-600 mt-1">Прикладная информатика</p>
          </div>
          <div className="border-l-4 border-gray-300 pl-4">
            <h3 className="font-bold">Разработчик-энтузиаст</h3>
            <p className="text-sm text-gray-500">Личные проекты</p>
            <p className="text-gray-600 mt-1">Проектирование кастомных механических клавиатур и 3D-печать корпусов.</p>
          </div>
        </div>
      </div>
    </div>
  )
}