import smtplib
import ssl
import imaplib
import email
import datetime
from time import gmtime, strftime

class Email:

    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    # email_from = "noreply.iotboard.pyt.ard@gmail.com"
    email_from = "phildschool@gmail.com"
    email_to = "phildschool@gmail.com"

    # pswd = 'itmd vfwu sywq tiix'
    pswd = 'vjty nkvt olic dvsd'

    message = ""
    notification = ""

    simple_email_context = ssl.create_default_context()

    # -----------------------------------------------------------------
    
    reply_email = 0
    original_email = 0

    def __init__(self):
        pass
    
    def setMessages(self, temp):
        self.message = """From: From IOT-Dashboard <iotdashboard@iotDash.com>
        To: Client <""" + self.email_to + """>
        Subject: Notice! the room is getting hot

        The Temperature is """ + str(temp) + """ Degrees Celsius.
        Would you like to turn on the fan?
        Please confirm your response in a reply to this email.
        """
        self.notification = """From: From IOT-Dashboard <iotdashboard@iotDash.com>
        To: Client <""" + self.email_to + """>
        Subject: Notification!

        The Light is ON at """ + str(datetime.datetime.now()) + """ time.
        """
        # strftime("%Y-%m-%d %H:%M:%S", gmtime())
        # datetime.datetime.now()
        
    def send(self,option):
        try:
            # Connect to the server
            print("Connecting to server...")
            TIE_server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            TIE_server.starttls(context=self.simple_email_context)
            TIE_server.login(self.email_from, self.pswd)
            print("Connected to server")
            
            # Send the actual email
            print(f"Sending email to - {self.email_to}")
            if(option == "message"):
                TIE_server.sendmail(self.email_from, self.email_to, self.message)
            if(option == "notification"):
                TIE_server.sendmail(self.email_from, self.email_to, self.notification)
            print(f"Email successfully sent to - {self.email_to}")

        # If there's an error, print it out
        except Exception as e:
            print(e)

        # Close the port
        finally:
            TIE_server.quit()
            
    # method for receiving here
    def receive(self):
        try:
            # Connect to the server
            print("Connecting to server...")
            TIE_server = imaplib.IMAP4_SSL(self.smtp_server)
            TIE_server.login(self.email_to, self.pswd)
            print("Connected to server")

            # Select the inbox folder
            TIE_server.select("inbox")

            # Search for emails to the receiver's email address
            _, data = TIE_server.search(None, f'(TO "{self.email_to}")')

            # Get the list of email IDs
            email_ids = data[0].split()

            # Get the latest email
            latest_email_id = email_ids[-1]

            # Fetch the email data
            _, email_data = TIE_server.fetch(latest_email_id, "(RFC822)")

            # Parse the email content
            raw_email = email_data[0][1]
            email_message = email.message_from_bytes(raw_email)

            # Check if the email subject and body contain "yes"
            subject = email_message["Subject"]
            body = ""
            if email_message.is_multipart():
                for part in email_message.get_payload():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        self.reply_email = len(body)
                        break
            else:
                body = email_message.get_payload(decode=True).decode()
                self.original_email = len(body)

            print(f"Received email - Subject: {subject}, Body: {body}")
            return "yes" in subject.lower() or "yes" in body.lower()

        except Exception as e:
            print(e)
            return False

        finally:
            # Close the connection
            TIE_server.logout()