cd /home/kirill/aram/helpdesk/odoo-modules-hd-12
git shortlog --summary --numbered --all --no-merges --since "2024-09-01" --until "2024-12-11"

cd /home/kirill/aram/dp/odoo-modules-dp-12
git shortlog --summary --numbered --all --no-merges --since "2024-09-01" --until "2024-12-11"

cd /home/kirill/aram/fcp/odoo-modules-fcp-14/
git shortlog --summary --numbered --all --no-merges --since "2024-09-01" --until "2024-12-11"

cd /home/kirill/aram/common/odoo-modules-common-12/
git shortlog --summary --numbered --all --no-merges --since "2024-09-01" --until "2024-12-11"

cd /home/kirill/aram/chat-bot/chat-bot
git shortlog --summary --numbered --all --no-merges --since "2024-09-01" --until "2024-12-11"

cd /home/kirill/aram/chat-bot/chat-bot-api
git shortlog --summary --numbered --all --no-merges --since "2024-09-01" --until "2024-12-11"

git-quick-stats -C


cd /home/kirill/aram/helpdesk/odoo-modules-hd-12

git log --author=ArtemDemidovAramMeem --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

git log --author=EvgeniaKotovaArammeem --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

git log --author=RustemIdrisovArammeem --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

git log --author="NikitaRyzhenkovArammeem" --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -


cd /home/kirill/aram/dp/odoo-modules-dp-12
git log --author=ArtemDemidovAramMeem --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

git log --author="Eduard Alekseiev" --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

git log --author="NikitaRyzhenkovArammeem" --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

cd /home/kirill/aram/fcp/odoo-modules-fcp-14/

git log --author=ArtemDemidovAramMeem --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

git log --author="Eduard Alekseiev" --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

git log --author="NikitaRyzhenkovArammeem" --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

cd /home/kirill/aram/common/odoo-modules-common-12/
git log --author=ArtemDemidovAramMeem --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

git log --author=EvgeniaKotovaArammeem --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

git log --author=RustemIdrisovArammeem --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

git log --author="Eduard Alekseiev" --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

git log --author="NikitaRyzhenkovArammeem" --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -

cd /home/kirill/aram/chat-bot/chat-bot
git log --author="Ildar" --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -
cd /home/kirill/aram/chat-bot/chat-bot-api
git log --author="Ildar" --since "2024-09-01" --until "2024-12-11" --pretty=tformat: --numstat \
| gawk '{ add += $1; subs += $2; loc += $1 + $2 } END { printf "added lines: %s removed lines: %s total lines: %s\n", add, subs, loc }' -