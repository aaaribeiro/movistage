#built-in modules
import re

# third-party modules
import click

# app modules
from utils.handlers import DbHandler
from utils.customtypes import Email
from models import models
from models import _crud


def check_user(ctx, param, value):
    with DbHandler() as db:
        db_user = _crud.get_user_by_email(db, value)
        if ctx.command.name == "user":
            if db_user: # quit if user exists
                click.echo(f"User {value} already registered")
                ctx.exit()
            else:
                return value
        else:
            if not db_user: # quit if user not exists
                click.echo(f"User {value} not exists")
                ctx.exit()
            else:
                return value


@click.group()
def main():
    pass


@main.command()
@click.option("--email", "-e", prompt=True, type=Email(), is_eager=True,
                callback=check_user)
@click.option("-A", "--admin", type=bool, default=False)
@click.password_option()
def user(admin, email, password):
    
    """
    Program used to create users directly from database
    """
    username = email.split("@")[0]
    with DbHandler() as db: 
        db_user = models.Users(name=username, email=email, isadmin=admin,
                            password=password)
        db.add(db_user)
        db.commit()
        db.close()
        click.echo(f"User {username}/{email} created")


@main.command()
@click.option("--email", "-e", prompt=True, type=Email(), is_eager=True,
                callback=check_user)
@click.option("--password", prompt=True, hide_input=True)
def token(email, password):
    
    """
    Program used to get user token
    """

    with DbHandler() as db:    
        db_user = _crud.get_user_by_email(db, email)
        if db_user.password != password: # quit if passwords don't match
            click.echo("Password doesn't match")
            exit()
        else: 
            token = _crud.get_access_token(db, db_user) # get token if exists
            if not token: # create a new one if doesn't
                token = _crud.create_access_token(db, db_user)
            click.echo(f"Token: {token.access_token}")
    

@main.command()
@click.option("--email", "-e", prompt=True, type=Email(), is_eager=True,
                callback=check_user)
@click.password_option()
def update_password(email, password):
    
    """
    Program used to update password
    """

    with DbHandler() as db:
        db_user = _crud.get_user_by_email(db, email)
        # if password equal the previous one BINGO! you don't need to change your password
        if password == db_user.password: 
            click.echo("Password currently in use")
            exit()
        else:
            db_token = _crud.get_token_by_user_id(db, db_user.user_id)
            # if token for this user exists, delete it
            if db_token:
                _crud.delete_token(db, db_user.user_id)
                click.echo("-> Token deleted, a new one has to be created")
            db_user.password = password 
            db.commit()            
            click.echo("Password up-to-date")


if __name__ == "__main__":
    main()