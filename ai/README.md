# Setup

    export COMPONENT_LIBRARY_ROOT=/path/to/your/reflex/project

Root dir directly containing your real `components/`, `docs/`, and
`native/lib/` folders.

    pip install -r requirements.txt
    python3 build_manifest.py         # docs/**/*.md (with prop tables) -> manifest.json
    python3 build_chart_manifest.py   # docs/charts/*.md -> chart_manifest.json
    python3 mine_patterns.py          # native/lib/**/*.py -> patterns.json
    export ANTHROPIC_API_KEY=...      # or OPENAI_API_KEY / GEMINI_API_KEY
    python3 cli.py [anthropic|openai|gemini]

## Two kinds of doc content

- `build_manifest.py` expects a `# API Reference` section with `## name` +
  a prop table — this is for real parameterized components (button, card, ...).
- `build_chart_manifest.py` expects frontmatter (title/description) + repeated
  `## Label` / `--DEMO(function_name)--` pairs, no prop table — this is for
  charts and any other doc category that's really a set of complete, non-
  parameterized example functions rather than a reusable component with props.
  If you add a new doc category shaped like this, it needs its own manifest
  builder (copy build_chart_manifest.py), not a hack bolted onto build_manifest.py.
