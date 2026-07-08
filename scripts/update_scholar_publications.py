#!/usr/bin/env python3
"""Update _data/publications.yml from a Google Scholar profile page.

Usage:
  python scripts/update_scholar_publications.py --user QMijGnwAAAAJ
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import html
import pathlib
import re
import subprocess
import sys
import urllib.parse
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "_data" / "publications.yml"
DEFAULT_CONFIG = ROOT / "_config.yml"

SMALL_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "but",
    "by",
    "for",
    "from",
    "in",
    "into",
    "nor",
    "of",
    "on",
    "onto",
    "or",
    "over",
    "per",
    "the",
    "to",
    "up",
    "via",
    "vs",
    "with",
    "without",
}

ACRONYM_MAP = {
    "drl": "DRL",
    "iov": "IoV",
    "iot": "IoT",
    "ids": "IDS",
    "rsma": "RSMA",
    "kan": "KAN",
    "v2x": "V2X",
    "vanet": "VANET",
    "vanets": "VANETs",
    "ieee": "IEEE",
    "mape": "MAPE",
    "iscit": "ISCIT",
    "vtc": "VTC",
    "emc": "EMC",
}

VENUE_OVERRIDES = {
    "joint optimization of task offloading and resource allocation for cooperative perception in vehicular edge computing systems":
        "IEEE Transactions on Vehicular Technology 74 (12), 19237-19251",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", help="Google Scholar user id, e.g. QMijGnwAAAAJ")
    parser.add_argument("--lang", default="zh-CN")
    parser.add_argument(
        "--skip-paper-links",
        action="store_true",
        help="Skip resolving direct paper URLs from each Scholar citation page.",
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    return parser.parse_args()


def extract_user_from_config(config_path: pathlib.Path) -> str | None:
    if not config_path.exists():
        return None
    text = config_path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'googlescholar\s*:\s*"([^"]+)"', text)
    if not m:
        return None
    url = m.group(1)
    qm = re.search(r"[?&]user=([A-Za-z0-9_-]+)", url)
    return qm.group(1) if qm else None


def build_scholar_url(user: str, lang: str) -> str:
    query = urllib.parse.urlencode({"user": user, "hl": lang, "oi": "sra"})
    return f"https://scholar.google.com/citations?{query}"


def fetch_html_with_urllib(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def quote_powershell_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def fetch_html_with_powershell(url: str, timeout: int = 60) -> str:
    script = (
        "$ProgressPreference = 'SilentlyContinue'; "
        f"$url = {quote_powershell_string(url)}; "
        f"$timeout = {int(timeout)}; "
        "$response = Invoke-WebRequest -Uri $url -Headers @{ 'User-Agent' = 'Mozilla/5.0' } -TimeoutSec $timeout; "
        "[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($response.Content))"
    )
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", script],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    return base64.b64decode(result.stdout.strip()).decode("utf-8", errors="ignore")


def fetch_html(url: str, timeout: int = 60) -> str:
    try:
        return fetch_html_with_urllib(url, timeout=timeout)
    except Exception as urllib_error:
        if not sys.platform.startswith("win"):
            raise
        try:
            return fetch_html_with_powershell(url, timeout=timeout)
        except Exception as powershell_error:
            raise RuntimeError(
                f"Failed to fetch {url} with urllib ({urllib_error}) and PowerShell ({powershell_error})."
            ) from powershell_error


def strip_html(raw: str) -> str:
    no_tags = re.sub(r"<.*?>", "", raw, flags=re.S)
    return html.unescape(no_tags).replace("\xa0", " ").strip()


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def clean_venue(venue_raw: str) -> str:
    venue = normalize_text(venue_raw)
    venue = re.sub(r",\s*\d{4}$", "", venue).strip().rstrip(",")
    for bad in ("â€¦", "鈥¦", "鈥?", "锟?", "�"):
        venue = venue.replace(bad, "")
    venue = re.sub(r"\s*(?:\.{3}|…)+\s*$", "", venue).strip()
    venue = venue.rstrip(" ,;:-")
    return venue


def apply_venue_override(title: str, venue: str) -> str:
    key = title.lower().strip()
    return VENUE_OVERRIDES.get(key, venue)


def _style_token(token: str, is_first: bool, is_last: bool, force_cap: bool) -> str:
    m = re.match(r"^([^A-Za-z0-9]*)([A-Za-z0-9][A-Za-z0-9']*)([^A-Za-z0-9]*)$", token)
    if not m:
        return token

    prefix, core, suffix = m.groups()
    lower = core.lower()

    if lower in ACRONYM_MAP:
        styled = ACRONYM_MAP[lower]
    elif any(ch.isupper() for ch in core[1:]) and any(ch.islower() for ch in core):
        # Keep existing mixed-case words such as DistilBERT, CATwin.
        styled = core
    elif core.isupper() and len(core) > 1:
        styled = core
    elif core[0].isdigit():
        styled = core
    elif not force_cap and not is_first and not is_last and lower in SMALL_WORDS:
        styled = lower
    else:
        styled = core[0].upper() + core[1:].lower()

    return f"{prefix}{styled}{suffix}"


def style_title(text: str) -> str:
    words = text.split()
    if not words:
        return text

    out: list[str] = []
    for idx, word in enumerate(words):
        is_first = idx == 0
        is_last = idx == len(words) - 1

        # Handle compound words such as "drl-enhanced" or "in-vehicle".
        pieces = re.split(r"([/-])", word)
        word_parts = [i for i, p in enumerate(pieces) if p not in {"-", "/"}]
        for part_pos, part_i in enumerate(word_parts):
            part_is_first = is_first and part_pos == 0
            part_is_last = is_last and part_pos == len(word_parts) - 1
            force_cap = part_pos > 0
            pieces[part_i] = _style_token(
                pieces[part_i],
                is_first=part_is_first,
                is_last=part_is_last,
                force_cap=force_cap,
            )

        out.append("".join(pieces))

    return " ".join(out)


def classify_pub_type(venue: str) -> str:
    v = venue.lower()
    journal_hints = ["journal", "transactions", "letters"]
    conf_hints = ["conference", "symposium", "workshop", "vtc", "iscit", "mape"]
    if any(k in v for k in journal_hints):
        return "journal"
    if any(k in v for k in conf_hints):
        return "conference"
    return "other"


def parse_profile_stats(page_html: str) -> dict[str, int]:
    table_m = re.search(r'<table id="gsc_rsb_st".*?</table>', page_html, flags=re.S)
    if not table_m:
        return {}

    rows = re.findall(r"<tr>(.*?)</tr>", table_m.group(0), flags=re.S)
    first_col_values: list[int] = []
    for row in rows:
        nums = re.findall(r'class="gsc_rsb_std">\s*(\d+)\s*</td>', row, flags=re.S)
        if nums:
            first_col_values.append(int(nums[0]))

    keys = ["citations", "h_index", "i10_index"]
    stats = {k: 0 for k in keys}
    for i, key in enumerate(keys):
        if i < len(first_col_values):
            stats[key] = first_col_values[i]
    return stats


def to_absolute_url(url: str) -> str:
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return "https://scholar.google.com" + url
    return url


def extract_direct_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc.endswith("scholar.google.com"):
        qs = urllib.parse.parse_qs(parsed.query)
        if qs.get("url"):
            return qs["url"][0]
    return url


def resolve_paper_url(scholar_url: str) -> str:
    try:
        detail_html = fetch_html(scholar_url)
    except Exception:
        return scholar_url

    m = re.search(
        r'<a[^>]*class="gsc_oci_title_link"[^>]*href="([^"]+)"',
        detail_html,
        flags=re.S,
    )
    if not m:
        return scholar_url

    candidate = html.unescape(m.group(1)).strip()
    candidate = to_absolute_url(candidate)
    candidate = extract_direct_url(candidate)
    return candidate or scholar_url


def load_existing_paper_urls(path: pathlib.Path) -> dict[str, str]:
    if not path.exists():
        return {}

    urls: dict[str, str] = {}
    current_title: str | None = None
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        title_m = re.match(r'\s+title:\s+"(.*)"\s*$', line)
        if title_m:
            current_title = title_m.group(1).replace('\\"', '"').replace('\\\\', '\\')
            continue

        paper_m = re.match(r'\s+paper_url:\s+"(.*)"\s*$', line)
        if paper_m and current_title:
            urls[current_title.lower()] = paper_m.group(1).replace('\\"', '"').replace('\\\\', '\\')
            current_title = None

    return urls


def parse_publications(
    page_html: str,
    skip_paper_links: bool,
    existing_paper_urls: dict[str, str] | None = None,
) -> list[dict[str, object]]:
    rows = re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page_html, flags=re.S)
    items: list[dict[str, object]] = []
    existing_paper_urls = existing_paper_urls or {}

    for row in rows:
        title_m = re.search(r'class="gsc_a_at">(.*?)</a>', row, flags=re.S)
        link_m = re.search(r'<a href="([^"]+)" class="gsc_a_at">', row, flags=re.S)
        year_m = re.search(r'<span class="gsc_a_h gsc_a_hc gs_ibl">(.*?)</span>', row)
        cite_m = re.search(r'class="gsc_a_ac gs_ibl">(.*?)</a>', row, flags=re.S)
        gray = re.findall(r'<div class="gs_gray">(.*?)</div>', row, flags=re.S)

        if not title_m or not link_m or len(gray) < 2:
            continue

        title = style_title(normalize_text(strip_html(title_m.group(1))))
        authors = normalize_text(strip_html(gray[0]))
        venue = clean_venue(strip_html(gray[1]))
        venue = apply_venue_override(title, venue)
        year = int(year_m.group(1)) if year_m else 0
        cited_by = int(cite_m.group(1)) if cite_m and cite_m.group(1).strip().isdigit() else 0
        scholar_url = "https://scholar.google.com" + link_m.group(1).replace("&amp;", "&")
        paper_url = existing_paper_urls.get(title.lower(), scholar_url) if skip_paper_links else resolve_paper_url(scholar_url)

        if not venue:
            continue
        if "beamer" in title.lower():
            continue

        pub_type = classify_pub_type(venue)
        if pub_type not in {"journal", "conference"}:
            continue

        items.append(
            {
                "type": pub_type,
                "title": title,
                "authors": authors,
                "venue": venue,
                "year": year,
                "cited_by": cited_by,
                "scholar_url": scholar_url,
                "paper_url": paper_url,
            }
        )

    items.sort(key=lambda x: (int(x["cited_by"]), int(x["year"])), reverse=True)
    return items


def yq(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def dump_yaml(items: list[dict[str, object]], stats: dict[str, int], output_path: pathlib.Path) -> None:
    today = dt.date.today().isoformat()
    lines: list[str] = [f'updated_at: "{today}"']
    lines.append("profile:")
    lines.append(f'  citations: {int(stats.get("citations", 0))}')
    lines.append(f'  h_index: {int(stats.get("h_index", 0))}')
    lines.append(f'  i10_index: {int(stats.get("i10_index", 0))}')
    lines.append("items:")

    for item in items:
        lines.append(f'  - type: {yq(str(item["type"]))}')
        lines.append(f'    title: {yq(str(item["title"]))}')
        lines.append(f'    authors: {yq(str(item["authors"]))}')
        lines.append(f'    venue: {yq(str(item["venue"]))}')
        lines.append(f'    year: {int(item["year"])}')
        lines.append(f'    cited_by: {int(item["cited_by"])}')
        lines.append(f'    scholar_url: {yq(str(item["scholar_url"]))}')
        lines.append(f'    paper_url: {yq(str(item["paper_url"]))}')

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    output = pathlib.Path(args.output).resolve()

    user = args.user
    if not user:
        user = extract_user_from_config(pathlib.Path(args.config))
    if not user:
        print("Error: missing Scholar user id. Use --user or configure author.googlescholar in _config.yml.")
        return 1

    url = build_scholar_url(user, args.lang)
    page_html = fetch_html(url)
    stats = parse_profile_stats(page_html)
    existing_paper_urls: dict[str, str] = {}
    if args.skip_paper_links:
        for existing_source in (output, DEFAULT_OUTPUT):
            existing_paper_urls.update(load_existing_paper_urls(existing_source))
    items = parse_publications(page_html, args.skip_paper_links, existing_paper_urls)

    if not items:
        print("Error: no publication rows parsed from Scholar page.")
        return 2

    dump_yaml(items, stats, output)
    print(f"Updated {output} with {len(items)} publications from {url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
