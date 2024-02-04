# from odoo import models, fields, api, _,http
# from odoo.exceptions import UserError, ValidationError



# employee_feedback/models/models.py

from odoo import models, fields,api

class EmployeeFeedback(models.Model):
    _name = 'employee.feedback'
    _description = 'Employee Feedback'
    _inherit = ['mail.thread']
    _inherits = {'hr.employee': 'employee_id'}

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, ondelete='cascade')
    employee_name = fields.Char(string='Employee Name', related='employee_id.name', store=True)
    date = fields.Date(string='Date')
    work_phone = fields.Char(string='Work Phone', related='employee_id.work_phone', readonly=True)
    work_email = fields.Char(string='Work Email', related='employee_id.work_email', readonly=True)
    department = fields.Char(string='Department', related='employee_id.department_id.name', readonly=True)
    feedback_type = fields.Selection([('1', 'Feedback'), ('2', 'Problem')], string='Feedback Type')
    image=fields.Binary( related='employee_id.image_1920', readonly=True)
    
    # Feedback Fields
    question_1 = fields.Boolean(string='Do you have everything you need to do your job?')
    question_2 = fields.Boolean(string='Do you feel your team works well together?')
    question_3 = fields.Boolean(string='Is the financial return rewarding for you?')
    question_4 = fields.Text(string='Where would you like to see yourself in the company in the short term and long term?')
    question_5 = fields.Text(string='Do you have any additional comments or questions?')

    # Problem Fields
    problem_description = fields.Text(string='Describe the problem clearly')
    category_ids = fields.Many2many(
        'hr.employee.category', 'feedback_category_rel',
        'feedback_id', 'category_id',string='Tags5')
    # New HTML fields for feedback and problem history
    feedback_history = fields.Html(string='Feedback History', readonly=True, sanitize=True)
    problem_history = fields.Html(string='Problem History', readonly=True, sanitize=True)

    # Method to refresh history
    def refresh_history(self):
        # Implement logic to update feedback_history and problem_history fields
        # Fetch and format previous feedback and problem data for the employee
        # Update self.feedback_history and self.problem_history fields accordingly
        pass
    @api.model
    def send_whatsapp_message(self, records):
        for record in records:
            if isinstance(record, int):
                # If 'record' is an integer, it's an ID. Fetch the record.
                record = self.browse(record)

            if record.work_phone:
                phone_number =record.work_phone
                message = f'Thanks for you, {record.employee_name}! Your feedback has been submitted successfully!'
                whatsapp_link_api = "https://api.whatsapp.com/send?phone=%s&text=%s" % (
                    phone_number, message)

                return {
                
                    'type': 'ir.actions.act_url',
                    'target': 'new',
                    'url': whatsapp_link_api
                }

