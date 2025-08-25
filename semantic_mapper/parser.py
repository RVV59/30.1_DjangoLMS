import os
import ast

INTERNAL_CLASSES = {'Meta', 'Manager', 'DoesNotExist'}

def get_layer(path):
    path = path.replace('\\', '/')
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
    elif 'permissions.py' in path:
        return 'Permission'
    elif 'services.py' in path:
        return 'Service'
    elif 'validators.py' in path:
        return 'Validator'
    elif 'paginators.py' in path:
        return 'Paginator'
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
        if 'migrations' in root.replace('\\', '/'):
            continue  # Пропускаем миграции
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read())
                        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                        calls = extract_calls(tree)
                        structure[full_path] = {
                            'layer': get_layer(full_path),
                            'classes': [c for c in classes if c not in INTERNAL_CLASSES],
                            'functions': functions,
                            'calls': calls
                        }
                except Exception as e:
                    print(f'❌ Ошибка в {full_path}: {e}')
    return structure

def build_edges(structure):
    edges = []
    name_to_layer = {}

    for path, data in structure.items():
        for cls in data['classes']:
            name_to_layer[cls] = data['layer']
        for func in data['functions']:
            name_to_layer[func] = data['layer']

    for path, data in structure.items():
        src_file = os.path.basename(path)
        src_layer = data['layer']
        for call in data['calls']:
            if call in name_to_layer:
                dst_layer = name_to_layer[call]
                edges.append((f'{src_layer}:{src_file}', f'{dst_layer}:{call}'))

        for cls in data['classes']:
            if src_layer == 'Model':
                edges.append((f'Model:{cls}', 'DB Table'))
        for func in data['functions']:
            if src_layer == 'View':
                edges.append((f'ViewFunc:{func}', 'HTTP Request'))

    return edges