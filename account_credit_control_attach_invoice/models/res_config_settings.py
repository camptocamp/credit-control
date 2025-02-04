from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    credit_ctrl_print_invoice = fields.Boolean(
        related="company_id.credit_ctrl_print_invoice",
        string="Print credit control summary with invoices",
        readonly=False,
    )

    report_to_attach_id = fields.Many2one(
        related="company_id.report_to_attach_id",
        string="Report to attach",
        readonly=False,
        config_parameter="qr_report_id",
    )
