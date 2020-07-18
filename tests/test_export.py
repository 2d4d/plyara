# Copyright 2020 plyara Maintainers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Unit tests for exporting model to valid YARA rules."""
import unittest

from plyara.model import Ruleset, Grouping, Import, Include, Rule, RuleTypes, RuleType, Tags, Tag, Meta, MetaDefinition
from plyara.model import Strings, StrDefinition, Modifiers, Modifier, Alphabet, Range, Condition
from plyara.model import Integer, Float, Hexadecimal, Boolean, Variable
from plyara.export import to_yara


class TestModelOutputToYARA(unittest.TestCase):
    """Tests each of the various parts of the model as output to valid YARA rules."""

    def test_basic_rule(self):
        """Test the most basic rule components."""
        rule = """rule test
{
    condition:
        true
}
"""

        model = Ruleset([
                        Rule('test', None, None, None, None, Condition([
                                                                       Boolean(True)
                                                                       ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_import(self):
        """Test import statement."""
        rule = """import "pe"

rule test
{
    condition:
        true
}
"""

        model = Ruleset([
                        Grouping([
                                 Import('pe')
                                 ]),
                        Rule('test', None, None, None, None, Condition([
                                                                       Boolean(True)
                                                                       ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_include(self):
        """Test include statement."""
        rule = """include "other.yar"

rule test
{
    condition:
        true
}
"""

        model = Ruleset([
                        Grouping([
                                 Include('other.yar')
                                 ]),
                        Rule('test', None, None, None, None, Condition([
                                                                       Boolean(True)
                                                                       ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_import_groupings(self):
        """Test grouping of import statements."""
        rule = """import "magic"
import "math"
import "pe"

rule test
{
    condition:
        true
}
"""

        model = Ruleset([
                        Grouping([
                                 Import('magic'),
                                 Import('math'),
                                 Import('pe')
                                 ]),
                        Rule('test', None, None, None, None, Condition([
                                                                       Boolean(True)
                                                                       ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_include_groupings(self):
        """Test grouping of include statements."""
        rule = """include "foo.yar"
include "bar.yar"
include "baz.yar"

rule test
{
    condition:
        true
}
"""

        model = Ruleset([
                        Grouping([
                                 Include('foo.yar'),
                                 Include('bar.yar'),
                                 Include('baz.yar')
                                 ]),
                        Rule('test', None, None, None, None, Condition([
                                                                       Boolean(True)
                                                                       ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_multiple_groupings(self):
        """Test grouping of include statements."""
        rule = """include "foo.yar"
include "bar.yar"
include "baz.yar"

import "magic"
import "math"
import "pe"

rule test
{
    condition:
        true
}
"""

        model = Ruleset([
                        Grouping([
                                 Include('foo.yar'),
                                 Include('bar.yar'),
                                 Include('baz.yar')
                                 ]),
                        Grouping([
                                 Import('magic'),
                                 Import('math'),
                                 Import('pe')
                                 ]),
                        Rule('test', None, None, None, None, Condition([
                                                                       Boolean(True)
                                                                       ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_meta_string_type(self):
        """Test a meta section entry of string type."""
        rule = """rule test
{
    meta:
        description = "This is a YARA rule."
    condition:
        false
}
"""

        model = Ruleset([
                        Rule('test', None, None, Meta([
                                                      MetaDefinition('description', 'string', 'This is a YARA rule.')
                                                      ]), None, Condition([
                                                                          Boolean(False)
                                                                          ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_meta_number_type(self):
        """Test a meta section entry of number type."""
        rule = """rule test
{
    meta:
        description = "This is a YARA rule."
        threat_level = 5
    condition:
        false
}
"""

        model = Ruleset([
                        Rule('test', None, None, Meta([
                                                      MetaDefinition('description',
                                                                     'string',
                                                                     'This is a YARA rule.'),
                                                      MetaDefinition('threat_level', 'number', 5)
                                                      ]), None, Condition([
                                                                          Boolean(False)
                                                                          ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_meta_boolean_type_false(self):
        """Test a meta section entry of false boolean type."""
        rule = """rule test
{
    meta:
        description = "This is a YARA rule."
        threat_level = 5
        in_the_wild = false
    condition:
        false
}
"""

        model = Ruleset([
                        Rule('test', None, None, Meta([
                                                      MetaDefinition('description',
                                                                     'string',
                                                                     'This is a YARA rule.'),
                                                      MetaDefinition('threat_level', 'number', 5),
                                                      MetaDefinition('in_the_wild', 'boolean', False)
                                                      ]), None, Condition([
                                                                          Boolean(False)
                                                                          ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_meta_boolean_type_true(self):
        """Test a meta section entry of true boolean type."""
        rule = """rule test
{
    meta:
        description = "This is a YARA rule."
        threat_level = 5
        in_the_wild = true
    condition:
        false
}
"""

        model = Ruleset([
                        Rule('test', None, None, Meta([
                                                      MetaDefinition('description',
                                                                     'string',
                                                                     'This is a YARA rule.'),
                                                      MetaDefinition('threat_level', 'number', 5),
                                                      MetaDefinition('in_the_wild', 'boolean', True)
                                                      ]), None, Condition([
                                                                          Boolean(False)
                                                                          ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_private_rule_keyword(self):
        """Test the private rule keyword."""
        rule = """private rule test
{
    meta:
        description = "This is a YARA rule."
    condition:
        false
}
"""

        model = Ruleset([
                        Rule('test', RuleTypes([
                                               RuleType('private')
                                               ]), None, Meta([
                                                              MetaDefinition('description',
                                                                             'string',
                                                                             'This is a YARA rule.')
                                                              ]), None, Condition([
                                                                                  Boolean(False)
                                                                                  ]))
                        ])
        self.assertEqual(rule, to_yara(model))

    def test_global_rule_keyword(self):
        """Test the global rule keyword."""
        rule = """global rule test
{
    meta:
        description = "This is a YARA rule."
    condition:
        false
}
"""

        model = Ruleset([
                        Rule('test', RuleTypes([
                                               RuleType('global')
                                               ]), None, Meta([
                                                              MetaDefinition('description',
                                                                             'string',
                                                                             'This is a YARA rule.')
                                                              ]), None, Condition([
                                                                                  Boolean(False)
                                                                                  ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_both_rule_keywords(self):
        """Test both private and global rule keywords."""
        rule = """private global rule test
{
    meta:
        description = "This is a YARA rule."
    condition:
        false
}
"""

        model = Ruleset([
                        Rule('test', RuleTypes([
                                               RuleType('private'),
                                               RuleType('global'),
                                               ]), None, Meta([
                                                              MetaDefinition('description',
                                                                             'string',
                                                                             'This is a YARA rule.')
                                                              ]), None, Condition([
                                                                                  Boolean(False)
                                                                                  ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_both_rule_keywords_global_first(self):
        """Test both private and global rule keywords with global first."""
        rule = """global private rule test
{
    meta:
        description = "This is a YARA rule."
    condition:
        false
}
"""

        model = Ruleset([
                        Rule('test', RuleTypes([
                                               RuleType('global'),
                                               RuleType('private'),
                                               ]), None, Meta([
                                                              MetaDefinition('description',
                                                                             'string',
                                                                             'This is a YARA rule.')
                                                              ]), None, Condition([
                                                                                  Boolean(False)
                                                                                  ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_one_tag(self):
        """Test rule with one tag."""
        rule = """rule test : OneTag
{
    meta:
        description = "This is a YARA rule."
    condition:
        false
}
"""

        model = Ruleset([
                        Rule('test', None, Tags([
                                                Tag('OneTag')
                                                ]), Meta([
                                                         MetaDefinition('description',
                                                                        'string',
                                                                        'This is a YARA rule.')
                                                         ]), None, Condition([
                                                                             Boolean(False)
                                                                             ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_two_tags(self):
        """Test rule with two tags."""
        rule = """rule test : OneTag TwoTag
{
    meta:
        description = "This is a YARA rule."
    condition:
        false
}
"""

        model = Ruleset([
                        Rule('test', None, Tags([
                                                Tag('OneTag'),
                                                Tag('TwoTag')
                                                ]), Meta([
                                                         MetaDefinition('description',
                                                                        'string',
                                                                        'This is a YARA rule.')
                                                         ]), None, Condition([
                                                                             Boolean(False)
                                                                             ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_text_string(self):
        """Test rule with one text string."""
        rule = """rule test
{
    meta:
        description = "This is a YARA rule."
        threat_level = 5
        in_the_wild = false
    strings:
        $a = "dummy1"
    condition:
        $a
}
"""

        model = Ruleset([
                        Rule('test', None, None, Meta([
                                                      MetaDefinition('description',
                                                                     'string',
                                                                     'This is a YARA rule.'),
                                                      MetaDefinition('threat_level', 'number', 5),
                                                      MetaDefinition('in_the_wild', 'boolean', False)
                                                      ]), Strings([
                                                                  StrDefinition('a', 'text', 'dummy1', None)
                                                                  ]), Condition([
                                                                                Variable('a', 'boolean')
                                                                                ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_hex_string(self):
        """Test rule with one hexadecimal string."""
        rule = """rule test
{
    meta:
        description = "This is a YARA rule."
        threat_level = 5
        in_the_wild = false
    strings:
        $a = { 4D 5A }
    condition:
        $a
}
"""

        model = Ruleset([
                        Rule('test', None, None, Meta([
                                                      MetaDefinition('description',
                                                                     'string',
                                                                     'This is a YARA rule.'),
                                                      MetaDefinition('threat_level', 'number', 5),
                                                      MetaDefinition('in_the_wild', 'boolean', False)
                                                      ]), Strings([
                                                                  StrDefinition('a', 'hex', '4D 5A', None)
                                                                  ]), Condition([
                                                                                Variable('a', 'boolean')
                                                                                ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_regex_string(self):
        """Test rule with one regular expression string."""
        rule = """rule test
{
    meta:
        description = "This is a YARA rule."
        threat_level = 5
        in_the_wild = false
    strings:
        $a = /md5: [0-9a-fA-F]{32}/
    condition:
        $a
}
"""

        model = Ruleset([
                        Rule('test', None, None, Meta([
                                                      MetaDefinition('description',
                                                                     'string',
                                                                     'This is a YARA rule.'),
                                                      MetaDefinition('threat_level', 'number', 5),
                                                      MetaDefinition('in_the_wild', 'boolean', False)
                                                      ]), Strings([
                                                                  StrDefinition('a',
                                                                                'regex',
                                                                                'md5: [0-9a-fA-F]{32}',
                                                                                None)
                                                                  ]), Condition([
                                                                                Variable('a', 'boolean')
                                                                                ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_string_modifier(self):
        """Test rule with one string with a modifier."""
        rule = """rule test
{
    meta:
        description = "This is a YARA rule."
        threat_level = 5
        in_the_wild = false
    strings:
        $a = "dummy1" nocase
    condition:
        $a
}
"""

        model = Ruleset([
                        Rule('test', None, None, Meta([
                                                      MetaDefinition('description',
                                                                     'string',
                                                                     'This is a YARA rule.'),
                                                      MetaDefinition('threat_level', 'number', 5),
                                                      MetaDefinition('in_the_wild', 'boolean', False)
                                                      ]), Strings([
                                                                  StrDefinition('a',
                                                                                'text',
                                                                                'dummy1',
                                                                                Modifiers([
                                                                                          Modifier('nocase', None)
                                                                                          ]))
                                                                  ]), Condition([
                                                                                Variable('a', 'boolean')
                                                                                ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_all_string_modifiers(self):
        """Test rules and iterate over all string modifiers."""
        modifier_keywords = ['nocase', 'wide', 'ascii', 'xor', 'base64', 'base64wide', 'fullword', 'private']

        rule_template = """rule test
{{
    meta:
        description = "This is a YARA rule."
        threat_level = 5
        in_the_wild = false
    strings:
        $a = "dummy1" {}
    condition:
        $a
}}
"""

        for keyword in modifier_keywords:
            base_model = Ruleset([
                                 Rule('test', None, None, Meta([
                                                               MetaDefinition('description',
                                                                              'string',
                                                                              'This is a YARA rule.'),
                                                               MetaDefinition('threat_level', 'number', 5),
                                                               MetaDefinition('in_the_wild', 'boolean', False)
                                                               ]), Strings([
                                                                           StrDefinition('a',
                                                                                         'text',
                                                                                         'dummy1',
                                                                                         Modifiers([
                                                                                                   Modifier(keyword,
                                                                                                            None)
                                                                                                   ]))
                                                                           ]), Condition([
                                                                                         Variable('a', 'boolean')
                                                                                         ]))
                                 ])

            self.assertEqual(rule_template.format(keyword), to_yara(base_model))

    def test_xor_parameter(self):
        """Test xor modifier with range parameter."""
        rule = """rule test
{
    meta:
        description = "This is a YARA rule."
        threat_level = 5
        in_the_wild = false
    strings:
        $a = "dummy1" xor(0x01-0xff)
    condition:
        $a
}
"""

        model = Ruleset([
                        Rule('test', None, None, Meta([
                                                      MetaDefinition('description',
                                                                     'string',
                                                                     'This is a YARA rule.'),
                                                      MetaDefinition('threat_level', 'number', 5),
                                                      MetaDefinition('in_the_wild', 'boolean', False)
                                                      ]), Strings([
                                                                  StrDefinition('a',
                                                                                'text',
                                                                                'dummy1',
                                                                                Modifiers([
                                                                                          Modifier('xor',
                                                                                                   Range('01', 'ff'))
                                                                                          ]))
                                                                  ]), Condition([
                                                                                Variable('a', 'boolean')
                                                                                ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_base64_parameter(self):
        """Test base64 modifier with alphabet parameter."""
        rule = r"""rule test
{
    meta:
        description = "This is a YARA rule."
        threat_level = 5
        in_the_wild = false
    strings:
        $a = "dummy1" base64("!@#$%^&*(){}[].,|ABCDEFGHIJ\x09LMNOPQRSTUVWXYZabcdefghijklmnopqrstu")
    condition:
        $a
}
"""

        alpha = r'!@#$%^&*(){}[].,|ABCDEFGHIJ\x09LMNOPQRSTUVWXYZabcdefghijklmnopqrstu'
        model = Ruleset([
                        Rule('test', None, None, Meta([
                                                      MetaDefinition('description',
                                                                     'string',
                                                                     'This is a YARA rule.'),
                                                      MetaDefinition('threat_level', 'number', 5),
                                                      MetaDefinition('in_the_wild', 'boolean', False)
                                                      ]), Strings([
                                                                  StrDefinition('a',
                                                                                'text',
                                                                                'dummy1',
                                                                                Modifiers([
                                                                                          Modifier('base64',
                                                                                                   Alphabet(alpha))
                                                                                          ]))
                                                                  ]), Condition([
                                                                                Variable('a', 'boolean')
                                                                                ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_boolean_variable(self):
        """Test condition with one boolean variable."""
        rule = """rule test
{
    strings:
        $a = "dummy1"
    condition:
        $a
}
"""

        model = Ruleset([
                        Rule('test', None, None, None, Strings([
                                                               StrDefinition('a', 'text', 'dummy1', None)
                                                               ]), Condition([
                                                                             Variable('a', 'boolean')
                                                                             ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_offset_variable(self):
        """Test condition with one offset variable."""
        rule = """rule test
{
    strings:
        $a = "dummy1"
    condition:
        @a
}
"""

        model = Ruleset([
                        Rule('test', None, None, None, Strings([
                                                               StrDefinition('a', 'text', 'dummy1', None)
                                                               ]), Condition([
                                                                             Variable('a', 'offset')
                                                                             ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_count_variable(self):
        """Test condition with one count variable."""
        rule = """rule test
{
    strings:
        $a = "dummy1"
    condition:
        #a
}
"""

        model = Ruleset([
                        Rule('test', None, None, None, Strings([
                                                               StrDefinition('a', 'text', 'dummy1', None)
                                                               ]), Condition([
                                                                             Variable('a', 'count')
                                                                             ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_length_variable(self):
        """Test condition with one length variable."""
        rule = """rule test
{
    strings:
        $a = "dummy1"
    condition:
        !a
}
"""

        model = Ruleset([
                        Rule('test', None, None, None, Strings([
                                                               StrDefinition('a', 'text', 'dummy1', None)
                                                               ]), Condition([
                                                                             Variable('a', 'length')
                                                                             ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_true_condition(self):
        """Test rule with true condition."""
        rule = """rule test
{
    condition:
        true
}
"""

        model = Ruleset([
                        Rule('test', None, None, None, None, Condition([
                                                                       Boolean(True)
                                                                       ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_false_condition(self):
        """Test rule with false condition."""
        rule = """rule test
{
    condition:
        false
}
"""

        model = Ruleset([
                        Rule('test', None, None, None, None, Condition([
                                                                       Boolean(False)
                                                                       ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_integer_condition(self):
        """Test rule with integer condition."""
        rule = """rule test
{
    condition:
        1
}
"""

        model = Ruleset([
                        Rule('test', None, None, None, None, Condition([
                                                                       Integer('1')
                                                                       ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_float_condition(self):
        """Test rule with float condition."""
        rule = """rule test
{
    condition:
        1.0
}
"""

        model = Ruleset([
                        Rule('test', None, None, None, None, Condition([
                                                                       Float('1.0')
                                                                       ]))
                        ])

        self.assertEqual(rule, to_yara(model))

    def test_hexadecimal_condition(self):
        """Test rule with hexadecimal condition."""
        rule = """rule test
{
    condition:
        0x01
}
"""

        model = Ruleset([
                        Rule('test', None, None, None, None, Condition([
                                                                       Hexadecimal('01')
                                                                       ]))
                        ])

        self.assertEqual(rule, to_yara(model))


class TestErrorsOutputToYARA(unittest.TestCase):
    """Tests error conditions in the output to valid YARA rules."""

    def test_unknown_obj(self):
        """Test single dispatch of completely unknown class."""

        class Unknown:
            """Completely unknown class."""

            pass

        model = Unknown()

        with self.assertRaises(RuntimeError):
            to_yara(model)

    def test_unknown_meta_type(self):
        """Test a meta section entry of unknown type."""
        model = Ruleset([
                        Rule('test', None, None, Meta([
                                                      MetaDefinition('description', 'foo', 'This is a YARA rule.')
                                                      ]), None, Condition([
                                                                          Boolean(False)
                                                                          ]))
                        ])

        with self.assertRaises(RuntimeError):
            to_yara(model)

    def test_unknown_string_type(self):
        """Test a strings section entry of unknown type."""
        model = Ruleset([
                        Rule('test', None, None, None, Strings([
                                                               StrDefinition('a', 'foo', 'dummy1', None)
                                                               ]), Condition([
                                                                             Boolean(False)
                                                                             ]))
                        ])

        with self.assertRaises(RuntimeError):
            to_yara(model)

    def test_unknown_variable_type(self):
        """Test a condition section variable of unknown type."""
        model = Ruleset([
                        Rule('test', None, None, None, Strings([
                                                               StrDefinition('a', 'text', 'dummy1', None)
                                                               ]), Condition([
                                                                             Variable('a', 'foo')
                                                                             ]))
                        ])

        with self.assertRaises(RuntimeError):
            to_yara(model)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
