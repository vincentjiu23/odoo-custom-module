# -*- coding: utf-8 -*-
{
    'name': 'Odoo Custom Module',
    'version': '17.0.1.0.0',
    'summary': 'Comprehensive Custom Module Template and Management System for Odoo',
    'description': """
Odoo Custom Module
==================
A production-ready custom module template providing a robust foundation for custom ERP workflows:
- Automated Sequence Numbering (e.g. CUST/YYYY/XXXX)
- Multi-state workflow lifecycle (Draft, In Progress, Approved, Done, Cancelled)
- Chatter integration with followers, activities, and audit message log
- Priority rating and dynamic tag classification
- Multi-currency monetary tracking
- Advanced search filters and grouping
- Interactive Tree, Form, and Kanban views
- Batch update Wizard for streamlined administrative tasks
- Printable QWeb PDF reports with company branding
- Granular Security Groups (User & Manager) with access control lists and record rules
- REST/JSON API endpoint controller example
    """,
    'category': 'Customizations/Management',
    'author': 'Vincent Jiu',
    'website': 'https://github.com/vincentjiu23/odoo-custom-module',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/custom_record_views.xml',
        'views/custom_tag_views.xml',
        'wizard/custom_record_wizard_views.xml',
        'report/custom_record_report.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
