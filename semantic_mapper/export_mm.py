import xml.etree.ElementTree as ET
from collections import defaultdict

def create_root_node():
    map_elem = ET.Element('map', version='0.9.0')
    root_node = ET.SubElement(map_elem, 'node', TEXT='Semantic Map')
    return map_elem, root_node

def group_edges(edges):
    grouped = defaultdict(list)
    for src, dst in edges:
        src_layer, src_name = src.split(':', 1)
        grouped[src_layer].append((src_name, dst))
    return grouped

def add_nodes(parent, items):
    for src, dst in items:
        src_node = ET.SubElement(parent, 'node', TEXT=src)
        ET.SubElement(src_node, 'node', TEXT=f'→ {dst}')

def export_to_mm(edges, output_path='semantic_map.mm'):
    map_elem, root_node = create_root_node()
    grouped = group_edges(edges)

    for layer, items in grouped.items():
        layer_node = ET.SubElement(root_node, 'node', TEXT=layer)
        add_nodes(layer_node, items)

    tree = ET.ElementTree(map_elem)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f'✅ Экспорт завершён: {output_path}')