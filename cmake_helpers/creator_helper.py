from os import walk, getcwd, listdir
from os.path import join, relpath, isdir, splitext, exists
from json import loads
from typing import Tuple

PROJECT_NAME = "${PROJECT_NAME}"
PROJECT_VERSION = "${PROJECT_VERSION}"
HEADER_FILES = "${HEADER_FILES}"
SOURCE_FILES = "${SOURCE_FILES}"


def log(type: str, msg: str) -> None:
    print("/_\\ %-8s /_\\ %s" % (type, msg))


def log_info(msg: str, verbose: bool) -> None:
    if verbose is False:
        return

    log("INFO", msg)


def log_warning(msg: str, verbose: bool) -> None:
    if verbose is False:
        return

    log("WARNING", msg)


def check_file_extension(filepath: str, extensions: str) -> bool:
    _, ext = splitext(filepath)

    if ext in extensions:
        return True

    return False


def get_files(
    workpath: str, extensions: set, exclude_dirs: set[str], exclude_files: set[str]
) -> Tuple[set[str], set[str]]:
    wanted_files = set()
    wanted_dirs = set()

    for roots, _, files in walk(workpath):
        for file in files:
            if file in exclude_files:
                continue

            if check_file_extension(file, extensions) is False:
                continue

            wanted_dir = relpath(roots)
            if wanted_dir in exclude_dirs:
                continue

            wanted_dirs.add(wanted_dir)
            wanted_files.add(relpath(join(roots, file)))

    return (wanted_files, wanted_dirs)


def get_include_files_recursive(
    exclude_files: set[str], exclude_dirs: set[str]
) -> Tuple[set[str], set[str]]:
    extensions = set()
    extensions.add(".h")
    extensions.add(".hpp")

    return get_files(getcwd(), extensions, exclude_dirs, exclude_files)


def get_include_files(
    dirpath: str, exclude_files: set[str], exclude_dirs: set[str]
) -> Tuple[set[str], set[str]]:
    extensions = set()
    extensions.add(".h")
    extensions.add(".hpp")

    return get_files(dirpath, extensions, exclude_dirs, exclude_files)


def get_source_files_recursive(
    exclude_files: set[str], exclude_dirs: set[str]
) -> Tuple[set[str], set[str]]:
    extensions = set()
    extensions.add(".c")
    extensions.add(".cpp")

    return get_files(getcwd(), extensions, exclude_dirs, exclude_files)


def get_source_files(
    dirpath: str, exclude_files: set[str], exclude_dirs: set[str]
) -> Tuple[set[str], set[str]]:
    extensions = set()
    extensions.add(".c")
    extensions.add(".cpp")

    return get_files(dirpath, extensions, exclude_dirs, exclude_files)


def get_subdir_dirs(subdir_path: str) -> set[str]:
    if exists(subdir_path) is False:
        return set()

    dirs = [dir for dir in listdir(subdir_path) if isdir(join(subdir_path, dir))]

    real_subdirs = set()

    for subdir in dirs:
        if exists(join(subdir_path, subdir, "CMakeLists.txt")) is False:
            continue

        real_subdirs.add(subdir)

    return real_subdirs


def get_macro_str(macro: str) -> str:
    return "${" + macro + "}"


from typing import NamedTuple


class CMakeConfigs(NamedTuple):
    project_name: str
    project_version: str
    configuration: str
    required_packages: list[str]
    inc_include_dirs: list[str]
    inc_exclude_dirs: list[str]
    inc_exclude_files: list[str]
    src_include_dirs: list[str]
    src_exclude_dirs: list[str]
    src_exclude_files: list[str]
    project_type: str
    precompile_headers: list[str]
    subdir_path: str
    cxx_version: int
    extra_cmake_path: str


def get_configs() -> CMakeConfigs:
    with open("cmake_config.json", "r") as json_file:
        json = loads(json_file.read())

    return CMakeConfigs(
        json["project_name"],
        json["project_version"],
        json["configuration"],
        json["required_packages"],
        json["includes"]["include_dirs"],
        json["includes"]["exclude_dirs"],
        json["includes"]["exclude_files"],
        json["sources"]["include_dirs"],
        json["sources"]["exclude_dirs"],
        json["sources"]["exclude_files"],
        json["project_type"],
        json["precompile_headers"],
        json["subdirectory_path"],
        json["cxx_version"],
        json["extra_cmake_path"],
    )
