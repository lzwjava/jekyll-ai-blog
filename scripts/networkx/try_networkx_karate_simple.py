import networkx as nx
import matplotlib.pyplot as plt


# Minimal, readable layout (Graphviz if available, else spring)
def get_layout(G):
    return nx.spring_layout(G, k=1.2, seed=42)


G = nx.DiGraph()

# Keep only essential nodes so the flow is easy to grasp
nodes = {
    # Authoring
    "Feature files (.feature)": "Authoring",
    # Execution
    "Runner (CLI/JUnit5/Maven/Gradle)": "Execution",
    # Runtime
    "Karate engine (DSL interpreter)": "Runtime",
    "Assertions & matchers": "Runtime",
    # Protocols / IO
    "HTTP/REST/GraphQL": "Protocols",
    # External
    "External systems/services": "External",
    # Reporting
    "Reports (HTML, JUnit, JSON)": "Reporting",
    "CI/CD": "Reporting",
}

# Add nodes with category attribute
for n, cat in nodes.items():
    G.add_node(n, category=cat)

# Essential edges: straight-through path from authoring to reporting
edges = [
    ("Feature files (.feature)", "Runner (CLI/JUnit5/Maven/Gradle)", "execute"),
    ("Runner (CLI/JUnit5/Maven/Gradle)", "Karate engine (DSL interpreter)", "invoke"),
    ("Karate engine (DSL interpreter)", "HTTP/REST/GraphQL", "call APIs"),
    ("HTTP/REST/GraphQL", "External systems/services", "requests"),
    ("External systems/services", "Karate engine (DSL interpreter)", "responses"),
    ("Karate engine (DSL interpreter)", "Assertions & matchers", "verify"),
    ("Assertions & matchers", "Reports (HTML, JUnit, JSON)", "results"),
    ("Reports (HTML, JUnit, JSON)", "CI/CD", "publish"),
]

for u, v, label in edges:
    G.add_edge(u, v, label=label)

# Colors per category
category_colors = {
    "Authoring": "#4C78A8",
    "Execution": "#F58518",
    "Runtime": "#B279A2",
    "Protocols": "#54A24B",
    "External": "#9A9A9A",
    "Reporting": "#E45756",
}

node_colors = [category_colors[G.nodes[n]["category"]] for n in G.nodes()]
pos = get_layout(G)

# Use dark mode: black background, light edges/text
plt.figure(figsize=(12, 8), facecolor="black")
ax = plt.gca()
ax.set_facecolor("black")
nx.draw_networkx_nodes(
    G,
    pos,
    node_color=node_colors,
    node_size=1400,
    alpha=0.95,
    linewidths=1.2,
    edgecolors="white",
)
nx.draw_networkx_edges(
    G,
    pos,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=16,
    width=1.2,
    connectionstyle="arc3,rad=0.06",
    edge_color="#CCCCCC",
    alpha=0.85,
)
nx.draw_networkx_labels(
    G,
    pos,
    font_size=9,
    font_color="white",
    font_weight="bold",
    bbox=dict(
        facecolor="black",
        edgecolor="white",
        boxstyle="round,pad=0.25",
        linewidth=0.8,
        alpha=0.95,
    ),
)

# Show all edge labels (few enough to be readable)
edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    font_size=8,
    label_pos=0.5,
    rotate=False,
    font_color="#FFFFFF",
    font_weight="bold",
    bbox=dict(
        facecolor="black",
        edgecolor="white",
        boxstyle="round,pad=0.15",
        linewidth=0.6,
        alpha=0.95,
    ),
)

import matplotlib.patches as mpatches

legend_patches = [
    mpatches.Patch(color=col, label=cat) for cat, col in category_colors.items()
]
legend = plt.legend(
    handles=legend_patches,
    loc="lower center",
    ncol=3,
    bbox_to_anchor=(0.5, -0.08),
    frameon=False,
)
# Make legend labels white for dark background
for text in legend.get_texts():
    text.set_color("white")
    text.set_weight("bold")

plt.title("Karate Framework — Minimal Flow", fontsize=14, color="white", weight="bold")
plt.axis("off")
plt.tight_layout()

# Save to tmp directory instead of showing interactively
import os

os.makedirs("tmp", exist_ok=True)
output_path = os.path.join("tmp", "karate_framework_minimal_flow.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="black")
print(f"Saved figure to {output_path}")
