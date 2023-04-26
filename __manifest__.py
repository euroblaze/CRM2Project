{
    "name": "CRM2Project Module with Plausibility Checks",
    "version": "1.0",
    "category": "Sales",
    "summary": "Module to intake data from FormBuilder/Formio, perform plausibility checks on it and pass on to Projects module for further processes",
    "author": "Simplify-ERP™",
    "website": "https://simplify-erp.de",
    "depends": [
        "base",
        "sale_management",
        "project",
        "crm",
    ],
    "data": [
        # "security/ir.model.access.csv",
        # "views/plausibility_check_view.xml",
        "views/crm_lead.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
