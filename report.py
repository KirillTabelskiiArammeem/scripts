import atexit
import csv
import datetime
import getpass
from functools import cache

import psycopg2

QUERY = """
SELECT
	agent_name AS "Agent Name",
	email AS "User email",
	auto_assigned AS "Assigned by auto-assign (odoobot)",
	autoassigned_manually AS "Assigned manually",
	ticket_id AS "Ticket ID",
	reason AS "Reason"

FROM (
		SELECT
		res_partner.name AS agent_name, 
		res_partner.email AS email, 
		mail_message.author_id = 2 AS auto_assigned,
		mail_message.author_id != 2 AS autoassigned_manually, 
		helpdesk_ticket.id AS ticket_id,
		helpdesk_ticket_type.name AS reason,
		mail_tracking_value.create_date AS assin_date,
		mail_tracking_value.new_value_integer AS user_id,
		FIRST_VALUE(mail_tracking_value.new_value_integer) 
	    OVER(
	    	  PARTITION BY helpdesk_ticket.id
	        ORDER BY mail_tracking_value.create_date
	    ) first_user_id
	
	FROM helpdesk_ticket
	LEFT JOIN 
		mail_message ON helpdesk_ticket.id = mail_message.res_id AND 
		mail_message.model = 'helpdesk.ticket' 
	LEFT JOIN 
		mail_tracking_value ON mail_tracking_value.mail_message_id = mail_message.id AND 
		mail_tracking_value.field = 'user_id' AND 
		mail_tracking_value.field_desc = 'Assigned to'
	LEFT JOIN 
		res_users ON mail_tracking_value.new_value_integer = res_users.id
	LEFT JOIN 
		res_partner ON  res_users.partner_id = res_partner.id 
	LEFT JOIN
		helpdesk_ticket_type ON helpdesk_ticket.ticket_type_id = helpdesk_ticket_type.id
	WHERE	
		mail_tracking_value.field = 'user_id'  AND 
		mail_tracking_value.field_desc = 'Assigned to' AND  
		mail_tracking_value.new_value_integer != 0 AND 
		helpdesk_ticket.create_date BETWEEN '{}' AND '{}' AND
		res_partner.email IN (
			'a.alhathal@toyou.io', 'r.alarifi@toyou.io', 'a.khiyar@toyou.io', 'n.alshawbash@toyou.io',
			'ah.alzahrani@toyou.io', 'no.aldowsari@toyou.io', 'y.alanbar@toyou.io', 'su.aldawsari@toyou.io',
			'k.balaa@toyou.io', 'na.abdullah@toyou.io', 'f.sulaiman@toyou.io', 'a.gumaah@toyou.io',
			'ra.aldawsari@toyou.io', 'y.alanazi@toyou.io', 's.ramis@toyou.io', 'o.alqahtani@toyou.io',
			'mo.albaqami@toyou.io', 'm.alajlani@toyou.io', 'a.alasmari@toyou.io', 's.alsaiari@toyou.io',
			'na.obaid@toyou.io', 'r.alosaimi@toyou.io'
			)
	ORDER BY
		helpdesk_ticket.id, mail_tracking_value.create_date
) AS assigns


WHERE user_id = first_user_id
"""


@cache
def get_connection():
    con = psycopg2.connect(
        host="gw-erp.net.amhub.org",
        port=5432,
        user=input("user: "),
        password=getpass.getpass("password:"),
        database="odoo_am_helpdesk_12_prod_ro",
    )
    atexit.register(con.close)
    return con


def get_daily_report(date):
    q = QUERY.format(date.isoformat(), (date + datetime.timedelta(days=1)).isoformat())
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(q)
            for row in cursor:
                yield row


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def main():
    with open("report.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Agent Name",
                "User email",
                "Assigned by auto-assign (odoobot)",
                "Assigned manually",
                "Ticket ID",
                "Reason",
            ]
        )
        for date in date_range(
                datetime.date(2023, 10, 1),
                datetime.date(2023, 10, 20)
        ):
            print(date)
            for row in get_daily_report(date):
                writer.writerow(row)


main()
