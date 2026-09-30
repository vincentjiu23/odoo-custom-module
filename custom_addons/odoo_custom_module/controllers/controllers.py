# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class CustomModuleController(http.Controller):

    @http.route('/api/custom_module/ping', type='json', auth='public', methods=['GET', 'POST'], csrf=False)
    def ping(self):
        """Health-check endpoint for custom module."""
        return {
            'status': 'success',
            'message': 'Custom Module API is running successfully',
            'version': '17.0.1.0.0',
        }

    @http.route('/api/custom_module/records', type='json', auth='user', methods=['POST'], csrf=False)
    def get_records(self, limit=10):
        """Fetch custom records for authenticated user."""
        records = request.env['custom.record'].search_read(
            [],
            ['id', 'name', 'title', 'state', 'amount', 'date'],
            limit=limit,
            order='id desc'
        )
        return {
            'status': 'success',
            'count': len(records),
            'records': records,
        }
