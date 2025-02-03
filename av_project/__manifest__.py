{
    "name": "Av Project",
    "version": "17.0.0.0",
    "summary": "Custom modifications for Project module.",
    "description": """
        This module adds a 'Project Amount', 'Departments' fields and other features to the Project module of Odoo.
    """,
    "author": "Tresor Sawasawa",
    "category": "Operations/Project",
    "depends": ["project", "hr"],
    "data": [
        "views/project_project_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False, 
    "license": "LGPL-3",
}
