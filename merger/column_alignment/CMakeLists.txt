cmake_minimum_required(VERSION 3.13)
project(untitled C)

set(CMAKE_C_STANDARD 99)


add_executable(column_alignment hungarian/hungarian.c csv/csvparser.c load_csv.c assignment.c assignment.h column_alignment.c column_alignment.h matrix.c matrix.h tarjan.c tarjan.h threshold.c threshold.h double.c double.h vector.c vector.h int.c int.h)