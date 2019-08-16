from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import re
import time
import dateutil.parser as parser
from datetime import datetime
import datetime
import json



def fetch_mail():
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify' 
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
       flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
       creds = tools.run_flow(flow, store)
    GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    user_id =  'me'
    label_id_one = 'Label_8279309830804272938'
    label_id_two = 'UNREAD'
	
    unread_msgs = GMAIL.users().messages().list(userId='me',labelIds=[label_id_one, label_id_two]).execute()
    
    mssg_list = unread_msgs['messages']
    print ("Total unread messages in inbox: ", str(len(mssg_list)))

    final_list=[]
    for mssg in mssg_list:
       temp_dict = { }
       m_id = mssg['id'] 
       message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute() 
       payld = message['payload']  
       headr = payld['headers'] 
    
       for t in headr: 
          if t['name'] == 'Date':
             msg_date = t['value']
             date_parse = (parser.parse(msg_date))
             m_date = (date_parse.date())
             m_time = (date_parse.time())
             temp_dict['Date'] = str(m_date)+" "+str(m_time)
          else:
             pass
       	
       for one in headr:
          if one['name'] == 'Subject':
             msg_subject = one['value']
             temp_dict['Subject'] = msg_subject
          else:
            pass
          
       for two in headr:
          if two['name'] == 'From':
             msg_from = two['value']
             temp_dict['Sender'] = msg_from
          else:
             pass
       
       temp_dict['Snippet'] = message['snippet'] 
       return_dict = split_n_sent(temp_dict['Sender'],temp_dict['Subject'],temp_dict['Date'],temp_dict['Snippet'])
       final_list.append(return_dict)
    return final_list

def split_n_sent(sender,subject,date_time,snippet):
    
    m_data={}
    m_data["sender"]=sender
    m_data["subject"]=subject
    m_data["date_time"]=date_time

    m_body={}
    body_split= snippet.split(";")
    m_body["reason"]=body_split[0].split(":")[1]
    m_body["Name"]=body_split[1].split(":")[1]
    m_body["Emp ID"]=int(body_split[2].split(":")[1])
    m_body["Leave Type"]=body_split[3].split(":")[1]

    m_data["body"]=m_body
    return m_data

def run_modules():
    first_mod=fetch_mail()
    json_data=json.dumps(first_mod)
    print("json")
    print(json_data)
    print("###")

def main():
    run_modules()

if __name__ == '__main__':
    main()
