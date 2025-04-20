/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "@cf_hex_ded_client/store";

export class CurrentBiome extends Component {
    static template = "CurrentBiome"
    static props = ["*"]

    setup() {
        super.setup();
        this.store = useStore()
        this.store.add({
            currentBiome: 0,
        })
        this.orm = useService("orm");

        onWillStart(async () => {
            this.store.biomeList = await this.orm.call("biome.biome", "get_json_biome_list", [], {})
                .then((result) => { return JSON.parse(result) })
        })
    }

    setCurrentBiome(biome){
        console.log(biome)
        this.store.resetCurrentSelect()
        this.store.currentBiome = biome
    }
}
