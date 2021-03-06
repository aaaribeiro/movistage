
from serializers.schemas import (
    Ticket,
    Agent,
    Organization,
    TimeAppointment,
)



def _upper(value):
    if value is not None: 
        return value.upper().lstrip()



def _time(value):
    if value is None: return "00:00:00"
    else: return value
    


def ticket(data):

    organization_id = _upper(data["clients"][0]["organization"]["id"])
    organization_name = _upper(data["clients"][0]["organization"]["businessName"])
    organization = Organization(
        organization_id = _upper(organization_id),
        organization_name =  _upper(organization_name),
    )

    try:
        agent_id = _upper(data["owner"]["id"])
        agent_name = _upper(data["owner"]["businessName"])
        agent_team = _upper(data["ownerTeam"])
    except:
        agent_id = None
        agent_name = None
        agent_team = None  
    
    agent = Agent(
        agent_id = agent_id,
        agent_name = agent_name,
        agent_team = agent_team,
    )

    # appointments = [] 
    # for action in data["actions"][::-1]:
    #     if action["createdBy"]["profileType"] in (1, 3):
    #         try:
    #             time_appointment_id = int(f"{data['id']}"
    #                                     + f"{action['id']:03}")
    #             ticket_id = data["id"]
    #             agent_id = action["timeAppointments"][0]["createdBy"]["id"]
    #             time_appointment = action["timeAppointments"][0]["workTime"]
    #             created_date = action["createdDate"]
                
    #             appointment = TimeAppointment(
    #                 time_appointment_id = time_appointment_id,
    #                 ticket_id = ticket_id,
    #                 agent_id = _upper(agent_id),
    #                 time_appointment = _time(time_appointment),
    #                 created_date = created_date,
    #             )
    #             appointments.append(appointment)
    #         except IndexError:
    #             continue

    ticket_id = data["id"]
    subject = _upper(data["subject"])
    category = _upper(data["category"])
    urgency = _upper(data["urgency"])
    created_date = _upper(data["createdDate"])
    status = _upper(data["status"])
    sla_first_response = data["slaResponseDate"]
    sla_solution_date = data["slaSolutionDate"]
    ticket = Ticket(
        ticket_id = ticket_id,
        agent_id = agent_id,
        organization_id = organization_id,
        subject = subject,
        category = category,
        urgency = urgency,
        status = status,
        created_date = created_date,
        sla_first_response = sla_first_response, 
        sla_solution_date = sla_solution_date,
    )
    
    return ticket, organization, agent 


# def organization(data):
#     organization_id  = data["id"]
#     organization_name = data["businessName"]

<<<<<<< HEAD
# def organization(data):
#     organization_id  = data["id"]
#     organization_name = data["businessName"]

=======
>>>>>>> dde6cd4f59602db4f8c421fc2a41567aa2450c87
#     return Organization(
#         organization_id = organization_id,
#         organization_name = _upper(organization_name)
#     )



def appointment(data, actionID):
    for action in data["actions"][::-1]:
        if action["id"] == actionID and \
        action["createdBy"]["profileType"] in (1, 3):
            try:
                time_appointment_id = int(f"{data['id']}"+f"{action['id']:03}")
                ticket_id = data["id"]
                agent_id = action["timeAppointments"][0]["createdBy"]["id"]
                time_appointment = action["timeAppointments"][0]["workTime"]
                created_date = action["createdDate"]
                
                appointment = TimeAppointment(
                    time_appointment_id = time_appointment_id,
                    ticket_id = ticket_id,
                    agent_id = _upper(agent_id),
                    time_appointment = _time(time_appointment),
                    created_date = created_date,
                )
            except IndexError:
                continue
            else:
                return appointment

    
