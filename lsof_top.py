import logging
old_team = env["helpdesk.team"].browse(589)
new_team = env["helpdesk.team"].browse(655)
stages = env["helpdesk.stage"].search([('is_close', '=', True)])

tickets = env["helpdesk.ticket"].search([('team_id', '=', old_team.id), ('stage_id', 'in', stages.ids)])

env.cr.commit()

query_template = """
UPDATE helpdesk_ticket
SET team_id = {new_team_id}
WHERE id = {ticket_id}
"""

logger = logging.getLogger('rm_13680')
i = 0

for ticket in tickets:
    i += 1
    print(f'{i}/{len(tickets)}')
    logger.info(f"RM-13680 Ticket {ticket.id} moved from team {old_team.id} to team {new_team.id}")
    query = query_template.format(new_team_id=new_team.id, ticket_id=ticket.id)
    logger.info(f"RM-13680 Query: {query}")
    env.cr.execute(query)
    env.cr.commit()


logger.info(f'tickets {tickets} moved from team {old_team.id} to team {new_team.id}')