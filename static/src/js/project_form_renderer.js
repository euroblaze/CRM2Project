/** @odoo-module **/

import FormRenderer from 'web.FormRenderer';
import { _t, qweb } from 'web.core';
import Dialog from 'web.Dialog';
import rpc from 'web.rpc';

var ProjectFormRenderer = FormRenderer.extend({
    _renderStatusbarButtons: function (buttons) {
        if (!this.state.data.hide_open_form_button) {
            var self = this;
            const $openForm = $('<button class="btn btn-primary" type="button" role="button">Open Form</button>')
                .on('click', self._actionMarkField.bind(self));
            buttons.push($openForm)
        }
        var $statusbarButtons = $('<div>', {class: 'o_statusbar_buttons'});
        buttons.forEach(button => $statusbarButtons.append(button));
        return $statusbarButtons;
    },

    _sendToSalesperson() {
        const valueCheckbox = $.find('.check-box');
        let listValueCheckbox = [];
        valueCheckbox.map(el => listValueCheckbox.push({
            key: el.id,
            isChecked: el.checked,
            note: $(`textarea[data-key|=${el.getAttribute('data-key')}]`)[0].value
        }))
        let datas = [ ...this.context['data'] ];
        datas = datas.map((data, index) => Object.assign(data, listValueCheckbox[index])).filter(d => d.isChecked === true);
        let listDatas = [];
        datas.map(d => {
            let value = d.value;
            if (d.type === 'selectboxes') {
                value = "";
                Object.entries(d.value).forEach(entry => {
                    if (entry[1] === true)
                        if (!value) value = value + entry[0];
                        else value = value + ', ' + entry[0];
                });
            }
            listDatas.push({label: d.label, value: value, note: d.note})
        });
        debugger
        return rpc.query({
            model: 'project.project',
            method: 'action_send_to_salesperson',
            args: [, listDatas, document.getElementById("note").value, this.state.res_id],
            context: this.context,
        })
    },

    async _actionMarkField() {
        this.context = await rpc.query({
            model: 'project.project',
            method: 'get_data',
            args: [, this.state.res_id],
        });
        const $content = $(qweb.render('CRM2Project.pickField', {listData: this.context['data']}));
        let title = this.context['title'];
        let dialog = new Dialog(this, {
            title: title,
            $content: $content,
            buttons: [
                {
                    text: _t('Send to salesperson'),
                    close: true,
                    click: this._sendToSalesperson.bind(this),
                }
            ],
        });
        dialog.open();
    },
});

export default ProjectFormRenderer;