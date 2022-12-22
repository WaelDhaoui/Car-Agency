from odoo import models, fields, api


class Damage(models.TransientModel):
    _name = 'damage.wizard'
    _description = 'Damaged cars'

    note = fields.Char(string="Note", required=True)

    def action_launch(self):

        active_id = self._context.get('active_id')
        self.env['car.car'].browse(active_id).damage_state = True

        rec = self.env['car.car'].search([('damage_state', '=', True)])

        return rec.write({
            'state': 'damaged',
            'note_car': self.note
        })
