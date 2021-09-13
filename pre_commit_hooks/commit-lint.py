#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File name    : commit-lint.py
Author       : miaoyc
Create date  : 2021/9/13 4:18 下午
Description  : commit提交规范检查
"""

# 根据分支名，自动添加commit message前缀以关联issue和commit。
#
# 分支名  | commit 格式
# --- | ---
# issue-1234  | #1234, message
# issue-1234-fix-bug  | #1234, message

import re
import sys
from subprocess import check_output
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    commit_msg_filepath = sys.argv[1]

    # 检测我们所在的分支
    branch = check_output(['git', 'symbolic-ref', '--short', 'HEAD']).strip().decode('utf-8')
    # 匹配如：issue-123, issue-1234-fix
    result = re.match('^issue-(\d+)((-.*)+)?$', branch)
    if not result:
        # 分支名不符合
        warning = "WARN: Unable to add issue prefix since the format of the branch name dismatch."
        warning += "\nThe branch should look like issue-<number> or issue-<number>-<other>, " \
                   "for example: issue-100012 or issue-10012-fix-bug)"
        print(warning)
        return
    issue_number = result.group(1)
    with open(commit_msg_filepath, 'r+') as f:
        content = f.read()
        if re.search('^#[0-9]+(.*)', content):
            # print('There is already issue prefix in commit message.')
            return
        issue_prefix = '#' + issue_number
        f.seek(0, 0)
        f.write("%s, %s" % (issue_prefix, content))
        # print('Add issue prefix %s to commit message.' % issue_prefix)


if __name__ == '__main__':
    exit(main())
