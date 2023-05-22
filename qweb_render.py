from collections import OrderedDict

air = env['amc.invoice.report']
air = air.browse(536295)
# air = air.browse(27214)

# air.generate_invoice_attachments_pdf()
acri = self.env.ref("aram_crm.report_invoice")


# pdf = self.env.ref("aram_crm.report_invoice").render_qweb_pdf(
#             self.ids,
#             data=self.get_context_invoice_pdf(),
#         )

data = air.get_context_invoice_pdf()
data.setdefault('report_type', 'pdf')
data.update(enable_editor=False)
save_in_attachment = OrderedDict()
res_ids = air.ids

Model = env[acri.model]
record_ids = Model.browse(res_ids)
wk_record_ids = Model

html = acri.render_qweb_html(res_ids, data=data)[0]