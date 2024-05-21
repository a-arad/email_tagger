import email
import pandas as pd

def mailbox_to_df(my_mail,data):
    """put email plaintexts, to, and from into dicts then form data frame from list of dicts"""
    
    emails = []

    for num in data[0].split():
        _, msg_data = my_mail.fetch(num, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                
                msg = email.message_from_bytes(response_part[1])
                mail_from = msg.get('From')
                mail_subject = msg.get('Subject')
                mail_content = ''

                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        cdispo = str(part.get('Content-Disposition'))

                        # skip attachments
                        if ctype == 'text/plain' and 'attachment' not in cdispo:
                            charset = part.get_content_charset('utf-8') 
                            payload = part.get_payload(decode=True)
                            try:
                                mail_content = payload.decode(charset)
                            except UnicodeDecodeError:
                                mail_content = payload.decode(charset, 'replace')  # replace undecodable chars
                            break
                else:
                    charset = msg.get_content_charset('utf-8') 
                    payload = msg.get_payload(decode=True)
                    try:
                        mail_content = payload.decode(charset)
                    except UnicodeDecodeError:
                        mail_content = payload.decode(charset, 'replace')

                # 
                emails.append({
                    'From': mail_from,
                    'Subject': mail_subject,
                    'Content': mail_content
                })

        email_df = pd.DataFrame(emails)
        return email_df