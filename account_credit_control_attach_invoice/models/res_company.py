from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    credit_ctrl_print_invoice = fields.Boolean(
        string="Print credit control summary with invoices",
        default=True,
    )
    report_to_attach_id = fields.Many2one(
        "ir.actions.report", string="Report to attach"
    )
