import argparse
import re
import subprocess

# build: 시스템 또는 외부 종속성에 영향을 미치는 변경사항 (npm, gulp, yarn 레벨)
# ci: ci구성파일 및 스크립트 변경
# chore: 패키지 매니저 설정할 경우, 코드 수정 없이 설정을 변경
# docs: documentation 변경
# feat: 새로운 기능
# fix: 버그 수정
# perf: 성능 개선
# refactor: 버그를 수정하거나 기능을 추가하지 않는 코드 변경, 리팩토링
# style: 코드 의미에 영향을 주지 않는 변경사항 ( white space, formatting, colons )
# test: 누락된 테스트 추가 또는 기존 테스트 수정
# revert: 작업 되돌리기
# hotfix: 급하게 반영되어야하는 작업

from typing import List


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_filepath")
    parser.add_argument(
        "-r",
        "--regex",
        default=r"(build|ci|chore|docs|feat|feature|fix|perf|refactor|style|test|revert|hotfix)\/\#\d{1,5}",
        help="regex which extract github issue to branch",
    )
    parser.add_argument(
        "-t",
        "--template",
        default="{}",
        help="commit msg template. ex: [{}] -> [#111]",
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

    result: str = next(iter(matches), "")
    issue_number: str = result.upper()

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
