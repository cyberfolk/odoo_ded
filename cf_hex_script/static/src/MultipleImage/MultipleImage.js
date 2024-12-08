/** @odoo-module **/
import { xml, Component, onWillStart, useState, onWillUpdateProps} from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
const fieldRegistry = registry.category("fields");

export class ImageField extends Component {
    static components = { };
    static template = "MultipleImage";
    static props = ["*"]

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.state = useState({
            imageIds: this.props.record.data.image_secondary_ids?._currentIds ?? null,
        })
        console.log(this.state.imageIds)
    }
}

export const imageField = {
    component: ImageField,
};

fieldRegistry.add("MultipleImage", imageField);
