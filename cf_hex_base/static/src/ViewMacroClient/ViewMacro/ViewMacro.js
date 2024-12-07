/** @odoo-module **/
import { Component } from "@odoo/owl";
import { HexHex } from '@cf_hex_base/ViewMacroClient/HexHex/HexHex';
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { getAxesV1, getAxesV2, POLYGON_QUAD_V1_LIST } from '@cf_hex_base/utility/utils';
import { store, useStore } from "@cf_hex_base/store";
const actionRegistry = registry.category("actions");

export class ViewMacro extends Component {
    static template = "ViewMacro"
    static props = ["*"]
    static components = { HexHex };

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.store = useStore({
            macro: null,
        })
    }

    getQuadStyleV1(quad) {
        const index = quad.index
        const { asse_x, asse_y } = getAxesV1(index, 0.97);
        const quadPath = POLYGON_QUAD_V1_LIST[index -1];
        return `top: ${asse_y}; left: ${asse_x}; z-index: ${20 - index}; clip-path: ${quadPath};`;
    }
}
