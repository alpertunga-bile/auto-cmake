from os.path import join
from typing import Tuple


from .creator_helper import (
    CMakeConfigs,
    get_include_files,
    get_include_files_recursive,
    get_source_files,
    get_source_files_recursive,
    get_configs,
    get_macro_str,
    get_subdir_dirs,
    log_info,
    log_warning,
    PROJECT_NAME,
    PROJECT_VERSION,
    HEADER_FILES,
    SOURCE_FILES,
)
from .extra_parser import get_extra_configs


def get_starting_string(
    project_name: str, project_version: str, configuration: str
) -> str:
    return f"""
cmake_minimum_required(VERSION 3.5.0)
project({project_name} VERSION {project_version} LANGUAGES C CXX)

include(CTest)
enable_testing()

set(CMAKE_BUILD_TYPE {configuration})\n
"""


def get_packages_string(required_packages: set[str]) -> str:
    package_string = ""

    for package in required_packages:
        package_string += f"find_package({package} REQUIRED)\n\n"

    return package_string


def get_header_strings(
    required_packages: set[str], files: set[str], dirs: set[str]
) -> str:
    header_string = "set(HEADER_FILES\n"

    for file in files:
        header_string += f"    {file}\n"

    header_string += ")\n\n"

    header_string += "include_directories(\n"

    for dir in dirs:
        header_string += f"    {dir}\n"

    for package in required_packages:
        header_string += f"    {get_macro_str(f'{package.upper()}_INCLUDE_DIRS')}\n"

    header_string += ")\n\n"

    return header_string


def get_source_string(files: set[str]) -> str:
    source_string = "set(SOURCE_FILES\n"

    for file in files:
        source_string += f"    {file}\n"

    source_string += f"    {HEADER_FILES}\n)\n\n"

    return source_string


def get_executable_string(
    required_packages: set[str], project_type: str, subdir_path: str
) -> str:
    exec_string = ""

    if project_type == "executable":
        exec_string += f"add_executable({PROJECT_NAME} {SOURCE_FILES})\n\n"
    elif project_type == "library":
        exec_string += f"add_library({PROJECT_NAME} {SOURCE_FILES})\n\n"
    elif project_type == "win32":
        exec_string += f"add_executable({PROJECT_NAME} WIN32 {SOURCE_FILES})\n\n"

    exec_string += f"target_link_libraries({PROJECT_NAME} PRIVATE\n"

    for package in required_packages:
        exec_string += f"    {get_macro_str(f'{package.upper()}_LIBRARIES')}\n"

    dirs = get_subdir_dirs(subdir_path)
    for subdir in dirs:
        exec_string += f"    {subdir}\n"

    exec_string += ")\n\n"

    return exec_string


def get_precompile_string(precompile_headers: set[str]) -> str:
    pre_string = "target_precompile_headers(\n"
    pre_string += f"    {PROJECT_NAME} PRIVATE\n"
    pre_string += f"    {HEADER_FILES}\n"

    for header in precompile_headers:
        pre_string += f"    <{header}>\n"

    pre_string += ")\n\n"

    return pre_string


def get_subdir_string(subdir_path: str) -> str:
    subdirs = get_subdir_dirs(subdir_path)
    subdir_string = ""

    for subdir in subdirs:
        subdir_string += f"add_subdirectory({join(subdir_path, subdir)})\n"

    return subdir_string


def get_cxx_version_string(version: int) -> str:
    return f"target_compile_features({PROJECT_NAME} PRIVATE cxx_std_{str(version)})\n\n"


def get_cpack_string() -> str:
    cpack_string = ""

    cpack_string += f"set(CPACK_PROJECT_NAME {PROJECT_NAME})\n"
    cpack_string += f"set(CPACK_PROJECT_VERSION {PROJECT_VERSION})\n"
    cpack_string += "include(CPack)"

    return cpack_string


def get_include_variables(
    include_dirs: set[str], exclude_dirs: set[str], exclude_files: set[str]
) -> Tuple[set[str], set[str]]:
    inc_files = set()
    inc_dirs = set()

    if len(include_dirs) == 0:
        inc_files, inc_dirs = get_include_files_recursive(exclude_files, exclude_dirs)
    else:
        for inc_dir in include_dirs:
            rtn_files, rtn_dirs = get_include_files(
                inc_dir, exclude_files, exclude_dirs
            )

            inc_files.update(rtn_files)
            inc_dirs.update(rtn_dirs)

    return (inc_files, inc_dirs)


def get_source_variables(
    source_dirs: set[str], exclude_dirs: set[str], exclude_files: set[str]
) -> Tuple[set[str], set[str]]:
    src_files = set()
    src_dirs = set()

    if len(source_dirs) == 0:
        src_files, src_dirs = get_source_files_recursive(exclude_files, exclude_dirs)
    else:
        for src_dir in source_dirs:
            rtn_files, rtn_dirs = get_source_files(src_dir, exclude_files, exclude_dirs)

            src_files.update(rtn_files)
            src_dirs.update(rtn_dirs)

    return (src_files, src_dirs)


def print_cmake_config(configs: CMakeConfigs):
    print(
        f"""
{" CMake Config Values ".center(50, "#")}
Project Name    : {configs.project_name}
Project Version : {configs.project_version}
Configuration   : {configs.configuration}
{"#" * 50}    
"""
    )


def create(verbose: bool):
    log_info("Starting", True)
    configs = get_configs()

    print_cmake_config(configs)

    header_files, header_dirs = get_include_variables(
        configs.inc_include_dirs, configs.inc_exclude_dirs, configs.inc_exclude_files
    )

    log_info(f"Header files are gathered | Total : {len(header_files)}", verbose)

    source_files, source_dirs = get_source_variables(
        configs.src_include_dirs, configs.src_exclude_dirs, configs.src_exclude_files
    )

    log_info(f"Source files are gathered | Total : {len(source_files)}", verbose)

    extra_config = get_extra_configs(configs.extra_cmake_path)

    log_info(f"Extra CMake configs are read from {configs.extra_cmake_path}", verbose)

    cmake_string = ""

    cmake_string += get_starting_string(
        configs.project_name, configs.project_version, configs.configuration
    )
    cmake_string += extra_config.after_starting_str

    cmake_string += get_packages_string(configs.required_packages)
    cmake_string += extra_config.after_packages_str

    cmake_string += get_header_strings(
        configs.required_packages, header_files, header_dirs
    )
    cmake_string += extra_config.after_headers_str

    cmake_string += get_source_string(source_files)
    cmake_string += extra_config.after_sources_str

    cmake_string += get_executable_string(
        configs.required_packages, configs.project_type, configs.subdir_path
    )
    cmake_string += extra_config.after_executable_str

    cmake_string += get_precompile_string(configs.precompile_headers)
    cmake_string += extra_config.after_precompile_str

    cmake_string += get_subdir_string(configs.subdir_path)
    cmake_string += extra_config.after_subdirectory_str

    cmake_string += get_cxx_version_string(configs.cxx_version)
    cmake_string += extra_config.after_cxx_version_str

    cmake_string += get_cpack_string()
    cmake_string += extra_config.after_cpack_str

    log_info("CMake string is ready to write", verbose)

    with open("CMakeLists_test.txt", "w") as cmake_file:
        cmake_file.write(cmake_string)

    log_info("CMakeLists.txt file is created", True)
