/** @odoo-module **/
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "@cf_hex_ded_client/store";

export class AddQuadrant extends Component {
    static template = "AddQuadrant"
    static props = ["*"]

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.store = useStore()
    }

    addRight(){
        this.orm.call("hex.map", "add_right", [this.store.currentMapID], {})
             .then((result) => { this.store.map = JSON.parse(result) })
    }

    addTop(){
        this.orm.call("hex.map", "add_top", [this.store.currentMapID], {})
             .then((result) => { this.store.map = JSON.parse(result) })
    }

    addBottom(){
        this.orm.call("hex.map", "add_bottom", [this.store.currentMapID], {})
             .then((result) => { this.store.map = JSON.parse(result) })
    }

    addLeft(){
        this.orm.call("hex.map", "add_left", [this.store.currentMapID], {})
             .then((result) => { this.store.map = JSON.parse(result) })
    }
}
