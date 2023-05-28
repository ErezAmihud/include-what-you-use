"""
Create a mapping for custom headers
"""
import re
import os
import json
import argparse

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


def header_to_path(root, header):
    """
    Convert header to a full path (convert the / split to the os separator)
    """
    return os.path.join(root, *header.split("/"))


def parse_header(root, header, processed):
    """
    Parsed a header from the root directory
    """
    if not os.path.exists(
        header_to_path(root, header)
    ):  # header is not part of the root directory
        return None

    if header in processed:
        return
    processed.append(header)

    for i in (
        h
        for h in get_file_includes(os.path.join(root, *header.split("/")))
        if h not in PUBLIC_HEADERS and os.path.exists(os.path.join(root, h))
    ):
        yield i
        yield from parse_header(root, i, processed)


def parse_headers(root):
    mappings = {}
    for header in PUBLIC_HEADERS:
        mappings[header] = set(parse_header(root, header, []))
    return mappings


def headers_to_imp(mappings):
    """
    Convert a mapping from public header to all it's private ones to the imp file format
    """
    for public_header, private_headers in mappings.items():
        for private_header in private_headers:
            yield {
                "include": [
                    f"<{public_header}>",
                    "private",
                    f"<{public_header}>",
                    "public",
                ]
            }


def main():
    global PUBLIC_HEADERS
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=str)
    parser.add_argument("public_headers", type=str)
    parser.add_argument("-o", "--output", type=str, default=None)
    args = parser.parse_args()
    PUBLIC_HEADERS = list(l.strip() for l in open(args.public_headers, 'r')) 
    mappings = parse_headers(args.root)
    imp_content = list(headers_to_imp(mappings))
    if args.output:
        json.dump(imp_content, open(args.output, "w"))
    else:
        print(imp_content)


if __name__ == "__main__":
    main()
