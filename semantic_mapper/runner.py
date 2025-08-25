from semantic_mapper.parser import extract_structure, build_edges
from semantic_mapper.visualizer import visualize
from semantic_mapper.export_mm import export_to_mm

project_path = r'C:\Users\Vlad\PycharmProjects\30.1_DjangoLMS\lms'

def main():
    structure = extract_structure(project_path)
    edges = build_edges(structure)

    print("\n📊 Найдено:")
    print(f"  🧱 Моделей: {sum(len(d['classes']) for d in structure.values() if d['layer'] == 'Model')}")
    print(f"  🔧 View-функций: {sum(len(d['functions']) for d in structure.values() if d['layer'] == 'View')}")
    print(f"  📦 Сериализаторов: {sum(len(d['classes']) for d in structure.values() if d['layer'] == 'Serializer')}")
    print(f"  ⚙️ Tasks: {sum(len(d['classes']) for d in structure.values() if d['layer'] == 'Task')}")
    print(f"  🛡 Permissions: {sum(len(d['classes']) for d in structure.values() if d['layer'] == 'Permission')}")

    visualize(edges)
    export_to_mm(edges)

if __name__ == "__main__":
    main()