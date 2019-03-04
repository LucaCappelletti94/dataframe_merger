cmake_minimum_required(VERSION 3.13)
project(untitled C)

set(CMAKE_C_STANDARD 99)


add_executable(column_alignment hungarian.c csvparser.c load_csv.c solve.c solve.h column_alignment.c column_alignment.h matrix.c matrix.h loss.c loss.h tarjan.c tarjan.h)