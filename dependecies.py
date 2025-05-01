import os
import re


def extract_depends(manifest_path):
    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the position of 'depends', taking into account different quotation marks
    depends_pos = (
        content.find("'depends'")
        if "'depends'" in content
        else content.find('"depends"')
    )
    if depends_pos == -1:
        return []

    # Extract depends list starting from the position of 'depends'
    match = re.search(r"\[\s*([\s\S]*?)\s*\]", content[depends_pos:])
    if match:
        depends_str = match.group(1)
        depends = re.findall(r'["\'](.*?)["\']', depends_str)
        return depends
    return []


def generate_plantuml_code():
    root_dir = os.getcwd()
    plantuml_code = "@startuml\n"

    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)

        if os.path.isdir(folder_path):
            manifest_path = os.path.join(folder_path, "__manifest__.py")
            if os.path.exists(manifest_path):
                depends = extract_depends(manifest_path)
                print(f"Dependencies for {folder_name}: {depends}")  # Debugging info
                for dep in depends:
                    plantuml_code += f"[{folder_name}] --> [{dep}]\n"

    plantuml_code += "@enduml\n"
    return plantuml_code


if __name__ == "__main__":
    code = generate_plantuml_code()
    with open("dependencies.puml", "w", encoding="utf-8") as f:
        f.write(code)
    print("Generated dependencies.puml")