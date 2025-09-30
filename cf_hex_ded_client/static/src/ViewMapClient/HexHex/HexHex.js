/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { getAxesV1, getAxesV2 } from '@cf_hex_ded_client/utility/utils';
import { useStore } from "@cf_hex_ded_client/store";
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
            sml: this.props.sml,
            code: this.props.code,
            type: this.props.type,
            index: this.props.index,
            color: this.props.color,
            hex_asset_id: this.props.hex_asset_id
        })
    }

    getHexStyle() {
        const { row, col, index, color, type } = this.state;
        let pos = "";

        if (type === "v3_no_q") {
            pos = col % 2 === 0
                ? "margin: 1px 1px 0px -13px;"
                : "margin: -23px 1px 0px -13px;";
        } else if (index) {
            const { asse_x, asse_y } = getAxesV1(index, 0.95);
            pos = `top: ${asse_y}; left: ${asse_x};`;
        } else {
            const { asse_x, asse_y } = getAxesV2(row, col);
            pos = `top: ${asse_y}; left: ${asse_x};`;
        }

        return `background-color: ${color}; ${pos} `;
    }

    /**
     * Gestisce l'azione di click su un oggetto "hex":
     *  - Se currentTile è impostato cambio il tile_id del Hex,
     *  - Se currentBiome è impostato cambio il biome_id del Hex,
     *  - Altrimenti vado alla vista Form del Hex.
     */
    async onClick(){
        const tile_id = this.store.currentTile?.tile_id ?? null;
        if (this.store.currentBiome)
            this.changeBiomeHex(this.state.id)
        else if (tile_id){
            this.setAssetTiles(this.state.id)}
        else {
            this.goToViewForm(this.state.id)
        }
    }
    async changeBiomeHex(){
        const biome_id = this.store.currentBiome?.id ?? null;
        await this.orm.call("hex.hex", "change_hex_biome", [this.state.id, biome_id], {});
        console.log(this.store.currentBiome)
        this.state.color = this.store.currentBiome.color
    }

    /**
     * Cambia il tales selezionato settandolo con il currentTile, poi aggiorna la maparea.
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
