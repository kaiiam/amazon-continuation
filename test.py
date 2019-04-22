#!/usr/bin/env python3
"""tests for amazon_xml_parser.py"""

import os.path
import re
from subprocess import getstatusoutput, getoutput

# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['', '-h', '--help']:
        out = getoutput('./amazon_xml_parser.py {}'.format(flag))
        assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_bad_input():
    """fails on bad input"""

    rv1, out1 = getstatusoutput('./amazon_xml_parser.py foo')
    assert rv1 > 0
    assert re.search('is not a file', out1)


# --------------------------------------------------
def test_good_input2():
    """works on good input"""
    assert os.path.isfile('Dissolved_Inorganic_carbon_profile.png')

    rv, out = getstatusoutput('./amazon_xml_parser.py biosample_result.xml')
    assert rv == 0
    tmpl = 'see Dissolved_Oxygen_profile.png\nsee Dissolved_Inorganic_carbon_profile.png'
    assert out == tmpl
