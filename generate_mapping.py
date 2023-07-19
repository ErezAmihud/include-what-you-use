"""
Create a mapping for custom headers
"""
import re
import os
import json
import argparse

INCLUDE_REGEX = re.compile("^#include [<](.+?)[>]")


def get_include_from_line(data):
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
        include = get_include_from_line(line)
        if include:
            yield include


def header_to_path(root, header):
    """
    Convert header to a full path (convert the / split to the os separator)
    """
    return os.path.join(root, *header.split("/"))


def parse_header(root, header, processed):
    """
    Parse a header from the root directory
    """
    if not os.path.exists(
        header_to_path(root, header)
    ):  # header is not part of the root directory
        return None

    if header in processed:
        return
    processed.append(header)
    for h in get_file_includes(header_to_path(root, header)):
        yield h
        yield from parse_header(root, h, processed)


def parse_headers(root, public_headers):
    mappings = {}
    processed = list(public_headers)
    for header in public_headers:
        mappings[header] = set(parse_header(root, header, processed))
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
                    "public",
                    f"<{private_header}>",
                    "private",
                ]
            }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=str)
    parser.add_argument("public_headers", type=str)
    parser.add_argument("-o", "--output", type=str, default=None)
    args = parser.parse_args()
    public_headers = list(l.strip() for l in open(args.public_headers, 'r')) 
    mappings = parse_headers(args.root, public_headers)
    imp_content = list(headers_to_imp(mappings))
    if args.output:
        json.dump(imp_content, open(args.output, "w"), indent=2)
    else:
        print(imp_content)


if __name__ == "__main__":
    main()
