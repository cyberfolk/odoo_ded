/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";

const fieldRegistry = registry.category("fields");

export class PxField extends Component {
    static components = {  };
    static template = "PxWidget";

    setup() {
        const { record, name } = this.props;
        this.state = useState({
            valueFormatted: record?.data?.[name] ? `${record?.data?.[name]} px` : ""
        })
        this.value = record?.data?.[name]
    }
}

export const pxField = {
    component: PxField,
};

fieldRegistry.add("PxWidget", pxField);
