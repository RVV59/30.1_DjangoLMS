from graphviz import Digraph
import subprocess

def visualize(edges, output='semantic_map'):
    dot = Digraph(comment='Semantic Map', format='png')
    dot.attr(rankdir='LR', size='10')

    for src, dst in edges:
        dot.edge(src, dst)

    filepath = dot.render(output, view=False)
    subprocess.run(['start', filepath], shell=True)