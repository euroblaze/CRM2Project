/** @odoo-module **/

import { ActionDialog } from "@web/webclient/actions/action_dialog";
import { patch } from "@web/core/utils/patch";
import { _t, qweb } from 'web.core';
import Dialog from 'web.Dialog';
import rpc from 'web.rpc';

patch(ActionDialog.prototype, "inherit_action_dialog", {
    // _actionSendMessage() {
    //     this.env.services.action.doAction({
    //         res_model: 'wizard.send.message',
    //         name: 'Send messages to salesperson',
    //         type: "ir.actions.act_window",
    //         views: [[false, "form"]],
    //         view_mode: "form",
    //         target: "new",
    //         context: this.props.actionProps.context,
    //     });
    // },

    _sendToSalesperson() {
        const valueCheckbox = this.$content.find('.check-box');
        let listValueCheckbox = [];
        valueCheckbox.map(el => listValueCheckbox.push({key: valueCheckbox[el].id, isChecked: valueCheckbox[el].checked}))
        let datas = [ ...this.__parentedParent.data ];
        datas = datas.map(data => Object.assign(data, listValueCheckbox.find(value => value.key === data.key))).filter(d => d.isChecked === true);
        let listDatas = [];
        datas.map(d => listDatas.push({'label': d.label, 'value': d.value}))
        debugger
        return rpc.query({
            model: 'project.project',
            method: 'action_send_to_salesperson',
            args: [, listDatas, document.getElementById("note").value],
        });
    },

    async _actionMarkField() {
        this.data = this.props.actionProps.context['data'];
        const $content = $(qweb.render('CRM2Project.pickField', {listData: this.data}));
        let title = this.props.actionProps.context['title'];
        let dialog = new Dialog(this, {
            title: title,
            $content: $content,
            context: this.props.actionProps.context,
            buttons: [
                {
                    text: _t('Send to salesperson'),
                    close: true,
                    click: this._sendToSalesperson,
                }
            ],
        });
        dialog.open();
    },

    async _sendToPm() {
        return true;
    },
});