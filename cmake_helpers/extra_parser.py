from os.path import exists
from typing import NamedTuple


class ExtraConfigs(NamedTuple):
    after_starting_str: str = ""
    after_packages_str: str = ""
    after_headers_str: str = ""
    after_sources_str: str = ""
    after_executable_str: str = ""
    after_precompile_str: str = ""
    after_subdirectory_str: str = ""
    after_cxx_version_str: str = ""
    after_cpack_str: str = ""


def get_extra_config_str(starting_str: str, ending_str: str, configs: list[str]) -> str:
    if starting_str in configs:
        starting_str_index = configs.index(starting_str)
    else:
        return ""

    if ending_str in configs:
        ending_str_index = configs.index(ending_str)
    else:
        return ""

    config_str = ""
    for index in range(starting_str_index + 1, ending_str_index):
        config_str += configs[index] if configs[index] != "" else "\n"
        config_str += "\n"

    config_str += "\n"

    return config_str


def get_extra_configs(extra_config_path: str) -> ExtraConfigs:
    if exists(extra_config_path) is False:
        return ExtraConfigs()

    with open(extra_config_path, "r") as config_file:
        configs = config_file.readlines()

    configs = [config.replace("\n", "") for config in configs]

    BEGIN_AFTER_STARTING = "### BEGIN AFTER STARTING"
    END_AFTER_STARTING = "### END AFTER STARTING"
    BEGIN_AFTER_PACKAGES = "### BEGIN AFTER PACKAGES"
    END_AFTER_PACKAGES = "### END AFTER PACKAGES"
    BEGIN_AFTER_HEADERS = "### BEGIN AFTER HEADERS"
    END_AFTER_HEADERS = "### END AFTER HEADERS"
    BEGIN_AFTER_SOURCES = "### BEGIN AFTER SOURCES"
    END_AFTER_SOURCES = "### END AFTER SOURCES"
    BEGIN_AFTER_EXECUTABLE = "### BEGIN AFTER EXECUTABLE"
    END_AFTER_EXECUTABLE = "### END AFTER EXECUTABLE"
    BEGIN_AFTER_PRECOMPILE = "### BEGIN AFTER PRECOMPILE"
    END_AFTER_PRECOMPILE = "### END AFTER PRECOMPILE"
    BEGIN_AFTER_SUBDIRECTORY = "### BEGIN AFTER SUBDIRECTORY"
    END_AFTER_SUBDIRECTORY = "### END AFTER SUBDIRECTORY"
    BEGIN_AFTER_CXX_VERSION = "### BEGIN AFTER CXX VERSION"
    END_AFTER_CXX_VERSION = "### END AFTER CXX VERSION"
    BEGIN_AFTER_CPACK = "### BEGIN AFTER CPACK"
    END_AFTER_CPACK = "### END AFTER CPACK"

    after_starting_str = get_extra_config_str(
        BEGIN_AFTER_STARTING, END_AFTER_STARTING, configs
    )
    after_packages_str = get_extra_config_str(
        BEGIN_AFTER_PACKAGES, END_AFTER_PACKAGES, configs
    )
    after_headers_str = get_extra_config_str(
        BEGIN_AFTER_HEADERS, END_AFTER_HEADERS, configs
    )
    after_sources_str = get_extra_config_str(
        BEGIN_AFTER_SOURCES, END_AFTER_SOURCES, configs
    )
    after_executable_str = get_extra_config_str(
        BEGIN_AFTER_EXECUTABLE, END_AFTER_EXECUTABLE, configs
    )
    after_precompile_str = get_extra_config_str(
        BEGIN_AFTER_PRECOMPILE, END_AFTER_PRECOMPILE, configs
    )
    after_subdirectory_str = get_extra_config_str(
        BEGIN_AFTER_SUBDIRECTORY, END_AFTER_SUBDIRECTORY, configs
    )
    after_cxx_version_str = get_extra_config_str(
        BEGIN_AFTER_CXX_VERSION, END_AFTER_CXX_VERSION, configs
    )
    after_cpack_str = get_extra_config_str(BEGIN_AFTER_CPACK, END_AFTER_CPACK, configs)

    return ExtraConfigs(
        after_starting_str,
        after_packages_str,
        after_headers_str,
        after_sources_str,
        after_executable_str,
        after_precompile_str,
        after_subdirectory_str,
        after_cxx_version_str,
        after_cpack_str,
    )
