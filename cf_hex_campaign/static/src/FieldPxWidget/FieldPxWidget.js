/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";

const fieldRegistry = registry.category("fields");

export class PxField extends Component {
    static components = {  };
    static template = "PxWidget";

    setup() {
        console.log(this);
        const { record, name } = this.props;
        this.value = record?.data?.[name]
    }

    get displayValue() {
        return this.value ? `${this.value} px` : "";
    }
}

export const pxField = {
    component: PxField,
};

fieldRegistry.add("PxWidget", pxField);
