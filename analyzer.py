import ast, math, re
from pathlib import Path
from collections import Counter

IGNORE_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules"}

def analyze_python_file(path):
    source = path.read_text(encoding="utf-8", errors="replace")
    lines = source.splitlines()
    nonblank = [line for line in lines if line.strip()]
    comments = [line for line in lines if line.lstrip().startswith("#")]
    functions, classes, long_functions = [], [], []
    complexity = 1
    smells = []
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node.name)
                if (node.end_lineno or node.lineno) - node.lineno + 1 > 40:
                    long_functions.append(node.name)
                    smells.append(f"Long function: {node.name}")
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While,
                                   ast.Try, ast.With, ast.AsyncWith, ast.ExceptHandler,
                                   ast.comprehension)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += max(0, len(node.values) - 1)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                if len(methods) > 15:
                    smells.append(f"Large class: {node.name}")
    except SyntaxError as exc:
        smells.append(f"Syntax issue near line {exc.lineno or '?'}")
    normalized = [re.sub(r"\s+", " ", line.strip()) for line in nonblank
                  if len(line.strip()) > 15]
    duplicates = len(normalized) - len(set(normalized))
    if duplicates:
        smells.append(f"Repeated non-trivial lines: {duplicates}")
    if len(nonblank) > 300:
        smells.append("Large source file")
    if comments and len(comments) / max(1, len(nonblank)) < 0.03:
        smells.append("Low comment ratio")
    return {
        "file": path.name,
        "path": str(path),
        "lines": len(lines),
        "nonblank": len(nonblank),
        "complexity": complexity,
        "functions": len(functions),
        "classes": len(classes),
        "long_functions": long_functions,
        "duplicates": duplicates,
        "smells": smells,
    }

def risk_score(item):
    # Transparent heuristic score (0–100), not a trained model.
    score = min(30, item["complexity"] * 2)
    score += min(20, item["lines"] / 15)
    score += min(20, item["duplicates"] * 5)
    score += min(20, len(item["long_functions"]) * 8)
    score += min(10, len(item["smells"]) * 2)
    return round(min(100, score), 1)

def analyze_project(root):
    paths = []
    for path in root.rglob("*.py"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        paths.append(path)
    results = []
    for path in paths:
        item = analyze_python_file(path)
        item["path"] = str(path.relative_to(root))
        item["risk"] = risk_score(item)
        item["severity"] = "High" if item["risk"] >= 60 else "Medium" if item["risk"] >= 30 else "Low"
        item["recommendations"] = []
        if item["complexity"] > 10:
            item["recommendations"].append("Split complex logic into smaller functions and simplify branching.")
        if item["long_functions"]:
            item["recommendations"].append("Break long functions into focused, testable units.")
        if item["duplicates"]:
            item["recommendations"].append("Extract repeated logic into reusable functions.")
        if item["smells"]:
            item["recommendations"].append("Review detected code smells and add focused tests or documentation.")
        if not item["recommendations"]:
            item["recommendations"].append("Keep the module covered by tests and review changes regularly.")
        results.append(item)
    results.sort(key=lambda x: x["risk"], reverse=True)
    total = len(results)
    avg = round(sum(x["risk"] for x in results) / total, 1) if total else 0
    return {
        "summary": {
            "files_scanned": total,
            "average_risk": avg,
            "high_risk": sum(x["severity"] == "High" for x in results),
            "medium_risk": sum(x["severity"] == "Medium" for x in results),
            "low_risk": sum(x["severity"] == "Low" for x in results),
            "total_lines": sum(x["lines"] for x in results)
        },
        "files": results,
        "notice": "Prototype analysis: Python AST metrics and transparent heuristic risk scoring. It does not train a machine-learning model or inspect Git history/dependencies."
    }
