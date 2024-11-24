/** @odoo-module **/
import { Component } from "@odoo/owl";
import { ClearCurrent } from '@cf_hex_base/ViewMacroClient/ClearCurrent/ClearCurrent';
import { CurrentColor } from '@cf_hex_base/ViewMacroClient/CurrentColor/CurrentColor';
import { CurrentTiles } from '@cf_hex_base/ViewMacroClient/CurrentTiles/CurrentTiles';
import { AddQuadrant } from '@cf_hex_base/ViewMacroClient/AddQuadrant/AddQuadrant';
import { CurrentZoom } from '@cf_hex_base/ViewMacroClient/CurrentZoom/CurrentZoom';
import { CurrentMap } from '@cf_hex_base/ViewMacroClient/CurrentMap/CurrentMap';
import { ViewMacro } from '@cf_hex_base/ViewMacroClient/ViewMacro/ViewMacro';
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "@cf_hex_base/store";
const actionRegistry = registry.category("actions");

class ViewMacroClient extends Component {
    static template = "ViewMacroClient"
    static props = ["*"]
    static components = { CurrentColor, CurrentZoom, CurrentMap, CurrentTiles, ClearCurrent, ViewMacro, AddQuadrant };

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.store = useStore()
    }

    resetCurrentSelect_ClickOutside(event) {
        if (!event.target.closest('.hex')) {  // Check se l'elemento cliccato è fuori dalla macro_form
            this.store.resetCurrentSelect();
        }
    }
}

actionRegistry.add('ViewMacroClient', ViewMacroClient);
