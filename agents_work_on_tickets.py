
in_progress_stage = env.ref("helpdesk.stage_in_progress")
team = env['helpdesk.team'].search([('name', '=', 'Test Team Assign')], limit=1)

configs = env['aram.autoassign.config'].search([('helpdesk_team', '=', team.id)])
users = configs.mapped('agent')


while True:
    tickets = env['helpdesk.ticket'].search([('team_id', '=', team.id), ('stage_id', '=', in_progress_stage.id)])
    solved_stage = self.env.ref("helpdesk.stage_solved")
    for ticket in tickets:
        ticket.sudo().write({'stage_id': solved_stage.id})
        print(ticket)
        env.cr.commit()
    env.cr.commit()