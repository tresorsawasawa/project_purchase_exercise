{
    "name": "Av Purchase",
    "version": "17.0.0.0",
    "summary": "Custom modifications for Purchase module.",
    "description": """
        This module adds a new functionalities to the Purchase module of Odoo.
    """,
    "author": "Tresor Sawasawa",
    "category": "Operations/Purchase",
    "depends": ["Purchase", "hr"],
    "data": [
        # Security
        "security/ir.model.access.csv",
        "security/res_groups.xml",

        # Views
        "views/Purchase",_Purchase",_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False, 
    "license": "LGPL-3",
}
