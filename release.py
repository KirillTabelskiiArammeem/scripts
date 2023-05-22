import os
import re

TASK_REGEX = re.compile(r'[A-Z]{2,3}-\d+')


def read(data_file: str) -> str:
    with open(os.path.join('check_release_data', data_file)) as file:
        return file.read()


def parse(dat_text: str) -> set:
    return set(TASK_REGEX.findall(dat_text))


def process_data_file(data_file: str):
    return parse(read(data_file))


def set_to_str(erp_set: set):

    return '\n'.join(sorted(f'\t{item}' for item in erp_set))


def print_report(title: str, erp_set: set):
    print('*'*20)
    print(title)
    print(set_to_str(erp_set))
    print('*'*20)


def main():
    jira = process_data_file('jira_row.txt')
    git = process_data_file('git_row.txt')

    jira_minus_git = jira - git
    git_minus_jira = git - jira

    if jira_minus_git:
        print_report('Tasks in jira, but not in git:', jira_minus_git)

    if git_minus_jira:
        print_report('Tasks in git, but not in jira:', git_minus_jira)


if __name__ == '__main__':
    main()
