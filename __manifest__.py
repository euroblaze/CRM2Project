{
    "name": "CRM2Project Module",
    "version": "1.0",
    "category": "Sales",
    "summary": "Module to intake data from FormBuilder/Formio, perform plausibility checks on it and pass on to Projects module for further processes",
    "author": "Simplify-ERP™",
    "website": "https://simplify-erp.de",
    "depends": [
        "base",
        "sale_project",
        "crm",
        "formio",
    ],
    "data": [
        # "views/plausibility_check_view.xml",
        "data/formio_crm_data.xml",
        "views/crm_lead.xml",
        "views/formio_form_views.xml",
        "views/project.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
