import smtplib
import ssl

class Email:
    # Setup port number and servr name

    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    email_from = "phildschool@gmail.com"
    email_to = "phildschool@gmail.com"

    pswd = 'vjty nkvt olic dvsd'

    message = """From: From IOT-Dashboard <iotdashboard@iotDash.com>
    To: Phil <phildschool@gmail.com>
    Subject: Notice! the room is getting hot

    The Temperature is above 24 Degrees Celsius.
    Would you like to turn on the fan?
    if yes, reply to this email with a `yes`.
    """    

    simple_email_context = ssl.create_default_context()

    # -----------------------------------------------------------------

    

    def __init__(self):
        return
    def send(self):
        try:
            # Connect to the server
            print("Connecting to server...")
            TIE_server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            TIE_server.starttls(context=self.simple_email_context)
            TIE_server.login(self.email_from, self.pswd)
            print("Connected to server")
            
            # Send the actual email
            print(f"Sending email to - {self.email_to}")
            TIE_server.sendmail(self.email_from, self.email_to, self.message)
            print(f"Email successfully sent to - {self.email_to}")

        # If there's an error, print it out
        except Exception as e:
            print(e)

        # Close the port
        finally:
            TIE_server.quit()
            
    # method for receiving here
    def receive(self):
        return