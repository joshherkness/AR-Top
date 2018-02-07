import base64

from flask import current_app
from flask_mail import Mail, Message

import bcrypt
import jwt
from constants import *
from models import *


class Helper():

    def validate_register(email, password):
        """Validate user registration.

        Keyword arguments:
        email -- The email being used to create a account.
        password -- The password that will be validated.

        Returns a tuple of invalid truthness, and error message if applicable.
        """
        message = None
        invalid = False
        try:
            if len(email) > max_email_length:
                message = "Email can't be over " + \
                    str(max_email_length) + " characters."
                invalid = True
            if not email_pattern.match(email):
                message = "Email not valid."
                invalid = False
            if len(password) < 8 or len(password) > max_password_length:
                message = "Password must be between 8-" + \
                    str(max_password_length) + " characters."
                invalid = False
            if not str.isalnum(password):
                message = "Only alphanumeric characters are allowed in a password."
                invalid = False

            # Try to retrieve a user object if it exists;
            user = User.objects(email=email).first()
            if user:
                message = "Email already in use, please use another one"
                invalid = False
        except Exception as e:
            current_app.logger.error(e)
        return invalid, message

    def validate_auth(email, password):
        """Validate an authentication attempt.

        email -- Email that will be used to query the database.
        password -- Password that will be used to verify against salted and hashed password in database.

        Returns valid truthness, error message if applicable, and authorization token if valid auth attempt.
        """
        message = None
        invalid = False
        auth_token = None
        try:
            user = User.objects(email=email).first()
            if user is None or len(user) == 0:
                message = "Incorrect email or password"
                invalid = True
            else:
                if bcrypt.checkpw(password.encode(), user.password.encode()):
                    auth_token = user.generate_auth_token().decode('utf-8')
        except Exception as e:
            current_app.logger.error(e)
        return invalid, message, auth_token

    def verify_jwt(request):
        """Verify that a JWT is valid.

        request -- The incoming request that is attempting to hit a protected endpoint

        Return the claims inside the JWT.
        """
        claims = None
        auth_header = request.headers['Authorization'].split()
        if auth_header[0] == 'Bearer':
            claims = jwt.decode(auth_header[1], base64.b64decode(
                secrets.JWT_KEY.encode()), algorithm=['HS512'])['data']
        return claims

    def hashpw(password):
        """ Hash and salt the incoming string. """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def send_email(text, recipients, subject="AR-top"):
        """Send email to user.

        text -- Message that will be sent to recipients.
        recipients -- Who will receive the email.
        subject -- Subject of email. Default = AR-Top

        """
        if type(recipients) is str:
            recipients = [recipients]

        try:
            msg = Message(subject, sender=secrets.MAIL_USERNAME,
                          recipients=recipients)
            msg.body = text
            mail.send(msg)
        except Exception as e:
            current_app.logger.error("Failed to send message to " +
                                     str(recipients) + "\n" + str(e))
