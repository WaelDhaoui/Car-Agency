from odoo import models, fields, api


class CarBrand(models.Model):
    _name = "car.brand"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Car Brand'

    name = fields.Char(string="Name Of Brand", required=True)
    image = fields.Image(string='Image')
    desc = fields.Char(string="description")
    agency_id = fields.Many2one("car.agency", string='Agency', required=True)

