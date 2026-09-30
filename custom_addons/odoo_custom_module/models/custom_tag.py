# -*- coding: utf-8 -*-
from odoo import models, fields


class CustomTag(models.Model):
    _name = 'custom.tag'
    _description = 'Custom Tag'
    _order = 'name asc'

    name = fields.Char(
        string='Tag Name',
        required=True,
        translate=True,
    )
    color = fields.Integer(
        string='Color Index',
        help='Color index used for displaying the tag in Kanban/Form views.',
        default=10,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Tag name must be unique!'),
    ]
