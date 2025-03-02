import os


def init_project():
    project_name = input()
    project_description = input()

    project_author = os.system("git config user.name")
    project_email = os.system("git config user.email")

    with open("pyproject.toml", "r") as f:
        pyproject = f.read().split("\n")

    for i, line in enumerate(pyproject):
        if line.startswith("name = "):
            pyproject[i] = f'name = "{project_name}"'
        elif line.startswith("description = "):
            pyproject[i] = f'description = "{project_description}"'
        elif line.startswith("authors = "):
            pyproject[i] = f'authors = ["{project_author} <{project_email}>"]'

    with open("pyproject.toml", "w") as f:
        f.write("\n".join(pyproject))

    os.rename("./aiogram_template", project_name)

    for root, _, files in os.walk(project_name):
        for file in files:
            if not file.endswith(".py"):
                continue

            filepath = os.path.join(root, file)
            with open(filepath, "r") as f:
                content = f.readlines()

            for i, l in enumerate(content):
                if l.startswith("from"):
                    content[i] = l.replace("aiogram_template", project_name)

            with open(filepath, "w") as f:
                f.writelines(content)

    os.system("poetry install --no-root")


if __name__ == "__main__":
    init_project()
