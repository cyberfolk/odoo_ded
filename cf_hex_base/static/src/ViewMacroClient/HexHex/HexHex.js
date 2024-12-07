/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { getAxesV1, getAxesV2 } from '@cf_hex_base/utility/utils';
import { useStore } from "@cf_hex_base/store";
import { useService } from "@web/core/utils/hooks";

export class HexHex extends Component {
    static template = "HexHex"
    static props = ["*"]

    setup() {
        super.setup();
        this.orm = useService("orm")
        this.action = useService("action");
        this.store = useStore()
        this.state = useState({
            id: this.props.id,
            row: this.props.row,
            col: this.props.col,
            dim: this.props.dim,
            code: this.props.code,
            index: this.props.index,
            color: this.props.color,
            hex_asset_id: this.props.hex_asset_id
        })
    }

    getHexStyle() {
        const { row, col, index, color } = this.state;
        const { asse_x, asse_y } = index ? getAxesV1(index, 0.95) : getAxesV2(row, col);
        return `top: ${asse_y}; left: ${asse_x}; background-color: ${color};`;
    }

    /**
     * Gestisce l'azione di click su un oggetto "hex":
     *  apre il form del "hex" se non è presente un colore corrente,
     *  altrimenti cambia il colore del "hex".
     */
    async onClick(){
        const tile_id = this.store.currentTile?.tile_id ?? null;
        if (this.store.currentColor)
            this.changeColorHex(this.state.id)
        else if (tile_id){
            this.setAssetTiles(this.state.id)}
        else {
            this.goToViewForm(this.state.id)
        }
    }
    async changeColorHex(){
        await this.orm.call("hex.hex", "change_hex_color", [this.state.id, this.store.currentColor], {});
        this.state.color = this.store.currentColor
    }

    /**
     * Cambia il tales selezionato settandolo con il currentTile, poi aggiorna la macroarea.
     */
    async setAssetTiles(){
        await this.orm.call("hex.hex", "set_asset_tiles", [this.state.id , this.store.currentTile], {});
        const { rotation, tile_id } = this.store.currentTile;
        this.state.hex_asset_id = { rotation, tile_id };
    }


        /**
    * Apre la view-form del hex_id passato.
    */
    goToViewForm(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Form View',
            res_model: 'hex.hex',
            res_id: this.state.id,
            views: [[false, 'form']],
            target: 'current'
        });
    }
}
