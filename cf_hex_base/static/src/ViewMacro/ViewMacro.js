/** @odoo-module **/
import { ClearCurrent } from '@cf_hex_base/ViewMacro/ClearCurrent/ClearCurrent';
import { CurrentColor } from '@cf_hex_base/ViewMacro/CurrentColor/CurrentColor';
import { CurrentTiles } from '@cf_hex_base/ViewMacro/CurrentTiles/CurrentTiles';
import { CurrentZoom } from '@cf_hex_base/ViewMacro/CurrentZoom/CurrentZoom';
import { CurrentMap } from '@cf_hex_base/ViewMacro/CurrentMap/CurrentMap';
import { HexHex } from '@cf_hex_base/ViewMacro/HexHex/HexHex';
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { getAxesV1, getAxesV2, POLYGON_QUAD_V2, POLYGON_QUAD_V1_LIST } from '../utility/utils.js';
import { store, useStore } from "../store";
const actionRegistry = registry.category("actions");

class ViewMacro extends Component {
    static template = "ViewMacro"
    static props = ["*"]
    static components = { CurrentColor, CurrentZoom, CurrentMap, CurrentTiles, ClearCurrent, HexHex };

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.store = useStore({
            macro: null,
        })
    }

    getQuadStyle(quad) {
        const index = quad.index
        if (index) {
            return `${getAxesV1(index, 0.97)}; z-index: ${20 - index}; clip-path: ${POLYGON_QUAD_V1_LIST[index -1]};`;
        } else {
            return `clip-path: ${POLYGON_QUAD_V2}; margin-left: -10px`;
        }
    }

    resetCurrentSelect_ClickOutside(event) {
        if (!event.target.closest('.hex')) {  // Check se l'elemento cliccato è fuori dalla macro_form
            this.store.resetCurrentSelect();
        }
    }
    addRight(){
        this.orm.call("hex.macro", "add_right", [store.currentMapID], {})
             .then((result) => { this.store.macro = JSON.parse(result) })
    }

    addTop(){
        this.orm.call("hex.macro", "add_top", [store.currentMapID], {})
             .then((result) => { this.store.macro = JSON.parse(result) })
    }

    addBottom(){
        this.orm.call("hex.macro", "add_bottom", [store.currentMapID], {})
             .then((result) => { this.store.macro = JSON.parse(result) })
    }

    addLeft(){
        this.orm.call("hex.macro", "add_left", [store.currentMapID], {})
             .then((result) => { this.store.macro = JSON.parse(result) })
    }
}

actionRegistry.add('ViewMacro', ViewMacro);
