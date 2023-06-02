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
        "data/formio_crm_data.xml",
        "views/crm_lead.xml",
        "views/formio_form_views.xml",
        "views/project.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'CRM2Project/static/src/js/**/*',
        ],
        'web.assets_qweb': [
            'CRM2Project/static/src/xml/**/*',
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
