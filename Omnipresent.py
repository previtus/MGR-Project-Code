import numpy as np

def len_(L):
    return np.array(L).shape


def send_main(subject, message, attachment_path = None):

    import smtplib, os
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    from mail_secrets import fromaddr, toaddr, passwrd

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject #"SUBJECT OF THE EMAIL"

    body = message #"TEXT YOU WANT TO SEND"

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path is not None:

        attachment_filename = os.path.basename(attachment_path)
        attachment = open(attachment_path, "rb") #"PATH OF THE FILE"

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % attachment_filename)

        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, passwrd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


#send_main('automatic mail', 'test', '/home/ekmek/Vitek/Logs/Number_of_FC_blocks_test/graph_together_Number_of_FC_blocks_test.png')

