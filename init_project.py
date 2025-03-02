import os

def init_project():
    project_name = input()

    with open("pyproject.toml", "r") as f:
        pyproject = f.readlines()

    for line in pyproject:
        if line.startswith("name = "):
            line = f'name = "{project_name}"\n'

    with open("pyproject.toml", "w") as f:
        f.writelines(pyproject)

    os.rename("./aiogram_template", project_name)

    for root, _, files in os.walk(project_name):
        for file in files:
            if not file.endswith(".py"):
                continue

            filepath = os.path.join(root, file)
            with open(filepath, "r") as f:
                content = f.readlines()

            for l in content:
                if l.startswith("from aiogram_tepmlate"):
                    l = l.replace("aiogram_template", project_name)

            with open(filepath, "w") as f:
                f.writelines(content)

            


if __name__ == "__main__":
    init_project()
