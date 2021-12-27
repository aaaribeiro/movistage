#built-in modules
import re

# third-party modules
import click

# app modules
from utils.handlers import DbHandler
from models import models
from models import crud


def check_email(email):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
    if not (re.search(regex, email)):   
        click.echo("Invalid Email")
        exit() 


@click.group()
def main():
    pass


@main.command()
@click.option("-A", "--admin", type=bool, default=False)
@click.option("-e", "--email", type=str, default=None)
@click.option("-u", "--user", type=str, default=None)
@click.option("-p", "--password", type=str, default=None) 
def user(admin, email, user, password):
    
    """
    Program used to create users directly from database
    """
    
    if not email: # check if email was inputed 
        email = click.prompt("E-mail")

    check_email(email) # check email pattern
    with DbHandler() as db: 
        db_user = crud.get_user_by_email(db, email)
        if db_user: # check if users exists
            click.echo("User already created")
            exit() 

    if not user: # check if username was inputed 
        user = click.prompt("Username").upper()
    
    if not password: # check if password was inputed 
        password = click.prompt("Password")

    # confirm password
    _password = click.prompt("Retype password")

    if password != _password: # quit program if passwords don't match
        click.echo("Passwords don't match")
        exit()
    else: # create new user
        with DbHandler() as db:
            db_user = models.Users(name=user, email=email, isadmin=admin,
                                password=password)
            db.add(db_user)
            db.commit()
            db.close()
            click.echo(f"User {user}/{email} created")


@main.command()
@click.option("--email", "-e", type=str, default=None)
@click.option("--password", "-p", type=str, default=None)
def token(email, password):
    
    """
    Program used to get user token
    """

    if not email: # check if email was inputed 
        email = click.prompt("E-mail") 

    check_email(email) # check email pattern 
    with DbHandler() as db:    
        db_user = crud.get_user_by_email(db, email)
        if not db_user: # quit if user already exists
            click.echo(f"User {email} not registered")
            exit()  
    
    if not password: # check if password was inputed 
        password = click.prompt("Password")
    
    with DbHandler() as db:
        db_user = crud.get_user_by_email(db, email) # get user's info
        if db_user.password != password: # quit if passwords don't match
            click.echo("Password doesn't match")
        else: 
            token = crud.get_access_token(db, db_user) # get token if exists
            if not token: # create a new one if doesn't
                token = crud.create_access_token(db, db_user)
            click.echo(f"Token: {token.access_token}")
    

@main.command()
@click.option("--email", "-e", type=str, default=None)
def update_password(email):
    
    """
    Program used to update password
    """

    if not email: # check if password was inputed 
        email = click.prompt("E-mail")

    check_email(email) # check email pattern
    with DbHandler() as db:
        db_user = crud.get_user_by_email(db, email)
        if db_user: # check if user exists (change password only makes sense if user is created)
            password = click.prompt("New password")
            _password = click.prompt("Retype password")

            if password != _password: # check if new passwords match
                click.echo("Passwords don't match")
                exit()
            else: # if match update password
                db_token = crud.get_token_by_user_id(db, db_user.user_id)
                if db_token: # if token for this user exists, delete it
                    crud.delete_token(db, db_token)
                    click.echo("-> Token deleted, a new one has to be created")
                db_user.password = password 
                db.commit()            
                click.echo("Password changed")

if __name__ == "__main__":
    main()