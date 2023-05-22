import subprocess
import os
import csv
import re


SPACES = re.compile('\s+')

def call(command):

    proc = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = proc.communicate()
    output = output.decode()
    error = error.decode()
    return output, error


folders = [
    '/home/kirill/aram/helpdesk/odoo-modules-hd-12',
    '/home/kirill/aram/crm/odoo-modules-crm-12',
    '/home/kirill/aram/dp/odoo-modules-dp-12',
    '/home/kirill/aram/mcp/odoo-modules-mcp-12',
    '/home/kirill/aram/fcp/odoo-modules-fcp-14'
]

folders_projects_map = {
    '/home/kirill/aram/helpdesk/odoo-modules-hd-12': 'helpdesk',
    '/home/kirill/aram/crm/odoo-modules-crm-12': 'crm',
    '/home/kirill/aram/dp/odoo-modules-dp-12': 'dp',
    '/home/kirill/aram/mcp/odoo-modules-mcp-12': 'mcp',
    '/home/kirill/aram/fcp/odoo-modules-fcp-14': 'fcp'

}


# for folder in folders:
#     os.chdir(folder)
#     call(f'git checkout master')
#     call('git pull --rebase')
#     call('git config user.name "KiriillTabelskiiArammeem"; git config user.email "k.tabelskii@arammeem.com"')


def get_stat():
    cmd_get_count_commits = """git log --since="Jan 1 2023"  --before="Dec 31 2023" --all --no-merges --pretty=format:"%h" | wc -l"""
    cmd_get_all_commits = """ git --no-pager  log  --since="2023-01-01" --until="2023-12-31"  --pretty=oneline --no-merges"""
    for folder in folders:

        os.chdir(folder)
        result, error = call(cmd_get_count_commits)
        count_commits = int(result.strip())

        result, error = call(cmd_get_all_commits)
        first_commit = result.strip().split('\n')[-1].split(' ')[0]
        last_commit = result.strip().split('\n')[0].split(' ')[0]

        call(f'git checkout {first_commit}')

        result, error = call('git ls-files | xargs cat | wc -l')
        count_lines_first = int(result.strip())

        os.chdir('./modules')
        result, error = call('grep -r "def test" | wc ')
        count_tests_first = int(SPACES.split(result.strip())[0])
        os.chdir('..')


        call(f'git checkout {last_commit}')
        result, error = call('git ls-files | xargs cat | wc -l')
        count_lines_last = int(result.strip())

        os.chdir('./modules')
        result, error = call('grep -r "def test" | wc ')
        count_tests_last = int(SPACES.split(result.strip())[0])
        os.chdir('..')

        lines_diff = count_lines_last - count_lines_first
        tests_diff = count_tests_last - count_tests_first


        call(f'git checkout master')

        yield {
            'project': folders_projects_map[folder],
            'count_commits': count_commits,
            'count_lines_first': count_lines_first,
            'count_lines_last': count_lines_last,
            'lines_diff': lines_diff,
            'count_tests_first': count_tests_first,
            'count_tests_last': count_tests_last,
            'tests_diff': tests_diff

        }


cmd = """git rev-list --count --since="Jan 1 2023"  --before="Dec 31 2023" --all --no-merges"""

with open('stat.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['project', 'count_commits', 'count_lines_first', 'count_lines_last', 'lines_diff', 'count_tests_first', 'count_tests_last', 'tests_diff'])
    writer.writeheader()
    for line in get_stat():
        writer.writerow(line)
