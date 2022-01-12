# import logging # library for logging
# import logging.config # logging config file

# logging.config.fileConfig("logging.config")
# logger = logging.getLogger("sqlalchemy")

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Time
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Boolean
from routers import webhooks
from sqlalchemy_utils import EmailType, PasswordType
# from sqlalchemy.sql.sqltypes import Boolean

from .database import Base

class Tickets(Base):
    
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, nullable=False)
    client_id = Column(String,  ForeignKey("organization.client_id"), nullable=False)
    created_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    owner_team = Column(String)
    category = Column(String, nullable=False)
    urgency = Column(String, nullable=False)
    subject =  Column(String, nullable=False)
    agent = Column(String)
    sla_solution_date = Column(DateTime)
    sla_first_response = Column(DateTime)

    # relationships
    time_appointments = relationship("TimeAppointments")
    client =  relationship("Organizations", back_populates="tickets")


class Organizations(Base):

    __tablename__ = "organization"

    client_id = Column(String, primary_key=True, nullable=False)
    organization_name = Column(String, nullable=False)

    # relationships
    tickets = relationship("Tickets", back_populates="client")


class TimeAppointments(Base):

    __tablename__ = "ticket_time_appointment"

    ticket_time_appointment_pk = Column(Integer, primary_key=True, nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.ticket_id"), nullable=False)
    time_appointment = Column(Time, nullable=False)
    agent = Column(String, nullable=False)


class WebhookLogs(Base):

    __tablename__ = "webhook_log"

    hook_id = Column(Integer, primary_key=True, nullable=False,
        autoincrement=True)
    ticket_id = Column(Integer, nullable=False)
    change = Column(String, nullable=False)
    trigger_date = Column(DateTime, nullable=False)
    was_read = Column(Boolean, nullable=False, default=False)


class Users(Base):

    __tablename__ = "auth_users"

    # TYPES = [u'admin', u'edit', u'read']

    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(EmailType, nullable=False, unique=True)
    isadmin = Column(Boolean, nullable=False, default=False)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']))
    
    # relationships
    token = relationship("AccessToken", backref=backref("auth_access_token", uselist=False))


class AccessToken(Base):

    __tablename__ = "auth_access_token"

    token_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey("auth_users.user_id"), nullable=False)
    access_token = Column(String, nullable=False)
