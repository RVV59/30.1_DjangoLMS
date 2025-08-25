import os
import ast
from pprint import pprint

INTERNAL_CLASSES = {'Meta', 'Manager', 'DoesNotExist'}
PROJECT_PATH = r'C:\Users\Vlad\PycharmProjects\30.1_DjangoLMS'

def get_layer(path):
    if 'models.py' in path:
        return 'Model'
    elif 'views.py' in path:
        return 'View'
    elif 'serializers.py' in path:
        return 'Serializer'
    elif 'tasks.py' in path:
        return 'Task'
    elif 'urls.py' in path:
        return 'URL'
    else:
        return 'Other'

def extract_calls(tree):
    calls = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr)
    return calls

def extract_structure(project_path):
    structure = {}
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read())
                        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                        funcs = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                        structure[full_path] = {
                            'layer': get_layer(full_path),
                            'classes': [c for c in classes if c not in INTERNAL_CLASSES],
                            'functions': funcs,
                            'calls': extract_calls(tree)
                        }
                except Exception as e:
                    print(f'❌ Ошибка в {full_path}: {e}')
    return structure

def build_edges(structure):
    edges = []
    name_to_layer = {}

    # Индексируем все классы и функции
    for path, data in structure.items():
        for cls in data['classes']:
            name_to_layer[cls] = data['layer']
        for func in data['functions']:
            name_to_layer[func] = data['layer']

    # Строим связи
    for path, data in structure.items():
        src_file = os.path.basename(path)
        src_layer = data['layer']
        for call in data['calls']:
            if call in name_to_layer:
                dst_layer = name_to_layer[call]
                edges.append((f'{src_layer}:{src_file}', f'{dst_layer}:{call}'))

        # Добавим базовые связи
        for cls in data['classes']:
            if src_layer == 'Model':
                edges.append((f'Model:{cls}', 'DB Table'))
        for func in data['functions']:
            if src_layer == 'View':
                edges.append((f'ViewFunc:{func}', 'HTTP Request'))

    return edges

def interactive_log(structure, edges):
    print("\n📦 Структура проекта:")
    for path, data in structure.items():
        print(f"\n📁 {path}")
        print(f"  🔹 Layer: {data['layer']}")
        print(f"  🧱 Classes: {data['classes']}")
        print(f"  🔧 Functions: {data['functions']}")
        print(f"  📞 Calls: {list(data['calls'])}")

    print("\n🔗 Построенные связи:")
    for src, dst in edges:
        print(f"  {src} → {dst}")

def main():
    if not os.path.exists(PROJECT_PATH):
        print(f"❌ Путь не найден: {PROJECT_PATH}")
        return

    structure = extract_structure(PROJECT_PATH)
    edges = build_edges(structure)
    interactive_log(structure, edges)

if __name__ == "__main__":
    main()