"""Собирает единый набор business-plugins: наши плагины + копии плагинов Anthropic.

1. Копирует установленные версии плагинов из кэша Claude Code в plugins/.
2. Переписывает .claude-plugin/marketplace.json под весь набор.
3. Кладёт в dist/ архивы:
   - business-plugins.zip — весь маркетплейс (для Claude Code);
   - claude-app/<плагин>.zip — по архиву на плагин (для загрузки в приложение Claude).

Запуск: python tools/build_bundle.py
"""
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = Path.home() / ".claude" / "plugins" / "cache" / "knowledge-work-plugins"
UPSTREAM = "https://github.com/anthropics/knowledge-work-plugins"

# Плагины Anthropic, которые входят в набор: имя -> категория.
ANTHROPIC = {
    "small-business": "business",
    "sales": "business",
    "marketing": "marketing",
    "brand-voice": "marketing",
    "finance": "finance",
    "legal": "legal",
    "product-management": "product",
    "design": "design",
    "productivity": "productivity",
    "enterprise-search": "productivity",
}
OWN = {"idea-council": "productivity"}

SKIP = {".in_use", ".git", "__pycache__"}


def latest(plugin_dir: Path) -> Path:
    versions = [p for p in plugin_dir.iterdir() if p.is_dir()]
    return max(versions, key=lambda p: p.stat().st_mtime)


def copy_anthropic():
    for name in ANTHROPIC:
        src = latest(CACHE / name)
        dst = ROOT / "plugins" / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=lambda d, names: [n for n in names if n in SKIP])
        print(f"  {name} {src.name}")


def manifest(name: str) -> dict:
    return json.loads((ROOT / "plugins" / name / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))


def write_marketplace():
    plugins = []
    for name, category in {**OWN, **ANTHROPIC}.items():
        m = manifest(name)
        entry = {
            "name": name,
            "description": m.get("description", ""),
            "version": m.get("version", "0.1.0"),
            "source": f"./plugins/{name}",
            "category": category,
        }
        if name in ANTHROPIC:
            entry["author"] = {"name": "Anthropic"}
            entry["homepage"] = f"{UPSTREAM}/tree/main/{name}"
        plugins.append(entry)
    path = ROOT / ".claude-plugin" / "marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["plugins"] = plugins
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def zip_dir(src: Path, target: Path, prefix: str = ""):
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(src.rglob("*")):
            rel = f.relative_to(src)
            if f.is_file() and not set(rel.parts) & (SKIP | {"dist"}):
                z.write(f, Path(prefix) / rel)


def build_dist():
    dist = ROOT / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    for name in {**OWN, **ANTHROPIC}:
        zip_dir(ROOT / "plugins" / name, dist / "claude-app" / f"{name}.zip")
    # Общий архив: маркетплейс + архивы для приложения в dist/claude-app.
    zip_dir(ROOT, dist / "business-plugins.zip", "business-plugins")
    with zipfile.ZipFile(dist / "business-plugins.zip", "a", zipfile.ZIP_DEFLATED) as z:
        for f in sorted((dist / "claude-app").glob("*.zip")):
            z.write(f, Path("business-plugins") / "dist" / "claude-app" / f.name)
    for f in sorted(dist.rglob("*.zip")):
        print(f"  {f.relative_to(ROOT)}  {f.stat().st_size // 1024} КБ")


if __name__ == "__main__":
    print("Копирую плагины Anthropic:")
    copy_anthropic()
    write_marketplace()
    print("Архивы:")
    build_dist()
