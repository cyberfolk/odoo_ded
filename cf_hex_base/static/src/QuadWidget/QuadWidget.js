/** @odoo-module **/
import { xml, Component, onWillStart, useState, onWillUpdateProps} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { getAxesV1 } from '@cf_hex_base/utility/utils';
const fieldRegistry = registry.category("fields");

export class QuadField extends Component {
    static components = { };
    static template = "QuadWidget";

    setup() {
        super.setup();
        this.orm = useService("orm");
        let quad_id = this.props.record.resId

        onWillStart(async () => {
            this.quad = await this.get_json_quad(quad_id)
            this.external_hexs = await this.get_json_external_hexs(quad_id)
        });

        onWillUpdateProps(async (nextProps) => {
            let quad_id = nextProps.record.resId
            this.quad = await this.get_json_quad(quad_id)
            this.external_hexs = await this.get_json_external_hexs(quad_id)
        });
    }

    get_json_quad(quad_id){
        const quad = this.orm.call("hex.quad", "get_json_quad", [], {'quad_id': quad_id})
        .then((result) => { return JSON.parse(result) })
        return quad
    }

    get_json_external_hexs(quad_id){
        const external_hexs = this.orm.call("hex.quad", "get_json_external_hexs", [], {'quad_id': quad_id})
        .then((result) => { return JSON.parse(result) })
        return external_hexs
    }

    getHexStyle(hex) {
        const { asse_x, asse_y } = getAxesV1(hex.index, 0.95);
        return `top: ${asse_y}; left: ${asse_x}; background-color: ${hex.color};`
    }

    getHexMissingStyle(hex) {
        let index = hex.index + 6 ;
        index = index > 19 ? (hex.index - 6) : index;
        const { asse_x, asse_y } = getAxesV1(index, 0.95);
        return `top: ${asse_y}; left: ${asse_x}; background-color: #eeeeee;`
    }

    getMissingHexStyle(index) {
        const { asse_x, asse_y } = getAxesV1(index, 0.95);
        return `top: ${asse_y}; left: ${asse_x}; background-color: #eeeeee;`
    }
}

export const quadField = {
    component: QuadField,
};

fieldRegistry.add("QuadWidget", quadField);
