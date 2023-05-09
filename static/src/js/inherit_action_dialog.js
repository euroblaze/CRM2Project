/** @odoo-module **/

import { ActionDialog } from "@web/webclient/actions/action_dialog";
import { patch } from "@web/core/utils/patch";

patch(ActionDialog.prototype, "inherit_action_dialog", {
    _actionSendMessage() {
        this.env.services.action.doAction({
            res_model: 'wizard.send.message',
            name: 'Send messages to salesperson',
            type: "ir.actions.act_window",
            views: [[false, "form"]],
            view_mode: "form",
            target: "new",
            context: this.props.actionProps.context,
        });
    }
});