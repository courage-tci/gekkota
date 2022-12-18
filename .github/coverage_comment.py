from subprocess import check_output
from json import loads
from os import getenv

commit_sha = getenv("GITHUB_SHA")
repo = getenv("GITHUB_REPOSITORY")


def filename_link(filename: str, line: int | None = None) -> str:
    return f"https://github.com/{repo}/blob/{commit_sha}/{filename}{f'#{line}' if line else ''}"


def format_link(text: str, url: str) -> str:
    return f"[{text}]({url})"


def format_filename_link(filename: str):
    return format_link(filename, filename_link(filename))


def make_ranges(file):
    ranges = []

    for missing_line in file["missing_lines"]:
        if not ranges:
            ranges.append([missing_line, missing_line])
            continue
        if ranges[-1][1] + 1 == missing_line:
            ranges[-1][1] = missing_line
        else:
            ranges.append([missing_line, missing_line])

    return ranges


def format_lines(filename, file):
    return ", ".join(
        [
            format_link(
                "-".join(map(str, sorted(set(r)))), filename_link(filename, line=r[0])
            )
            for r in make_ranges(file)
        ]
    )


report = loads(check_output(["coverage", "json", "--include", "gekkota/*", "-o", "-"]))

total_percent = report["totals"]["percent_covered"]

total_message = f"The coverage is {total_percent:.2f}%."

missing_message = "Good work!"
missing_list = ""

if total_percent < 100:
    missing_message = "Missing coverage:\n"

    missing_list = "\n".join(
        [
            f"- {format_filename_link(filename)}: {format_lines(filename, file)}"
            for filename, file in report["files"].items()
            if file["missing_lines"] and filename.startswith("gekkota")
        ]
    )


message = f"""Test coverage report:

{total_message} {missing_message}{missing_list}
"""

with open("coverage.txt", "w") as file:
    file.write(message)
