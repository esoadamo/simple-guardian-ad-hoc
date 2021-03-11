from unittest import TestCase, main
from lib import LogRule


class TestLogRule(TestCase):
    def test_regex_rule_generation(self):
        rule = LogRule("hello, my name is %name% and I'm %age%")
        self.assertEqual(rule.regex_rule, r"""^hello\,\ my\ name\ is\ (.+?)\ and\ I\'m\ (.+?)$""")

    def test_group_generation(self):
        rule = LogRule("hello, my name is %name% and I'm %age%")
        parsed = rule.parse_record("hello, my name is Adam and I'm 20")

        self.assertIsNotNone(parsed)
        self.assertIn('name', parsed)
        self.assertIn('age', parsed)
        self.assertEqual(parsed['name'], 'Adam')
        self.assertEqual(parsed['age'], '20')
        self.assertTrue(set(parsed.keys()) == {'name', 'age'})


if __name__ == '__main__':
    main()
