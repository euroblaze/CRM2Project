/** @odoo-module **/

import { ActionDialog } from "@web/webclient/actions/action_dialog";
import { patch } from "@web/core/utils/patch";
import { _t, qweb } from 'web.core';
import Dialog from 'web.Dialog';
import rpc from 'web.rpc';

patch(ActionDialog.prototype, "inherit_action_dialog", {

    _sendToSalesperson() {
        const valueCheckbox = this.$content.find('.check-box');
        let listValueCheckbox = [];
        valueCheckbox.map(el => listValueCheckbox.push({
            key: valueCheckbox[el].id,
            isChecked: valueCheckbox[el].checked,
            note: $(`textarea[data-key|=${valueCheckbox[el].getAttribute('data-key')}]`)[0].value
        }))
        let datas = [ ...this.__parentedParent.data ];
        datas = datas.map((data, index) => Object.assign(data, listValueCheckbox[index])).filter(d => d.isChecked === true);
        let listDatas = [];
        datas.map(d => listDatas.push({label: d.label, value: d.value, note: d.note}))
        return rpc.query({
            model: 'project.project',
            method: 'action_send_to_salesperson',
            args: [, listDatas, document.getElementById("note").value],
            context: this.__parentedParent.props.actionProps.context,
        }).then(function () {
            document.getElementById('button_close').click();
        });
    },

    async _actionMarkField() {
        this.data = this.props.actionProps.context['data'];
        const $content = $(qweb.render('CRM2Project.pickField', {listData: this.data}));
        let title = this.props.actionProps.context['title'];
        let dialog = new Dialog(this, {
            title: title,
            $content: $content,
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
        return rpc.query({
            model: 'crm.lead',
            method: 'action_send_to_pm',
            args: [[]],
            context: this.props.actionProps.context,
        }).then(function () {
            document.getElementById('button_close').click();
        });
    },

});