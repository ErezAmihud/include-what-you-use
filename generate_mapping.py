"""
Create a mapping for custom headers
"""
import re
import os
import json
import argparse

PUBLIC_HEADERS = [
        # get all from https://en.cppreference.com/w/cpp/header
    "array",
    "memory",
    "string",
]
INCLUDE_REGEX = re.compile("^#include [<](.+?)[>]")


def get_include(data):
    """
    Get line of text and return the include file it is pointing to.
    Works only on absolute includes (using < >)
    :returns: string if a match was found, None if a match is not found
    """
    res = INCLUDE_REGEX.search(data)
    if res:
        return res.group(1)


def get_file_includes(file_path):
    """
    Get a file and extract all the absolute includes from it
    :return: an iterator of all the includes
    """
    for line in open(file_path, "r"):
        include = get_include(line)
        if include:
            yield include


def parse_headers(root):
    return {"string": get_file_includes(os.path.join(root, "string"))}


def headers_to_imp(mappings):
    """
    Convert a mapping from public header to all it's private ones to the imp file format
    """
    output = []
    for public_header, private_headers in mappings.items():
        output.extend(
            {"include": [f"<{header}>", "private", f"<{public_header}>", "public"]}
            for header in private_headers if header not in PUBLIC_HEADERS
        )
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=str)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()
    mappings = parse_headers(args.root)
    imp_content = headers_to_imp(mappings)
    if args.output:
        json.dump(
            imp_content, open(args.output, "w")
        )
    else:
        print(imp_content)


if __name__ == "__main__":
    main()
