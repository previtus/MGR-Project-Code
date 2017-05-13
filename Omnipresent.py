import numpy as np
import urllib2

def len_(L):
    return np.array(L).shape

def send_mail(subject, message, attachment_path = None):
    try:
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
        return True
    except Exception as inst:
        print "Exception when trying to send mail."
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst           # __str__ allows args to be printed directly
        return False


#send_mail('automatic mail', 'test', '/home/ekmek/Vitek/Logs/Number_of_FC_blocks_test/graph_together_Number_of_FC_blocks_test.png')

def save_job_report_page(folder_path, job_id, cut = True):
    try:

        url = 'https://metavo.metacentrum.cz/pbsmon2/job/' + job_id

        response = urllib2.urlopen(url)
        webContent = response.read()

        if cut:
            substr = 'Job '+job_id
            index = webContent.replace(substr,'ignore', 1).find(substr)
            offset = 18
            webContent = webContent[index+offset:-1]

        #print(webContent)

        f = open(folder_path + job_id+'.html', 'w')
        f.write(webContent)
        f.close()
        return True
    except Exception as inst:
        print "Exception in the report page downloading from Metacentrum"
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst           # __str__ allows args to be printed directly
        return False


#save_job_report_page(folder_path='',job_id='1398409.arien-pro.ics.muni.cz')
