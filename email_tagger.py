import pandas as pd
from get_completion import get_completion
from mailbox_to_df import mailbox_to_df
import imaplib
import yaml 

#

def connectmailbox(credentials_fp, imap_url, label = 'inbox'):
    #Load the user name and passwd from yaml file
    with open(credentials_fp,'r') as f:
        content = f.read()

    creds = yaml.load(content, Loader=yaml.FullLoader)
    user, password = creds["user"], creds["password"]    

    # Connection with GMAIL using SSL
    my_mail = imaplib.IMAP4_SSL(imap_url)

    # Log in using your credentials
    my_mail.login(user, password)

    # Select the Inbox to fetch messages
    my_mail.select(label)
    
    return my_mail


my_mail = connectmailbox('credentials.yml','imap.gmail.com')


type, data = my_mail.search(None,'ALL')


email_df = mailbox_to_df(my_mail,data)


with open('find_database_emails_prompt.md','r') as f:
    email_prompt = f.read()


for _,row in email_df.iloc[0:5].iterrows():
    list_of_inputs = [email_prompt,row['From'],"\n",row['Subject'],"\n",row['Content']]
    email_prompt_plus_input = " ".join(list_of_inputs)
    print(get_completion(email_prompt_plus_input))