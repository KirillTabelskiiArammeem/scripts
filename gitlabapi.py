

import os
import requests

host = "https://gitlab.2u.team/"
token = os.getenv("CI_JOB_TOKEN")

def get_project_id(project_name):
    response  = requests.get(
        f"{host}api/v4/projects?search={project_name}",
        headers={"PRIVATE-TOKEN": token})
    return response.json()[0]['id']

def get_packages(project_id):
    response = requests.get(
        f"{host}api/v4/projects/{project_id}/packages",
        headers={"PRIVATE-TOKEN": token})
    return response.json()

def download_package(project_id, package_id):
    response = requests.get(
        f"{host}api/v4/projects/{project_id}/packages/{package_id}",
        headers={"PRIVATE-TOKEN": token},
        stream=True
    )
    if response.status_code == 200:
        with open(f"package_{package_id}.tar.gz", 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded package {package_id}")
    else:
        print(f"Failed to download package {package_id}: {response.status_code}")

project_id = get_project_id('vatnumber')
print(project_id)

# packages = get_packages(project_id)
#
# download_package(project_id, packages[0]['id'])
