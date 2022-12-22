from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Car(models.Model):
    _name = "car.car"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Car'
    _rec_name = "car_model"

    reg_num = fields.Char(string="Registration Number", required=True)
    mileage = fields.Float(string="mileage")

    start_date = fields.Date(string='Start Date', default=lambda self: fields.Datetime.now())
    end_date = fields.Date(string='End Date', default=lambda self: fields.Datetime.now())
    car_model = fields.Many2one('car.brand')

    # tache 2
    cin = fields.Integer(string="CIN")

    # tache 4
    note_car = fields.Char(string="Note")
    # State sequence
    state = fields.Selection([('available', 'Available'),
                              ('rented', 'Rented'),
                              ('damaged', 'Damaged')])

    damage_state = fields.Boolean(string="Car_state")

    # # Number sequence
    car_seq = fields.Char(string="Order Reference", required=True, copy=False, readonly=True,
                          index=True, default=lambda self: _('New'))

    # Customer
    customer_id = fields.Many2one("res.partner", string="Customer")

    model_ids = fields.One2many(
        "car.car.details", 'model_id'
    )

    @api.model
    def create(self, vals):
        if vals.get('car_seq', _('New') == _('New')):
            vals['car_seq'] = self.env['ir.sequence'].next_by_code('car.car') or _('New')
        result = super(Car, self).create(vals)
        return result

    @api.constrains('reg_num')
    def _check_reg_num_length(self):
        if len(self.reg_num) != 8:
            raise models.ValidationError('Registration number must be 8')
        for rec in self.reg_num:
            if rec != '0' and rec != '1' and rec != '2' and rec != '3' and rec != '4' and rec != '5' and rec != '6' and rec != '7' and rec != '8' and rec != '9':
                raise models.ValidationError('Registration number must be positive number')

    _sql_constraints = [
        (
            'code_reg_num_uniq',
            'unique(reg_num)',
            'Registration number must be unique per car !'
        ),
    ]

    def button_undamaged_cars(self):
        return self.write({
            'state': 'available',
            'damage_state': False,
            'note_car': ''
        })

    def button_rented_cars(self):
        return self.write({
            'state': 'rented',
        })

    def button_available_cars(self):
        return self.write({
            'state': 'available',
        })


class CarDetails(models.Model):
    _name = "car.car.details"
    _description = 'Car Details'

    model_id = fields.Many2one('car.car')
    status = fields.Selection(related="model_id.state")

    list_id = fields.Many2one('car.agency')


class Customer(models.Model):
    _inherit = 'res.partner'

    cin = fields.Integer(string="CIN")
