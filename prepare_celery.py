# docker exec -it odoo-modules-hd-12-odoo-1 bash
# odoo shell -c /etc/odoo/odoo.conf --no-http


import odoo

name = 'Test Team Assign'
limitation_number = 5

ready_status = env.ref("aram_agent_status.agent_status_ready")
ticket_type = env.ref("__export__.helpdesk_ticket_type_3589_9a430297")
order_status = env.ref(
            "__export__.helpdesk_ticket_order_status_1_472dfaf5"
        )
channel = self.env.ref("__export__.amh_channel_1_1294302a")
customer_tier = self.env.ref("webhook_chat_incoming.blue_customer_tier")
initiator = self.env.ref("__export__.helpdesk_ticket_initiator_1_130964ad")
in_progress_stage = self.env.ref("helpdesk.stage_in_progress")
solved_stage = self.env.ref("helpdesk.stage_solved")
closed_stage = self.env.ref("aram_helpdesk.stage_closed")
updated_stage = self.env.ref("aram_helpdesk.stage_updated")
stages = self.env["helpdesk.stage"].search([]).mapped("id")
team = self.env["helpdesk.team"].create(
            {
                "name": name,
                "assign_method": "limitbalanced",
                "limitation_number": limitation_number,
                "team_type": "open",
            }
        )
team.stage_ids = stages
number_of_users = 20
users = []
configs = []
for i in range(number_of_users):
    user = odoo.tests.new_test_user(
        self.env,
        login="test_user_{}_team_{}".format(i, team.id),
        team_ids=[team.id],
    )
    user.team_ids = [team.id]
    config = self.env["aram.autoassign.config"].create(
        {"agent": user.id, "helpdesk_team": team.id}
    )
    user.status_work = ready_status
    users.append(user)
    configs.append(config)

team.autoassign_configs = [config.id for config in configs]
env.cr.commit()

# team = env['helpdesk.team'].browse(889)

def quick_create_ticket(name, order_number):
        return env["helpdesk.ticket"].create(
            {
                "name": name,
                "team_id": team.id,
                "ticket_type_id": ticket_type.id,
                "channel_id": channel.id,
                "customer_tier": customer_tier.id,
                "initiator": initiator.id,
                "order_status": order_status.id,
                "order_number": order_number,
                "is_autocreated": True,
            }
        )


for i in range(10300, 11300):
    try:
        quick_create_ticket("test ticket", i)
        env.cr.commit()
    except Exception as er:
        print(er)