cmake_minimum_required(VERSION 3.13)
project(Column_alignment C)

set(CMAKE_C_STANDARD 99)

FILE(GLOB MyCSources *.c)
file(GLOB_RECURSE SOURCES RELATIVE ${CMAKE_SOURCE_DIR} "src/*.c")
ADD_EXECUTABLE(column_alignment ${SOURCES})