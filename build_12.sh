docker image rm odoo-modules-hd-12-odoo_test --force;
docker image rm odoo-modules-hd-12-odoo --force;
docker image rm odoo-modules-hd-12-python_interpreter --force;
docker image rm odoo-modules-crm-12-odoo_test --force;
docker image rm odoo-modules-crm-12-odoo --force;
docker image rm odoo-modules-crm-12-python_interpreter --force;
docker image rm arammeem16/odoo_base  --force;
docker image rm arammeem16/odoo_core:12.0-latest --force;

cd ~/aram/devops/docker-image-sources
git pull --rebase
cd ./odoo.12.base
make build_latest
cd ~/aram/common/odoo-modules-common-12
git pull --rebase
cd ./odoo.12.core
docker build . --build-arg=VERSION_BASE=latest -t arammeem16/odoo_core:12.0-latest