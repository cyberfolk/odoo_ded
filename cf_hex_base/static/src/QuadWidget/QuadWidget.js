/** @odoo-module **/
import { xml, Component, onWillStart, useState, onWillUpdateProps} from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";
import { getAxesV1 } from '@cf_hex_base/utility/utils';
import { registry } from "@web/core/registry";
import { HexHex } from '@cf_hex_base/ViewMacroClient/HexHex/HexHex';
const fieldRegistry = registry.category("fields");

export class QuadField extends Component {
    static components = { HexHex };
    static template = "QuadWidget";

    setup() {
        super.setup();
        this.orm = useService("orm");
        let quad_id = this.props.record.resId

        onWillStart(async () => {
            this.quad = await this.get_json_quad(quad_id)
        });

        // Per aggiornare il QuadWidget quando passo al hex.quad successivo/precedente dentro una vista form
        onWillUpdateProps(async (nextProps) => {
            let quad_id = nextProps.record.resId
            this.quad = await this.get_json_quad(quad_id)
        });
    }

    get_json_quad(quad_id){
        const quad = this.orm.call("hex.quad", "get_json_quad", [], {'quad_id': quad_id})
        .then((result) => { return JSON.parse(result) })
        return quad
    }
}

export const quadField = {
    component: QuadField,
};

fieldRegistry.add("QuadWidget", quadField);
