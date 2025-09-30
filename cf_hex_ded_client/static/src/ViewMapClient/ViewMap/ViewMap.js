/** @odoo-module **/
import { Component } from "@odoo/owl";
import { HexHex } from '@cf_hex_ded_client/ViewMapClient/HexHex/HexHex';
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { getAxesV1, getAxesV2, POLYGON_QUAD_V1_LIST } from '@cf_hex_ded_client/utility/utils';
import { store, useStore } from "@cf_hex_ded_client/store";
const actionRegistry = registry.category("actions");

export class ViewMap extends Component {
    static template = "ViewMap"
    static props = ["*"]
    static components = { HexHex };

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.store = useStore({
            map: null,
        })
    }

    getQuadStyleV1(quad) {
        const index = quad.index
        const { asse_x, asse_y } = getAxesV1(index, 0.97);
        const quadPath = POLYGON_QUAD_V1_LIST[index -1];
        return `top: ${asse_y}; left: ${asse_x}; z-index: ${20 - index}; clip-path: ${quadPath};`;
    }
    getBgStyleV3() {
        const polygon ="clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);"
        return polygon;
    }
}
