import os
import re
import json
import base64
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pytz
import openai
import requests
from jira import JIRA
from ApiClassification import PRE_PROMPT

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# from dotenv import load_dotenv
# load_dotenv()

  # take environment variables from .env.

# from langchain.agents import load_tools
# from langchain.agents import initialize_agent
# from langchain.agents import AgentType
# from langchain.llms import OpenAI, HuggingFaceHub, HuggingFacePipeline
# from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig, pipeline
# import torch

JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_API_KEY = os.getenv("JIRA_API")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
SERVER = f'https://{JIRA_DOMAIN}.atlassian.net'
GSCOPES = ['https://www.googleapis.com/auth/gmail.compose',
           'https://www.googleapis.com/auth/gmail.readonly',
           'https://www.googleapis.com/auth/calendar']

# REDIRECT = 'https://d059-34-29-244-42.ngrok-free.app'
REDIRECT = 'http://localhost:5000'

openai.api_key = os.getenv("OPENAI_API_KEY")

def friday_openai():

    def predict(message,model="gpt-3.5-turbo"):
        completion = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": message}])
        return completion.choices[0].message["content"]


    def parse_json(message):
        response:str = predict(message,model="gpt-3.5-turbo-0301")

        json_start = response.find("{")
        json_end = response.rfind("}")

        print(response[json_start:json_end+1])
        event =  json.loads(response[json_start:json_end+1])
        return event


    def jira(messages):

        jira = JIRA(
                    server=SERVER,
                    basic_auth=(JIRA_USERNAME, JIRA_API_KEY)
                    )

        pre_message = PRE_PROMPT[1] + f"The statement is '{messages}'"
        instruct_dict = parse_json(pre_message)
        operation = instruct_dict["operation"]
        name:str = instruct_dict["project_name"]

        key = name.upper().strip()

        if "key" in instruct_dict.keys():
            key = instruct_dict["key"] if instruct_dict["key"] is not None \
            and instruct_dict["key"]!="" else key
        key = re.sub("[^A-Z]","",key)
        if len(key)>10:
            key = key[:10]


        def get_project(name:str,projects):
            name = name.strip().lower().replace(" ","")
            for project in projects:
                p_name = project.name.lower().replace(" ","")
                if  p_name == name :
                    return project
            return None


        def create_project(jira,name):
            # description = "-"  if not instruct_dict["description"]\
            #  else instruct_dict["description"]
            try:
                print(key)
                project = jira.create_project(
                key=key,
                name=name,
                template_name='Kanban software development',
                # description=description
                )
            except Exception as ex:
                print(ex.args)
                projects = jira.projects()
                project = get_project(name,projects)
                if project:
                    return f"Successfully created a new Jira project with name '{project.name}'"
            return f"Could not create a new Jira Project '{name}'"


        def delete_project(jira,name):
            try:
                projects = jira.projects()
                project = get_project(name,projects)
                if project:
                    endpoint_url = SERVER + f'/rest/api/2/project/{project.key}'
                    response = jira._session.delete(endpoint_url, params={'delete': 'true'})
                    if response.status_code == 204:
                        return f"permanently deleted project '{name}'"

                    return f"Project '{name}' could not be deleted."

                return f"could not delete Jira project '{name}'"
            except requests.exceptions.HTTPError as error:
                return f'Request failed to Jira API with status code: {error.response.status_code}'


        def get_project_status(jira,name):
            try:
                projects = jira.projects()
                project = get_project(name,projects)
                if project:
                    project = jira.project(project.key)

                    issues = jira.search_issues(f'project={project.key}', maxResults=False)

                    status_string = ""
                    for issue in issues:
                        pre_string = "Status:"
                        if issue.fields.issuetype.name !="Story":
                            pre_string = "Issue in:"
                        status_string += f"{pre_string} '{issue.fields.status}'\n"
                        if issue.fields.summary:
                            status_string += f"with summary: '{issue.fields.summary}'\n"
                        if issue.fields.description:
                            status_string += f"with description: '{issue.fields.description}'\n"
                        if issue.fields.assignee:
                            status_string += f"and assigned to: '{issue.fields.assignee}'\n"
                        if issue.fields.reporter:
                            status_string += f"and reports to: '{issue.fields.reporter}'\n"
                        if issue.fields.priority:
                            status_string += f"having priority: '{issue.fields.priority}'\n"
                        if issue.fields.issuetype:
                            status_string += f"with type: '{issue.fields.issuetype}'\n"

                    return status_string
                return f"Could not get status for project '{name}'"
            except Exception as ex:
                print(ex.args)
                return f"Could not get status for project '{name}'"

        ops_map = {}
        ops_map["create"] = create_project
        ops_map["delete"] = delete_project
        ops_map["get"] = get_project_status

        return ops_map[operation](jira,name)


    def authenticate():

        flow = InstalledAppFlow.from_client_secrets_file(
        '3.json', GSCOPES,redirect_uri=REDIRECT)
        authorization_url, _ = flow.authorization_url(
                access_type='offline',include_granted_scopes='true',scopes=GSCOPES)
        return authorization_url


    def googlecal(messages):

        now = datetime.now(pytz.utc)
        formatted_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')

        if not os.path.exists("token.json"):
            creds = authenticate()
            return creds
        creds = Credentials.from_authorized_user_file('token.json', scopes=GSCOPES)

        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()

        # Get the time zone information from the calendar
        time_zone = pytz.timezone(calendar['timeZone'])

        pre_message = PRE_PROMPT[2] + formatted_time + \
            f" and using timezone: {time_zone.zone}" +\
            f". The statement is '{messages}'"

        event = parse_json(pre_message)

        event = service.events().insert(calendarId='primary', body=event).execute()
        return 'Event created: %s' % (event.get('htmlLink'))


    def gmail(messages):

        pre_message = PRE_PROMPT[3] + f"'{messages}'"
        event = parse_json(pre_message)

        if not os.path.exists("token.json"):
            creds = authenticate()
            return creds
        creds = Credentials.from_authorized_user_file('token.json', scopes=GSCOPES)
        to_recep = event["to"]
        subject = event["subject"]
        content = event["message"]

        if not subject:
            subject = "No subject"

        if "@" not in to_recep:
            service = build('people', 'v1', credentials=creds)
            connections = service.people().connections().list(
            resourceName='people/me',
            personFields='names,emailAddresses').execute()

            for person in connections.get('connections', []):
                names = person.get('names', [])
                if names[0]["displayName"] == to_recep:
                    email_addresses = person.get('emailAddresses', [])
                if email_addresses:
                    to_recep = email_addresses[0]["value"]

        service = build('gmail', 'v1', credentials=creds)
        message = MIMEMultipart()
        message['to'] = to_recep
        message['subject'] = subject
        body = MIMEText(content)
        message.attach(body)
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        try:
            _ = (service.users().messages()
                    .send(userId='me', body={'raw': raw_message}).execute())
            # os.remove("token.json")
            return f'The message was sent to {to_recep}'
        except Exception as error:
            print(error.args)
            return 'An error occurred: {error}'


    def slack():
        return "The API call Integration is in progress for slack"

    def run(messages):

        pre_message = PRE_PROMPT[0]+  "The statement is " + f'"{messages}"'
        prompt_cls = predict(pre_message)

        classification = "else"
        value = messages

        if prompt_cls.lower() not in ["else","google cal","slack","jira"]:
            json_start = prompt_cls.find("{")
            json_end = prompt_cls.rfind("}")
            response = json.loads(prompt_cls[json_start:json_end+1])
            classification = response["name"].lower()
            value = response["value"].lower()

        print(classification)
        func = {}
        func["jira"] = jira
        func["google cal"] = googlecal
        func["gmail"] = gmail
        func["slack"] = slack

        if classification !="else":
            return func[classification](value)
        return predict(messages,model="gpt-3.5-turbo-0301")

    return run

