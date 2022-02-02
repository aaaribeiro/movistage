# built-in libraries
# import logging # libvrary for logging
# import logging.config
from os import urandom # logging config file

# personal modules
import utils
from serializers.schemas import TicketNestedCompany, Agent, Organization
# configuring logging hanlder for script
# logging.config.fileConfig("logging.config")
# logger = logging.getLogger(__name__)
# logger.debug(f"{__name__} log done, starting the application")

# @utils.debug
# def check(payload, fields):
#     for key in payload.keys():
#         if key not in fields:
#             print("ticket payload without mandatory fields")
#             # logger.error("ticket payload without mandatory fields")
#             exit(1)


# # @utils.debug
# def company(data):
#     return {
#         "client_id": data["clients"][0]["organization"]["id"],
#         "organization_name": data["clients"][0]\
#                             ["organization"]["businessName"].upper(),
#         }

# @utils.debug
def ticket(data):

    def to_upper(value):
        if value is not None: 
            return value.upper().lstrip()


    organization_id = data["clients"][0]["organization"]["id"]
    organization_name = data["clients"][0]["organization"]["businessName"]
    organization = Organization(
        organization_id = to_upper(organization_id),
        organization_name =  to_upper(organization_name),
    )

    agent_id = data["owner"]["id"]
    agent_name = data["owner"]["businessName"]
    agent_team = data["ownerTeam"]
    agent = Agent(
        agent_id = to_upper(agent_id),
        agent_name = to_upper(agent_name),
        agent_team = to_upper(agent_team),
    )

    ticket_id = data["id"]
    subject = data["subject"]
    category = data["category"]
    urgency = data["urgency"]
    created_date = data["createdDate"]
    status = data["status"]
    sla_first_response = data["slaResponseDate"]
    sla_solution_date = data["slaSolutionDate"]

    return TicketNestedCompany(
        ticket_id = ticket_id,
        agent = agent,
        organization = organization,
        subject = to_upper(subject),
        category = to_upper(category),
        urgency = to_upper(urgency),
        status = to_upper(status),
        created_date = created_date,
        sla_first_response = sla_first_response, 
        sla_solution_date = sla_solution_date,
    )




# @utils.debug
def appointment(data):
    actions = data["actions"]
    for action in actions[::-1]:
        if action["createdBy"]["profileType"] in (1, 3):
            t_appointment = action["timeAppointments"][0]["workTime"]
            agent = action["timeAppointments"][0]["createdBy"]["businessName"]
            # team =  action["timeAppointments"][0]["createdByTeam"]["name"]
            break


    return {
        "ticket_id": data["id"],
        "time_appointment": t_appointment if t_appointment is not None else "00:00:00",
        "agent": agent.upper() if agent is not None else None
        # "team": team
    }
