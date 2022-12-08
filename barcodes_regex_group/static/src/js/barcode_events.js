odoo.define('barcodes_regex_group.BarcodeEvents', function (require) {
    "use strict";

    var BarcodeEvents = require('barcodes.BarcodeEvents').BarcodeEvents;

    BarcodeEvents.regexp = /(.{3,})/s;
    BarcodeEvents.suffix = /[\0]/;
});