# def friday_openai(tools=[]):
#     llm = OpenAI(temperature=0)
#     #Combine desired tools with better tools
#     agent_tools = tools + ["llm-math", "serpapi"]
#     tools = load_tools(agent_tools, llm=llm)
#
#     agent = initialize_agent(
#             tools,
#             llm,
#             agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#             verbose=True)
#
#     return agent

def friday_flan(tools=[]):
    return
#     llm = HuggingFaceHub(repo_id="google/flan-t5-xl",
#           model_kwargs={"temperature":0, "max_length":64})
#     #Combine desired tools with better tools
#     agent_tools = tools + ["llm-math", "serpapi"]
#     tools = load_tools(agent_tools, llm=llm)
#     agent = initialize_agent(
#             tools,
#             llm,
#             agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#             verbose=True)
#     return agent

def friday_alpaca(tools=[]):
    return
#     tokenizer = LlamaTokenizer.from_pretrained("chavinlo/alpaca-native")
#
#     base_model = LlamaForCausalLM.from_pretrained(
#         "chavinlo/alpaca-native",
#         load_in_8bit=False,
#         device_map="auto",
#         offload_folder="offload",
#         torch_dtype=torch.float16
#     )
#     pipe = pipeline(
#         "text-generation",
#         model=base_model,
#         tokenizer=tokenizer,
#         max_length=256,
#         temperature=0.6,
#         top_p=0.95,
#         repetition_penalty=1.2
#     )
#
#     local_llm = HuggingFacePipeline(pipeline=pipe)
#     agent = initialize_agent(
#             tools,
#             local_llm,
#             agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#             verbose=True)
#     return agent
