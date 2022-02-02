# built-in libraries
# import logging # libvrary for logging
# import logging.config
# from os import urandom # logging config file

# personal modules
# import utils
from serializers.schemas import TicketNestedCompany, Agent, Organization, TimeAppointment
# # @utils.debug
# def company(data):
#     return {
#         "client_id": data["clients"][0]["organization"]["id"],
#         "organization_name": data["clients"][0]\
#                             ["organization"]["businessName"].upper(),
#         }


def _upper(value):
    if value is not None: 
        return value.upper().lstrip()



def _time(value):
    if value is None: return "00:00:00"
    else: return value



def ticket(data):

    organization_id = data["clients"][0]["organization"]["id"]
    organization_name = data["clients"][0]["organization"]["businessName"]
    organization = Organization(
        organization_id = _upper(organization_id),
        organization_name =  _upper(organization_name),
    )

    agent_id = data["owner"]["id"]
    agent_name = data["owner"]["businessName"]
    agent_team = data["ownerTeam"]
    agent = Agent(
        agent_id = _upper(agent_id),
        agent_name = _upper(agent_name),
        agent_team = _upper(agent_team),
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
        subject = _upper(subject),
        category = _upper(category),
        urgency = _upper(urgency),
        status = _upper(status),
        created_date = created_date,
        sla_first_response = sla_first_response, 
        sla_solution_date = sla_solution_date,
    )




# @utils.debug
def appointments(data):

    appointments = []
 
    for action in data["actions"][::-1]:
        if action["createdBy"]["profileType"] in (1, 3):
            
            time_appointment_id = action["timeAppointments"][0]["id"]
            ticket_id = data["id"]
            agent_id = action["timeAppointments"][0]["createdBy"]["id"]
            time_appointment = action["timeAppointments"][0]["workTime"]
            
            appointment = TimeAppointment(
                time_appointment_id = time_appointment_id,
                ticket_id = ticket_id,
                agent_id = _upper(agent_id),
                time_appointment = _time(time_appointment)
            )

            appointments.append(appointment)

    return appointments
