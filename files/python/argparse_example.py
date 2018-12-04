#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Program description")
parser.add_argument("required_arg", help="Required argument")

parser.add_argument("optional_arg_1", nargs="?", default="", help="Optional argument 1")
parser.add_argument("optional_arg_2", nargs="?", default="", help="Optional argument 2")

parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], help="increase output verbosity")
parser.add_argument('-d', '--dont-do-something', dest='dont_do_something', action='store_true',
    default=False, help='Do not do something')

# Change *display* name of an argument
# Here it will display
# usage: argparse_example.py [-h] [-o optional_param_value] ...
#   ...
#   -o optional_param_value, --some-optional-param optional_param_value
#                         Some optional parameter (default: def-value)
# instead of
# usage: argparse_example.py [-h] [-o SOME_OPTIONAL_PARAM] ...
#   ...
#   -o SOME_OPTIONAL_PARAM, --some-optional-param SOME_OPTIONAL_PARAM
#                         Some optional parameter (default: def-value)
parser.add_argument("-o", "--some-optional-param", dest="some_optional_param", default="def-value",
    help='Some optional parameter (default: def-value)', metavar="optional_param_value")

options = parser.parse_args()
print("required_arg: " + options.required_arg)
print("optional_arg_1: " + options.optional_arg_1)
print("optional_arg_2: " + options.optional_arg_2)
print("dont_do_something: " + str(options.dont_do_something))
print("some_optional_param: " + options.some_optional_param)
