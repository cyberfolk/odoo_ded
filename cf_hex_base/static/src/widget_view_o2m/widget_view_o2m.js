/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { onWillStart, Component, useState } from "@odoo/owl";

export class viewFormO2m extends Component {
    static props = {model: { type: String }};
    static components = {}
    setup() {
        super.setup();
        const url = window.location.href;
        console.log(url)
        const model_path= new URLSearchParams(url.split('#')[1]).get('model')
        this.action = useService("action");
        this.model_prop= this.props.model
        this.model_parent_prop= this.props.model_parent
        this.invisible= this.model_prop === model_path || model_path !== this.model_parent_prop
        this.id= this.props.record.data.id
    };

    goToViewForm(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Record Form',            // Nome della finestra
            res_model: this.model_prop,     // Modello del record
            res_id: parseInt(this.id, 10),  // ID del record da aprire
            views: [[false, 'form']],
            target: 'current',              // Può essere 'current' o 'new'
        });
    }
}

viewFormO2m.template = "cf_hex_base.ViewFormO2m";
export const ViewFormO2m = {
    component: viewFormO2m,
    extractProps: ({ attrs }) => {
        return {model: attrs.model, model_parent: attrs.model_parent,};
    },
};
registry.category("fields").add("view_form_o2m", ViewFormO2m);
