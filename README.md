Sumbission for langjam#0001

docco like tool to extract comments

first-class comments: treat comments as value type that is freely storable / serialisable ... like python dictionaries + pickle

loom is a tool along the lines docco that generates documentation from source code.
it also includes a translater that can strip comments and execute the resultant code.

also included is support for storing what code / comment sequences into a sqlite database to does some simple code analysis using sql and treating. one such analysis is number of lines of comment / lines of code.

