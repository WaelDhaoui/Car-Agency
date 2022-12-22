from odoo import models, fields, api, _


class Agency(models.Model):
    _name = "car.agency"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Agency'
    _rec_name = "responsible_id"

    responsible_id = fields.Many2one('res.partner', string="Responsible", required=True)
    list_ids = fields.One2many(
        "car.car.details", 'list_id',
        string='Lists'
    )

    # # Number sequence
    name_seq = fields.Char(string="Order Reference", required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New') == _('New')):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('car.agency') or _('New')
        result = super(Agency, self).create(vals)
        return result

    # Start SMART BUTTON

    def action_smart_button_brand_car(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Car Brand'),
            'res_model': 'car.brand',
            'context': {},
            'domain': [('agency_id', '=', self.id)],
            'view_mode': 'list,form',
            'target': 'current',
        }

    # END SMART BUTTON
