import json
import os
import re
import urllib.request
from pathlib import Path


README_PATH = Path("README.md")
LEETCODE_PROBLEMS_API = (
    "https://api.github.com/repos/Merd0/leetcode-c-solutions/"
    "contents/problems?ref=main"
)
COUNT_PATTERN = re.compile(
    r"(<!-- leetcode-c-count:start -->)\d+"
    r"(<!-- leetcode-c-count:end -->)"
)


def fetch_directory_count(url: str) -> int:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Merd0-profile-metrics",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request, timeout=30) as response:
        entries = json.load(response)

    return sum(entry.get("type") == "dir" for entry in entries)


def update_readme_count(count: int) -> None:
    readme = README_PATH.read_text(encoding="utf-8")
    updated, replacements = COUNT_PATTERN.subn(
        rf"\g<1>{count}\g<2>",
        readme,
        count=1,
    )

    if replacements != 1:
        raise RuntimeError("LeetCode count markers were not found exactly once")

    README_PATH.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    leetcode_count = fetch_directory_count(LEETCODE_PROBLEMS_API)
    update_readme_count(leetcode_count)
    print(f"LeetCode problem count: {leetcode_count}")
