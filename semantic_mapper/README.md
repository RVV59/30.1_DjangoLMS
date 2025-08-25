Semantic Mapper v0.2 — визуализация архитектуры Django-проекта

🔧 Запуск:
- Через PyCharm: External Tools → Semantic Mapper
- Или вручную: python semantic_mapper/runner.py

📦 Что делает:
- Сканирует проект
- Извлекает классы и функции
- Строит связи между слоями: Model, View, Serializer, Task, URL
- Визуализирует через Graphviz
- Открывает semantic_map.png автоматически

📁 Расширения:
- Поддержка ForeignKey, ManyToManyField (в разработке)
- Экспорт в .mm для Mind Map 2008
- AI-аннотация узлов (в планах)

👨‍🏫 Подходит для:
- Преподавателей, студентов, архитекторов
- Визуального анализа и документации