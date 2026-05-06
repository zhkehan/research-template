# research-template

Project scaffolding templates for data pipeline and academic research projects.

## Branches

| Branch | Type | Description |
|--------|------|-------------|
| `data-pipeline` | Data pipeline | Source data → Parquet → DuckDB |
| `academic` | Academic research | Code, results, writing |

## Usage

```bash
# Data pipeline project
git clone --branch data-pipeline --single-branch https://github.com/zhkehan/research-template.git MyProject
cd MyProject
python setup.py --name MyProject --root "C:\path\to\MyProject" --datasets "TableA, TableB"

# Academic project
git clone --branch academic --single-branch https://github.com/zhkehan/research-template.git MyPaper
cd MyPaper
python setup.py --name MyPaper --root "C:\path\to\MyPaper"
```

After setup, `setup.py` removes itself.

## What's Included

### data-pipeline branch
- `config.py` — centralized paths and manifests
- `scripts/` — conversion, validation, DuckDB build scripts
- `.claude/` — hooks, rules, agents for Claude Code
- `PLAN.md`, `CLAUDE.md`, `requirements.txt`

### academic branch
- `code/` — data preparation and analysis scripts
- `.claude/` — hooks, rules, agents for Claude Code
- `PROJECT.md`, `CLAUDE.md`, `.gitignore`
