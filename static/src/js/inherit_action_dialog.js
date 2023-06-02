/** @odoo-module **/

import { ActionDialog } from "@web/webclient/actions/action_dialog";
import { patch } from "@web/core/utils/patch";
import rpc from 'web.rpc';

patch(ActionDialog.prototype, "inherit_action_dialog", {
    _sendToPm() {
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