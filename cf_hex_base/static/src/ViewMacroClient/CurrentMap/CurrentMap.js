/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "@cf_hex_base/store";

export class CurrentMap extends Component {
    static template = "CurrentMap"
    static props = ["*"]

    setup() {
        super.setup();
        this.store = useStore()
        this.store.add({
            mapList: null,
            currentMapID: 1,
        })
        this.orm = useService("orm");

        onWillStart(async () => {
            this.store.mapList = await this.orm.call("hex.macro", "get_json_map_list", [], {})
                .then((result) => { return JSON.parse(result) })
            if (this.store.mapList[0]){
                this.store.currentMapID = this.store.mapList[0].id
                this.onChangeCurrentMapID()
            }
        })
    }

    async onChangeCurrentMapID() {
        this.store.currentMapID = parseInt(this.store.currentMapID, 10)
        this.store.macro = await this.orm.call("hex.macro", "get_json_macro", [this.store.currentMapID], {})
            .then((result) => { return JSON.parse(result) })
    }
}
