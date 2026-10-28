"""Export the agent's state machine diagram.

  python diagram.py      # writes docs/state_machine.mmd (+ .png via mermaid.ink)

The Mermaid source is generated from the compiled LangGraph, so it always
matches the code. PNG rendering calls the public mermaid.ink API; if that is
unreachable the .mmd file is still written (GitHub renders Mermaid natively).
"""

from __future__ import annotations

import os

from matching_agent import build_graph

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(BASE_DIR, "docs")


def main() -> None:
    os.makedirs(DOCS, exist_ok=True)
    graph = build_graph().get_graph()
    mmd = graph.draw_mermaid()
    with open(os.path.join(DOCS, "state_machine.mmd"), "w", encoding="utf-8") as f:
        f.write(mmd)
    print("wrote docs/state_machine.mmd")
    try:
        png = graph.draw_mermaid_png()
        with open(os.path.join(DOCS, "state_machine.png"), "wb") as f:
            f.write(png)
        print("wrote docs/state_machine.png")
    except Exception as e:
        print(f"PNG render skipped ({type(e).__name__}: {e})")


if __name__ == "__main__":
    main()
