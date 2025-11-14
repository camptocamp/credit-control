# Copyright 2016-2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def evaluate_risk_message(self, partner):
        self.ensure_one()
        risk_amount = self.currency_id._convert(
            self.amount_total,
            partner.risk_currency_id,
            self.company_id,
            self.date_order
            and self.date_order.date()
            or fields.Date.context_today(self),
            round=False,
        )
        exception_msg = ""
        if partner.risk_exception:
            exception_msg = self.env._("Financial risk exceeded.\n")
        elif partner.risk_sale_order_limit and (
            (partner.risk_sale_order + risk_amount) > partner.risk_sale_order_limit
        ):
            exception_msg = self.env._(
                "This sale order exceeds the sales orders risk.\n"
            )
        elif partner.risk_sale_order_include and (
            (partner.risk_total + risk_amount) > partner.sudo().credit_limit
        ):
            exception_msg = self.env._("This sale order exceeds the financial risk.\n")
        return exception_msg

    def action_confirm(self):
        if not self.env.context.get("bypass_risk", False):
            for order in self.filtered(
                lambda so: not so.company_id.allow_overrisk_sale_confirmation
            ):
                partner = order.partner_invoice_id.commercial_partner_id
                exception_msg = order.evaluate_risk_message(partner)
                if exception_msg:
                    return (
                        self.env["partner.risk.exceeded.wiz"]
                        .create(
                            {
                                "exception_msg": exception_msg,
                                "partner_id": partner.id,
                                "origin_reference": f"{order._name},{order.id}",
                                "continue_method": "action_confirm",
                            }
                        )
                        .action_show()
                    )
        return super().action_confirm()

    @api.model
    def _get_risk_states(self):
        risk_states = ["sale"]
        ICP = self.env["ir.config_parameter"].sudo()
        if ICP.get_param("sale_financial_risk.include_risk_sale_order_done"):
            risk_states.append("done")
        return risk_states
