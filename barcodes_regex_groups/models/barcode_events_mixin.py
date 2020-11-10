# -*- coding: utf-8 -*-
# Copyright 2020 Sunflower IT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BarcodeEventsMixin(models.AbstractModel):
    _inherit = 'barcodes.barcode_events_mixin'

    _barcode_match_current = fields.Integer(store=False)
    _barcode_match_target = fields.Integer(store=False)

    @api.onchange('_barcode_scanned')
    def _on_barcode_scanned(self):
        self._barcode_match_current = 0
        self._barcode_match_target = 0

        # Try until it really fails
        barcode_match_target = 0
        print self._name
        while True:
            ret = super(BarcodeEventsMixin, self)._on_barcode_scanned()
            print self._barcode_match_target, ret
            if ret and 'warning' in ret and \
                    self._barcode_match_target > barcode_match_target:
                continue
            break
        return ret

