# built-in libraries
from datetime import datetime, time

# third-party libraries
from typing import Optional, List
from pydantic import BaseModel



class Ticket(BaseModel):
    ticket_id: Optional[int]
    organization_id: Optional[str]
    agent_id: Optional[str]
    created_date: Optional[datetime]
    status: Optional[str]
    category: Optional[str]
    urgency: Optional[str]
    subject: Optional[str]
    sla_solution_date: Optional[datetime]
    sla_first_response: Optional[datetime]

    class Config:
        orm_mode = True


class Agent(BaseModel):

    agent_id: Optional[str]
    agent_name: Optional[str]
    agent_team: Optional[str]

    class Config:
        orm_mode = True


class Organization(BaseModel):
    organization_id: Optional[str]
    organization_name: Optional[str]

    class Config:
        orm_mode = True


################################ ?
class TicketAppointment(BaseModel):
    time_appointment_id: Optional[int]
    time_appointment: Optional[time]
    created_date: Optional[datetime]
    agent : Optional[Agent] = None

    class Config:
        orm_mode = True


class TimeAppointment(BaseModel):
    time_appointment_id: Optional[int]
    ticket_id: Optional[int]
    agent_id: Optional[str]
    time_appointment: Optional[time]
    created_date: Optional[datetime]

    class Config:
        orm_mode = True


class TicketNestedCompany(BaseModel):
    ticket_id: Optional[int]
    organization: Optional[Organization] = None
    agent: Optional[Agent] = None
    created_date: Optional[datetime]
    status: Optional[str]
    category: Optional[str]
    urgency: Optional[str]
    subject: Optional[str]
    sla_solution_date: Optional[datetime]
    sla_first_response: Optional[datetime]
    time_appointments: List[TicketAppointment] = None

    class Config:
        orm_mode = True



# class AgentAppointment(BaseModel):
#     time_appointment_id: Optional[int]
#     agent: Optional[Agent] = None
#     time_appointment: Optional[time]
#     created_date: Optional[datetime]

#     class Config:
#         orm_mode = True


# class TimeAppointmentGroupedByTicket(BaseModel):
#     ticket_id: Optional[int]
#     time_appointments: List[AgentAppointment] = None

#     class Config:
#         orm_mode = True


# class TimeAppointmentGroupedByAgent(BaseModel):
#     agent_id: Optional[str]
#     agent_name: Optional[str]
#     agent_team: Optional[str]
#     time_appointments: List[TicketAppointment] = None

#     class Config:
#         orm_mode = True


# class WebhookLog(BaseModel):
#     hook_id: Optional[int]
#     ticket_id: Optional[int]
#     change: Optional[str]
#     trigger_date: Optional[datetime]
#     was_read: Optional[bool]

#     class Config:
#         orm_mode = True


class User(BaseModel):
    user_id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    isadmin: Optional[bool]
    password: Optional[str]

    class Config:
        orm_mode = True


class CreatedUser(BaseModel):
    user_id: Optional[int]
    name: Optional[str]
    email: Optional[str]

    class Config:
        orm_mode = True


# class AccessToken(BaseModel):
#     access_token: Optional[str]

#     class Config:
#         orm_mode = True

# if __name__ == "__main__":
#     test = CreatedUser(
#         user_id = 1,
#         name = "Andre",
#         email = "andre@netcon"
#     )
#     print(test)
#     name = test.pop("name")
#     print(name)