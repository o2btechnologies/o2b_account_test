# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models, _
from odoo.addons import decimal_precision as dp

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    paid_total_amount = fields.Float(string='Paid Total Amount', digits=dp.get_precision('Product Price'), copy=False)
    paid_total_tax_amount = fields.Float(string='Paid Total Tax Amount', digits=dp.get_precision('Product Price'), copy=False)


class account_payment(models.Model):
    _inherit = "account.payment"

    @api.multi
    def post(self):
        res = super(account_payment, self).post()
        for payment in self:
            context = self.env.context
            active_ids = context.get('active_ids')
            inv_obj = self.env['account.invoice'].browse(active_ids)
            for inv in inv_obj:
                if inv.state == 'paid':
                    inv.write({'paid_total_amount':inv.amount_total,'paid_total_tax_amount':inv.amount_tax})
                elif inv.state == 'open':
                    amount_total = inv.amount_total
                    payment_amount = payment.amount
                    total_tax = inv.amount_tax
                    if not inv.paid_total_amount:
                        total_paid_amount_percentage = (payment_amount/amount_total)*100 #get total amount percentage
                        total_paid_amount_tax = (total_tax*total_paid_amount_percentage)/100 # get total tax amount based on total amount
                        inv.write({'paid_total_amount':payment.amount,'paid_total_tax_amount':total_paid_amount_tax})
                    else:
                        total_payment = inv.paid_total_amount+payment_amount
                        total_paid_amount_percentage = (total_payment/amount_total)*100
                        total_paid_amount_tax = (total_tax*total_paid_amount_percentage)/100
                        inv.write({'paid_total_amount':total_payment,'paid_total_tax_amount':total_paid_amount_tax})

        return res

# Update for old record
class Account_paymentOld(models.TransientModel):
    _name='update.account.payment'

    @api.multi
    def update_total_amount(self):
        inv_obj = self.env['account.invoice']
        active_ids = self._context.get('active_ids',[])
        for inv in inv_obj.browse(active_ids).filtered(lambda x: x.state in ['paid','open']):
            if inv.state == 'paid':
                inv.write({'paid_total_amount':inv.amount_total,'paid_total_tax_amount':inv.amount_tax})
            elif inv.state == 'open':
                amount_total = inv.amount_total
                total_tax = inv.amount_tax
                payment_ids = inv.mapped('payment_ids')
                payment_amount = sum(payment_id.amount for payment_id in payment_ids)
                total_paid_amount_percentage = (payment_amount/amount_total)*100
                total_paid_amount_tax = (total_tax*total_paid_amount_percentage)/100
                inv.write({'paid_total_amount':payment_amount,'paid_total_tax_amount':total_paid_amount_tax})

