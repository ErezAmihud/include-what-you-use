import unittest
import generate_mapping

REGEX_TEST_LIST = [
    ("#include <string>", "string"),  # sanity
    ('#include "sys"', None),  # ignore " includes
    ("#include <sys/socket>", "sys/socket"),  # sanity with folder
    ('#include "sys/socket"', None),  # ignore " includes also in folders
    ('std::cout << "echo a" >> something', None),  # sanity not include lines
    (
        "#include <aaa.h> // for >>",
        "aaa.h",
    ),  # making sure comments after include don't make problems
    (
        "#include <aaa.h> // for <>",
        "aaa.h",
    ),  # making sure comments after include don't make problems
    (
        "#include <aaa.h> // for <<",
        "aaa.h",
    ),  # making sure comments after include don't make problems
]


class TestIncludeRegex(unittest.TestCase):
    def test_include_regex(self):
        for include, result in REGEX_TEST_LIST:
            with self.subTest(
                msg="Check regex on line equal result", line=include, result=result
            ):
                self.assertEqual(generate_mapping.get_include(include), result)
