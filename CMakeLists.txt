## CMakeLists.txt: top-level CMake file for MiKTeX packaging
##
## Licensed to you under the MIT license.  See the LICENSE file in
## the project root for more information.

cmake_minimum_required(VERSION 3.2.1 FATAL_ERROR)

project(miktex-packaging NONE)

set(required_programs
   diff
   md5walk
   rsync
   tar
   tdsutil
   unzip
)

if(WIN32 AND NOT UNIX)
  list(APPEND required_programs
    unix2dos
  )
endif()

foreach(p ${required_programs})
  string(TOUPPER "${p}" p_u)
  find_program(${p_u}_EXECUTABLE NAMES ${p})
  if(NOT ${p_u}_EXECUTABLE)
    message(FATAL_ERROR "The program ${p} could not be found.")
  endif()
endforeach()

if(DEFINED ENV{MIKTEX_CTAN_MIRROR})
  set(miktex_ctan_mirror_ $ENV{MIKTEX_CTAN_MIRROR})
elseif(DEFINED ENV{CTAN})
  set(miktex_ctan_mirror_ $ENV{CTAN})
else()
  set(miktex_ctan_mirror_ "/path/to/ctan_mirror")
endif()

set(
  MIKTEX_CTAN_MIRROR
  ${miktex_ctan_mirror_}
  CACHE PATH
  "The path to the root directory of a local CTAN mirror."
)

if(DEFINED ENV{MIKTEX_TEX_CATALOGUE})
  set(miktex_tex_catalogue_ $ENV{MIKTEX_TEX_CATALOGUE})
elseif(DEFINED ENV{TEX_CATALOGUE})
  set(miktex_tex_catalogue_ $ENV{TEX_CATALOGUE})
else()
  set(miktex_tex_catalogue_ "/path/to/tex_catalogue")
endif()

set(
  MIKTEX_TEX_CATALOGUE
  ${miktex_tex_catalogue_}
  CACHE PATH
  "The path to the TeX catalogue entries."
)

if(DEFINED ENV{MIKTEX_PACKAGE_STAGING_ROOT})
  set(miktex_package_staging_root_ $ENV{MIKTEX_PACKAGE_STAGING_ROOT})
else()
  set(miktex_package_staging_root_ "/path/to/miktex_package_staging_root")
endif()

set(
  MIKTEX_PACKAGE_STAGING_ROOT
  ${miktex_package_staging_root_}
  CACHE PATH
  "The path to the root directory of the MiKTeX package staging area."
)

configure_file(
  ${CMAKE_SOURCE_DIR}/setvars.cmd.in
  ${CMAKE_BINARY_DIR}/setvars.cmd
)

configure_file(
  ${CMAKE_SOURCE_DIR}/setvars.sh.in
  ${CMAKE_BINARY_DIR}/setvars.sh
  @ONLY
)

configure_file(
  ${CMAKE_SOURCE_DIR}/python/miktex/packaging/settings/paths.py.in
  ${CMAKE_BINARY_DIR}/python2/miktex/packaging/settings/paths.py
)

configure_file(
  ${CMAKE_SOURCE_DIR}/python/miktex/packaging/settings/__init__.py.in
  ${CMAKE_BINARY_DIR}/python2/miktex/packaging/settings/__init__.py
)

configure_file(
  ${CMAKE_SOURCE_DIR}/python/miktex/packaging/__init__.py.in
  ${CMAKE_BINARY_DIR}/python2/miktex/packaging/__init__.py
)

configure_file(
  ${CMAKE_SOURCE_DIR}/python/miktex/__init__.py.in
  ${CMAKE_BINARY_DIR}/python2/miktex/__init__.py
)
