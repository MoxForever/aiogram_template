import os
import subprocess


def read_file_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return f.read().split("\n")


def write_file_lines(file_path: str, lines: list[str]):
    with open(file_path, "w") as f:
        f.write("\n".join(lines))


def init_project():
    project_name = input("Enter project name: ")
    project_description = input("Enter project description: ")

    project_author = (
        subprocess.check_output(["git", "config", "user.name"]).strip().decode("utf-8")
    )
    project_email = (
        subprocess.check_output(["git", "config", "user.email"]).strip().decode("utf-8")
    )

    pyproject = read_file_lines("pyproject.toml")
    for i, line in enumerate(pyproject):
        if line.startswith("name = "):
            pyproject[i] = f'name = "{project_name}"'
        elif line.startswith("description = "):
            pyproject[i] = f'description = "{project_description}"'
        elif line.startswith("authors = "):
            pyproject[i] = f'authors = ["{project_author} <{project_email}>"]'

    write_file_lines("pyproject.toml", pyproject)

    os.rename("./aiogram_template", project_name)

    for root, _, files in os.walk(project_name):
        for file in files:
            if not file.endswith(".py"):
                continue
            else:
                filepath = os.path.join(root, file)

            content = read_file_lines(filepath)
            for i, l in enumerate(content):
                if l.startswith("from"):
                    content[i] = l.replace("aiogram_template", project_name)
            write_file_lines(filepath, content)

    os.system("poetry install --no-root")

    os.remove("init_project.py")


if __name__ == "__main__":
    init_project()
