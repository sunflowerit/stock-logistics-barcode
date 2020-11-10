# -*- coding: utf-8 -*-
# Copyright 2020 Sunflower IT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re
from typing import Match

from odoo import fields, models


class BarcodeNomenclature(models.Model):
    _inherit = 'barcode.nomenclature'

    def match_pattern(self, barcode, pattern):
        # If pattern ends with '(try)', we keep matching other rules
        # even if this rule matches
        print pattern
        _try = False
        if pattern and pattern.endswith('(try)'):
            pattern = pattern[:-5]
            _try = True

        match = super(BarcodeNomenclature, self).match_pattern(
            barcode, pattern)

        # We cannot use numerical content and matching groups at the same time
        numerical_content = re.search("[{][N]*[D]*[}]", pattern)
        if numerical_content:
            return match

        # If there are no regex groups in pattern, use normal matching
        has_regex_groups = re.search("[(].*[)]", pattern)
        if not has_regex_groups:
            return match

        # Perform pattern matching using 'search' instead of 'match'
        # And don't truncate barcode on search pattern length
        match['match'] = re.search(pattern, match['base_code'])

        # Abuse 'value' to store the result, since it goes to 'parsed_result'
        if match['match'] and self.env.context.get('barcodes_regex_groups'):
            #if _try and (match_counter[0] < match_counter[1]):
            #    match['match'] = None
            #    match_counter[0] += 1
            #else:
            match['value'] = {'match': match['match'], 'try': _try}
        print match
        return match

    def parse_barcode(self, barcode):
        print 'XXXX', barcode
        parsed_result = super(BarcodeNomenclature, self.with_context(
            barcodes_regex_groups=True
        )).parse_barcode(barcode)
        print 'YYYY'

        # Post-process any result of group-matching
        if isinstance(parsed_result['value'], dict):
            match = parsed_result['value']['match']
            _try = parsed_result['value']['try']
            parsed_result['value'] = 0
            parsed_result['code'] = match.group(1)
            print parsed_result
            if _try:
                print self._name

        return parsed_result
