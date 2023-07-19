import argparse
import json

LINE_START_PREFIX = "{{dsc inc|cpp/header/dsc "
def get_headers(edit_file, output):
    with open(output, 'w') as f:
        for l in get_head(edit_file):
            f.write(l)
            f.write("\n")
    json.dump(list(get_head(edit_file)), open(output, 'w'))

def get_head(f):
    for line in open(f, 'r'):
        if line.startswith(LINE_START_PREFIX):
            yield line[len(LINE_START_PREFIX): -3]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()#help="go to https://en.cppreference.com/mwiki/index.php?title=cpp/header&action=edit and copy the text to file")
    parser.add_argument("cpp_desc_file")
    parser.add_argument("output")
    res = parser.parse_args()
    get_headers(res.cpp_desc_file, res.output)
