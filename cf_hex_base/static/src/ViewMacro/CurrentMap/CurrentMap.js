/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "../../store";

export class CurrentMap extends Component {
    static template = "CurrentMap"
    static props = ["*"]

    setup() {
        super.setup();
        this.store = useStore()
        this.store.add({
            mapList: null,
            currentMap: 1,
        })
        this.orm = useService("orm");

        onWillStart(async () => {
            store.mapList = await this.orm.call("hex.macro", "get_json_map_list", [], {})
                .then((result) => { return JSON.parse(result) })
        })
    }
    async onChange(event) {
        this.store.currentMap = event.target.value;
        this.store.macro = await this.orm.call("hex.macro", "get_json_macro", [this.store.currentMap], {})
            .then((result) => { return JSON.parse(result) })
    }
}
