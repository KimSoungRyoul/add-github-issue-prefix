import argparse
import re
import subprocess

from typing import List


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_filepath")
    parser.add_argument(
        "-r",
        "--regex",
        default=r"#\d{1,5}",
        help="regex which extract github issue to branch",
    )
    parser.add_argument(
        "-t",
        "--template",
        default="[{}]",
        help="commit msg template ex: [{}] -> [#111]",
    )
    args = parser.parse_args()
    commit_msg_filepath: str = args.commit_msg_filepath
    template: str = args.template
    regex_str: str = args.regex

    branch: str = ""

    try:
        branch = subprocess.check_output(
            ["git", "symbolic-ref", "--short", "HEAD"], universal_newlines=True
        ).strip()
    except Exception as e:
        print(e)

    matches: List[str] = re.findall(regex_str, branch)

    issue_number: str = matches[0] if matches else ""
    issue_number = issue_number.upper()

    with open(commit_msg_filepath, "r+") as f:
        content = f.read()
        content_subject = content.split("\n", maxsplit=1)[0].strip()
        f.seek(0, 0)
        if issue_number and issue_number not in content_subject:
            prefix = template.format(issue_number)
            f.write("{} {}".format(prefix, content))
        else:
            f.write(content)


if __name__ == "__main__":
    exit(main())
