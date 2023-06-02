/** @odoo-module **/

import FormView from 'web.FormView';
import view_registry from 'web.view_registry';
import ProjectFormRenderer from './project_form_renderer'

var ProjectFormView = FormView.extend({
    config: _.extend({}, FormView.prototype.config, {
        Renderer: ProjectFormRenderer,
    }),
});

view_registry.add('project_form_view', ProjectFormView);

export default ProjectFormView;
