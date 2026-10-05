"""
tools/LLM_sync_dev_prompts.py
=============================
Parses JOURNAL.md to extract Jim's direct steering prompts, agent errors/corrections,
and architectural milestones, generating a structured JSON dataset in content/data/dev-prompts.json.

Honors Jim's authoring architecture:
- content/pages/prompt-history.md remains clean pure Markdown for Obsidian.
- Development Prompts dataset is saved to content/data/dev-prompts.json.
- Jinja2 template (theme/templates/prompt-history.html) renders the chat threads during Pelican build.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
JOURNAL_PATH = REPO_ROOT / "JOURNAL.md"
DEV_PROMPTS_JSON = REPO_ROOT / "content" / "data" / "dev-prompts.json"


def parse_journal() -> tuple[list[dict], int]:
    """Parse JOURNAL.md and return structured milestone entries and total prompt count."""
    text = JOURNAL_PATH.read_text(encoding="utf-8")
    
    # Split by section headers (## YYYY-MM-DD ...)
    raw_sections = re.split(r"\n(?=## \d{4}-\d{2}-\d{2})", text)
    milestones = []
    total_prompt_count = 0

    for sec in raw_sections:
        if not sec.strip().startswith("## "):
            continue

        lines = [l for l in sec.strip().split("\n") if l.strip()]
        header_line = lines[0].replace("## ", "").strip()

        # Extract title and date
        header_match = re.match(r"^(\d{4}-\d{2}-\d{2})\s*[—–-]\s*(.*)$", header_line)
        if header_match:
            date_str, title_str = header_match.groups()
        else:
            date_str, title_str = "", header_line

        # Extract Jim's prompts
        prompts = []
        prompt_block_match = re.search(
            r">\s*\[!NOTE\]\s*Jim'?s?\s*(?:Prompts|Instructions|Guidance|Steering)[^\n]*\n((?:>[^\n]*\n?)+)",
            sec,
            re.IGNORECASE
        )
        if prompt_block_match:
            block = prompt_block_match.group(1)
            bullet_prompts = re.findall(r'>\s*-\s*\*(?:""|")?(.*?)(?:""|")?\*(?:\s*|$)', block, re.DOTALL)
            if bullet_prompts:
                for bp in bullet_prompts:
                    cleaned = bp.strip().strip('"').strip()
                    if cleaned:
                        prompts.append(cleaned)
            else:
                quotes = re.findall(r'"([^"\n]{10,})"', block)
                for q in quotes:
                    prompts.append(q.strip())

        if not prompts:
            continue

        total_prompt_count += len(prompts)

        # Extract AI response actions
        actions = []
        action_matches = re.findall(r'^\d+\.\s+\*\*(.*?)\*\*:\s*(.*)$', sec, re.MULTILINE)
        if action_matches:
            for act_title, act_desc in action_matches:
                actions.append(f"{act_title}: {act_desc}")

        milestones.append({
            "date": date_str,
            "title": title_str,
            "prompts": prompts,
            "actions": actions,
        })

    return milestones, total_prompt_count


def format_date(date_str: str) -> str:
    """Format YYYY-MM-DD as 'Sept DD YYYY'."""
    if not date_str:
        return ""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    try:
        parts = date_str.split("-")
        if len(parts) == 3:
            y, m, d = parts
            return f"{months[int(m)-1]} {int(d)} {y}"
    except Exception:
        pass
    return date_str


def get_release_timestamps() -> dict[str, str]:
    """Extract release timestamps from pelicanconf.py RECENT_RELEASES."""
    try:
        pelicanconf_path = REPO_ROOT / "pelicanconf.py"
        code = pelicanconf_path.read_text(encoding="utf-8")
        match = re.search(r"RECENT_RELEASES\s*=\s*(\[.*?\])", code, re.DOTALL)
        if not match:
            return {}
        
        releases_data = json.loads(re.sub(r"#.*", "", match.group(1)).replace("'", '"'))
        release_times = {}
        months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]

        for item in releases_data:
            tag = item.get("version")
            raw = item.get("timestamp")
            if tag and raw:
                m_iso = re.search(r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s(\w+)", raw)
                if m_iso:
                    dt_part, tz = m_iso.groups()
                    date_part, time_part = dt_part.split(" ")
                    y, mo, d = date_part.split("-")
                    hh, mm, ss = time_part.split(":")
                    hour = int(hh)
                    minute = int(mm)
                    ampm = "AM" if hour < 12 else "PM"
                    display_hour = hour % 12
                    if display_hour == 0:
                        display_hour = 12
                    formatted = f"{months[int(mo)-1]} {int(d)} {y}, {display_hour}:{minute:02d} {ampm} {tz}"
                    release_times[tag] = formatted
                else:
                    release_times[tag] = raw
        return release_times
    except Exception:
        return {}


def generate_prompt_history_data(milestones: list[dict], total_prompts: int) -> dict:
    """Generate structured JSON data dictionary for prompt history timeline."""
    latest_date_str = milestones[0]["date"] if milestones and milestones[0].get("date") else "2026-09-15"
    latest_formatted = format_date(latest_date_str)
    chronological_milestones = list(reversed(milestones))
    release_timestamps = get_release_timestamps()

    processed_milestones = []
    for m in chronological_milestones:
        title = m['title']
        date_str = m['date']
        
        ver_match = re.search(r"v\d+\.\d+(?:\.\d+)?", title)
        tag = ver_match.group(0) if ver_match else ""
        if tag:
            rel_link = f"https://github.com/jimcollinsworth/jimcollinsworth.github.io/releases/tag/{tag}"
            formatted_dt = release_timestamps.get(tag, format_date(date_str))
        else:
            rel_link = "https://github.com/jimcollinsworth/jimcollinsworth.github.io/releases"
            formatted_dt = format_date(date_str)

        sanitized_prompts = []
        for p in m["prompts"]:
            sanitized_p = re.sub(r"<(/?[a-zA-Z0-9]+[^>]*)>", r"&lt;\1&gt;", p.strip())
            sanitized_p = re.sub(r"`([^`]+)`", r"<code>\1</code>", sanitized_p)
            sanitized_p = sanitized_p.replace("...", "&hellip;")
            sanitized_prompts.append(sanitized_p)

        sanitized_actions = []
        for a in m["actions"]:
            sanitized_a = re.sub(r"<(/?[a-zA-Z0-9]+[^>]*)>", r"&lt;\1&gt;", a)
            sanitized_a = re.sub(r"`([^`]+)`", r"<code>\1</code>", sanitized_a)
            sanitized_a = sanitized_a.replace("...", "&hellip;")
            sanitized_actions.append(sanitized_a)

        processed_milestones.append({
            "title": title,
            "date": date_str,
            "formatted_date": formatted_dt,
            "rel_link": rel_link,
            "prompts": sanitized_prompts,
            "actions": sanitized_actions,
        })

    return {
        "latest_date_str": latest_date_str,
        "latest_formatted": latest_formatted,
        "total_prompts": total_prompts,
        "milestones_count": len(milestones),
        "milestones": processed_milestones,
    }


def main():
    milestones, total_prompts = parse_journal()
    print(f"Parsed {len(milestones)} milestones and {total_prompts} total steering prompts from JOURNAL.md")
    
    data = generate_prompt_history_data(milestones, total_prompts)
    DEV_PROMPTS_JSON.parent.mkdir(parents=True, exist_ok=True)
    DEV_PROMPTS_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Successfully generated {DEV_PROMPTS_JSON} ({len(data['milestones'])} milestones, {total_prompts} prompts)")


if __name__ == "__main__":
    main()
