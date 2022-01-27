# built-in libraries
from datetime import datetime, time

# third-party libraries
from typing import Optional
from pydantic import BaseModel, Field


class Ticket(BaseModel):
    ticket_id: Optional[int]
    client_id: Optional[str]
    created_date: Optional[datetime]
    status: Optional[str]
    owner_team: Optional[str]
    category: Optional[str]
    urgency: Optional[str]
    subject: Optional[str]
    agent: Optional[str]
    sla_solution_date: Optional[datetime]
    sla_first_response: Optional[datetime]

    class Config:
        orm_mode = True


class Organization(BaseModel):
    client_id: Optional[str]
    organization_name: Optional[str]

    class Config:
        orm_mode = True


class TicketNestedCompany(BaseModel):
    ticket_id: Optional[int]
    client: Optional[Organization] = None
    created_date: Optional[datetime]
    status: Optional[str]
    owner_team: Optional[str]
    category: Optional[str]
    urgency: Optional[str]
    subject: Optional[str]
    agent: Optional[str]
    sla_solution_date: Optional[datetime]
    sla_first_response: Optional[datetime]

    class Config:
        orm_mode = True


class TimeAppointment(BaseModel):
    ticket_time_appointment_pk: Optional[int]
    ticket_id: Optional[int]
    agent_id: Optional[str]
    time_appointment: Optional[time]
    
    class Config:
        orm_mode = True


class Agent(BaseModel):

    agent_id: Optional[str]
    agent_name: Optional[str]
    agent_team: Optional[str]

    class Config:
        orm_mode = True


class WebhookLog(BaseModel):
    hook_id: Optional[int]
    ticket_id: Optional[int]
    change: Optional[str]
    trigger_date: Optional[datetime]
    was_read: Optional[bool]

    class Config:
        orm_mode = True


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