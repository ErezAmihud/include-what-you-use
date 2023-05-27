import unittest
import generate_mapping


class TestIncludeRegex(unittest.TestCase):
    def test_include_system(self):
        self.assertEqual(generate_mapping.get_include("#include <string>"), "string")

    def test_include_relative(self):
        self.assertEqual(generate_mapping.get_include('#include "sys"'), None)

    def test_include_system_multiple(self):
        self.assertEqual(
            generate_mapping.get_include("#include <sys/socket>"), "sys/socket"
        )

    def test_include_relative_multiple(self):
        self.assertEqual(generate_mapping.get_include('#include "sys/socket"'), None)

    def test_include_doesnot_exist(self):
        self.assertEqual(
            generate_mapping.get_include('std::cout << "echo a" >> something'), None
        )

    def test_multiple_ends(self):
        self.assertEqual(generate_mapping.get_include('#include <aaa.h> // for >>'), "aaa.h")


