/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "@cf_hex_client/store";

export class HideShow extends Component {
    static template = "HideShow"
    static props = ["*"]

    setup() {
        super.setup();
        this.store = useStore()
        this.store.add({
            showHexCode: false,
            showHexSml: false,
        })
    }
}
