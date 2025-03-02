import os
import shutil
import subprocess
from dataclasses import dataclass


HOST_TYPES = {
    "SystemD": "bot.service",
    "Docker": "docker",
}


@dataclass
class ProjectInfo:
    name: str
    description: str
    author: str


def read_file_lines(file_path: str) -> list[str]:
    with open(file_path, "r") as f:
        return f.read().split("\n")


def write_file_lines(file_path: str, lines: list[str]):
    with open(file_path, "w") as f:
        f.write("\n".join(lines))


def base_project_info() -> ProjectInfo:
    print("Enter project name:")
    project_name = input(">>")

    print("Enter project description:")
    project_description = input(">>")

    project_author = (
        subprocess.check_output(["git", "config", "user.name"]).strip().decode("utf-8")
    )
    project_email = (
        subprocess.check_output(["git", "config", "user.email"]).strip().decode("utf-8")
    )

    return ProjectInfo(
        name=project_name,
        description=project_description,
        author=f"{project_author} <{project_email}>",
    )


def get_host_method() -> str:
    result: str | None = None
    host_method: str = ""
    host_methods_text: str = "\n".join(
        [f"{i}. {t}" for i, t in enumerate(HOST_TYPES.keys())]
    )
    while True:
        print("Choose host method:")
        print(host_methods_text)

        host_method = input(">>")
        if host_method.isnumeric():
            if 1 <= int(host_method) <= len(HOST_TYPES):
                result = list(HOST_TYPES.keys())[int(host_method)]
                break

        print("Invalid input. Try again.")

    return result


def edit_pyproject_and_alembic(project: ProjectInfo):
    pyproject = read_file_lines("pyproject.toml")
    for i, line in enumerate(pyproject):
        if line.startswith("name = "):
            pyproject[i] = f'name = "{project.name}"'
        elif line.startswith("description = "):
            pyproject[i] = f'description = "{project.description}"'
        elif line.startswith("authors = "):
            pyproject[i] = f'authors = ["{project.author}"]'

    alembic = read_file_lines("alembic.ini")
    for i, line in enumerate(alembic):
        if line.startswith("script_location = "):
            alembic[i] = line.replace("aiogram_template", project.name)

    write_file_lines("pyproject.toml", pyproject)
    write_file_lines("alembic.ini", alembic)


def rename_imports_and_src(project_name: str):
    os.rename("./aiogram_template", project_name)

    files_list = ["./main.py"]
    for root, _, files in os.walk(project_name):
        for file in files:
            if file.endswith(".py"):
                files_list.append(os.path.join(root, file))

    for file in files_list:
        content = read_file_lines(file)
        for i, l in enumerate(content):
            if l.startswith("from"):
                content[i] = l.replace("aiogram_template", project_name)
            elif l.strip() == "":
                continue
            else:
                break

        write_file_lines(file, content)


def remove_unused_host_methods(host_method: str):
    for name, path in HOST_TYPES.items():
        if name != host_method:
            os.remove(path)


def init_project():
    project = base_project_info()
    host_method = get_host_method()

    edit_pyproject_and_alembic(project)
    rename_imports_and_src(project.name)
    remove_unused_host_methods(host_method)

    shutil.copy("example.env", ".env")
    os.system("poetry install --no-root")

    os.remove("init_project.py")


if __name__ == "__main__":
    init_project()
