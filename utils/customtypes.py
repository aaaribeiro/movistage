import re
import click

class Email(click.ParamType):
    name = "e-mail"

    def convert(self, value, param, ctx):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
        if (re.search(regex, value)):   
            return value
        else:
            self.fail(f"{value!r} is not a valid e-mail", param, ctx)

