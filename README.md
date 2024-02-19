# auto-cmake

CMakeLists.txt file creation automation written in Python.

## Config file

|      Variable      | Definition                                                                         |
| :----------------: | :--------------------------------------------------------------------------------- |
|    project_name    | Sets the project name                                                              |
|  project_version   | Sets the project version                                                           |
|   configuration    | Sets the project's configuration. Debug or Release for examples                    |
| required packages  | Sets the ```find_package``` variables. This packages are set with __REQUIRED__ tag |
|      includes      | Gather header files (*.h, *.hpp) files from the specified directoriess             |
|      sources       | Gather source files (*.c, *.cpp) files from the specified directories              |
|    project_type    | Sets the project type which are __win32__, __executable__ or __library__           |
| precompile_headers | Adds specified standard libraries to **target_precompile_headers** function        |
| subdirectory_path  | Sets the additional CMakeLists.txt project as **add_subdirectory**                 |
|    cxx_version     | Sets the cpp version                                                               |
|  extra_cmake_path  | Sets the path for extra_cmake.txt                                                  |

- __includes__ and __sources__ variables have three additional variables:
    - As default the program is search for files as recursive from the working directory
    - Recursive search results are relative path to working directory
    - **include_dirs** : The program is going to search files from these directories. At least one specified directory disables the recursive search
    - **exclude_dirs** : The program exclude the specified directories from the recursive search
    - **exclude_files** : The program exclude the specified files from the recursive search result

- The header and library variables from the packages that are specified in the **required_packages** are added automatically to **include_directories** and **target_link_libraries** functions
- The subdirectories under the **subdirectory_path** are added automatically to **target_link_libraries**

### Extra CMake

- extra_cmake.txt file contains the additional CMake functions or declarations
- There are nine places that new arguments can be inserted:
    - ```AFTER STARTING``` : After the **configuration** variable
    - ```AFTER PACKAGES``` : After the **required_packages** variable
    - ```AFTER HEADERS``` : After the **include_directories** function
    - ```AFTER SOURCES``` : After the **set(SOURCE_FILES)** function
    - ```AFTER EXECUTABLE``` : After the **target_link_libraries** function
    - ```AFTER PRECOMPILE``` : After the **target_precompile_headers** function
    - ```AFTER SUBDIRECTORY``` : After the **add_subdirectory** functions
    - ```AFTER CXX VERSION``` : After the **cxx_version** variable
    - ```AFTER CPACK``` : After the CPack declarations

- The definition must start with ```### BEGIN``` and follow with place name. For example ```### BEGIN AFTER STARTING```
- The definition must end with ```### END``` and follow with place name. For example ```### END AFTER STARTING```
- For example:
<pre>
### BEGIN AFTER STARTING

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmakes")

### END AFTER STARTING
</pre>

## CLI Arguments

| Command | Definition                         |
| :-----: | :--------------------------------- |
| verbose | Enable additional terminal outputs |