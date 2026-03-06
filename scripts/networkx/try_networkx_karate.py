import networkx as nx
import matplotlib.pyplot as plt


# Try to use Graphviz for a cleaner layout if available; fall back to spring_layout otherwise.
def get_layout(G):
    try:
        # Try PyGraphviz
        from networkx.drawing.nx_agraph import graphviz_layout

        return graphviz_layout(G, prog="dot")
    except Exception:
        try:
            # Try pydot
            from networkx.drawing.nx_pydot import graphviz_layout

            return graphviz_layout(G, prog="dot")
        except Exception:
            # Fallback: spring layout
            return nx.spring_layout(G, k=1.2, seed=42)


G = nx.DiGraph()

# Define nodes grouped by category
nodes = {
    # Authoring
    "Feature files (.feature)": "Authoring",
    "Reusable features (call/read)": "Authoring",
    "karate-config.js / properties": "Authoring",
    "Test data (JSON/CSV)": "Authoring",
    # Execution
    "Runner (CLI/JUnit5/Maven/Gradle)": "Execution",
    "Parallel runner": "Execution",
    # Runtime
    "Karate engine (DSL interpreter)": "Runtime",
    "JS engine": "Runtime",
    "Variable/context": "Runtime",
    "Assertions & matchers": "Runtime",
    # Protocols / IO
    "HTTP/REST/SOAP/GraphQL": "Protocols",
    "WebSocket": "Protocols",
    "UI driver (web)": "Protocols",
    "Mock server": "Protocols",
    # External
    "External systems/services": "External",
    # Reporting
    "Reports (HTML, JUnit, JSON)": "Reporting",
    "CI/CD": "Reporting",
}

# Add nodes with category attribute
for n, cat in nodes.items():
    G.add_node(n, category=cat)

# Define edges (u -> v) with optional labels
edges = [
    # Authoring to Execution
    ("Feature files (.feature)", "Runner (CLI/JUnit5/Maven/Gradle)", "execute"),
    ("karate-config.js / properties", "Runner (CLI/JUnit5/Maven/Gradle)", "configure"),
    ("Test data (JSON/CSV)", "Feature files (.feature)", "data-driven"),
    ("Reusable features (call/read)", "Feature files (.feature)", "reuse"),
    # Execution to Runtime
    ("Runner (CLI/JUnit5/Maven/Gradle)", "Parallel runner", "optional"),
    ("Runner (CLI/JUnit5/Maven/Gradle)", "Karate engine (DSL interpreter)", "invoke"),
    ("Parallel runner", "Karate engine (DSL interpreter)", "parallelize"),
    # Runtime internals
    ("Karate engine (DSL interpreter)", "JS engine", "script expressions"),
    ("Karate engine (DSL interpreter)", "Variable/context", "manage state"),
    # Engine to protocols
    ("Karate engine (DSL interpreter)", "HTTP/REST/SOAP/GraphQL", "call APIs"),
    ("Karate engine (DSL interpreter)", "WebSocket", "send/receive"),
    ("Karate engine (DSL interpreter)", "UI driver (web)", "drive UI"),
    ("Karate engine (DSL interpreter)", "Mock server", "start/stub"),
    # Protocols to external systems
    ("HTTP/REST/SOAP/GraphQL", "External systems/services", "requests"),
    ("WebSocket", "External systems/services", "messages"),
    ("UI driver (web)", "External systems/services", "browser/app"),
    ("Mock server", "External systems/services", "simulate"),
    # Responses flowing back to engine
    ("External systems/services", "Karate engine (DSL interpreter)", "responses"),
    # Assertions and reporting
    ("Karate engine (DSL interpreter)", "Assertions & matchers", "verify"),
    ("Assertions & matchers", "Reports (HTML, JUnit, JSON)", "results"),
    ("Karate engine (DSL interpreter)", "Reports (HTML, JUnit, JSON)", "runtime logs"),
    ("Reports (HTML, JUnit, JSON)", "CI/CD", "publish"),
]

# Add edges to graph
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

# Build color list for nodes
node_colors = [category_colors[G.nodes[n]["category"]] for n in G.nodes()]

# Compute layout
pos = get_layout(G)

plt.figure(figsize=(14, 10))
# Draw nodes
nx.draw_networkx_nodes(
    G,
    pos,
    node_color=node_colors,
    node_size=1600,
    alpha=0.9,
    linewidths=1.2,
    edgecolors="black",
)
# Draw edges
nx.draw_networkx_edges(
    G,
    pos,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=16,
    width=1.2,
    connectionstyle="arc3,rad=0.06",
)
# Draw labels
nx.draw_networkx_labels(G, pos, font_size=9, font_color="white")

# Draw a subset of edge labels to reduce clutter
important_edge_labels = {
    (u, v): d["label"]
    for u, v, d in G.edges(data=True)
    if d["label"]
    in {
        "execute",
        "invoke",
        "parallelize",
        "call APIs",
        "start/stub",
        "verify",
        "results",
        "publish",
    }
}
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=important_edge_labels, font_size=8, label_pos=0.5, rotate=False
)

# Legend
import matplotlib.patches as mpatches

legend_patches = [
    mpatches.Patch(color=col, label=cat) for cat, col in category_colors.items()
]
plt.legend(
    handles=legend_patches,
    loc="lower center",
    ncol=3,
    bbox_to_anchor=(0.5, -0.05),
    frameon=False,
)

plt.title("How the Karate Test Framework Works (High-Level Flow)", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.show()
