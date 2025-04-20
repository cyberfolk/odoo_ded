/** @odoo-module **/
import { Component } from "@odoo/owl";
import { ClearCurrent } from '@cf_hex_ded_client/ViewMapClient/ClearCurrent/ClearCurrent';
import { CurrentBiome } from '@cf_hex_ded_client/ViewMapClient/CurrentBiome/CurrentBiome';
import { CurrentTiles } from '@cf_hex_ded_client/ViewMapClient/CurrentTiles/CurrentTiles';
import { AddQuadrant } from '@cf_hex_ded_client/ViewMapClient/AddQuadrant/AddQuadrant';
import { CurrentZoom } from '@cf_hex_ded_client/ViewMapClient/CurrentZoom/CurrentZoom';
import { CurrentMap } from '@cf_hex_ded_client/ViewMapClient/CurrentMap/CurrentMap';
import { HideShow } from '@cf_hex_ded_client/ViewMapClient/HideShow/HideShow';
import { ViewMap } from '@cf_hex_ded_client/ViewMapClient/ViewMap/ViewMap';
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { store, useStore } from "@cf_hex_ded_client/store";
const actionRegistry = registry.category("actions");

class ViewMapClient extends Component {
    static template = "ViewMapClient"
    static props = ["*"]
    static components = {
        CurrentBiome, CurrentZoom, CurrentMap, CurrentTiles, ClearCurrent, ViewMap, AddQuadrant, HideShow
    };

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.store = useStore()
    }

    resetCurrentSelect_ClickOutside(event) {
        if (!event.target.closest('.hex')) {  // Check se l'elemento cliccato è fuori dalla map_form
            this.store.resetCurrentSelect();
        }
    }
}

actionRegistry.add('ViewMapClient', ViewMapClient);
