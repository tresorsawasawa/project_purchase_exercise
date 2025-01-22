{
    "name": "Av Project and Purchase",
    "version": "17.0.0.0",
    "summary": "Custom modifications for Project and Purchase modules",
    "description": """
        This module adds a 'Project Price' field to the Project module and restricts 
        project creation to Project Administrators. Additional purchase-related customizations can be added here.
    """,
    "author": "Tresor Sawasawa",
    "category": "Operations/Project",
    "depends": ["project", "purchase", "hr"],
    "data": [
        "views/project_project_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False, 
    "license": "LGPL-3",
}
