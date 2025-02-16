docker image rm odoo-modules-hd-12-odoo_test --force;
docker image rm odoo-modules-hd-12-odoo --force;
docker image rm odoo-modules-hd-12-python_interpreter --force;
docker image rm odoo-modules-dp-12-odoo_test --force;
docker image rm odoo-modules-dp-12-odoo --force;
docker image rm odoo-modules-dp-12-python_interpreter --force;
docker image rm arammeem16/odoo_base --force;
docker image rm arammeem16/odoo_core:12.0-latest --force;

cd ~/aram/devops/docker-image-sources
git pull --rebase
cd ./odoo.12.base
make build_latest
#docker pull arammeem16/odoo_base:12.0-rel-20221012-0.0.1-85a8e26

cd ~/aram/common/odoo-modules-common-12
git pull --rebase
cd ./odoo.12.core
docker build . --build-arg=VERSION_BASE=latest -t arammeem16/odoo_core:12.0-latest
#docker build -f ./Dockerfile.bookworm.python3.10 .  --build-arg=VERSION_BASE=latest -t arammeem16/odoo_core:12.0-latest
#docker build . --build-arg=VERSION_BASE=12.0-rel-20221012-0.0.1-85a8e26 -t arammeem16/odoo_core:12.0-latest