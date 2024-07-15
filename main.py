import os
import random
import discord
from dotenv import load_dotenv
import pytesseract
import urllib.request
from PIL import Image
import openai
from datetime import date
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = discord.Client(intents=discord.Intents.default())
openai.api_key = OPENAI_API_KEY

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1g8ShzIvCdP3cPxMMfM6x6x77U7SWAcbR8Fraz4i14Bo"
TOTAL_EXPENSES_RANGE = "F1:J1"

def structurized(text):
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      temperature=0.8,
      messages=[
        {"role": "system", "content": "You are a personal finance management system. You get a string of text as a prompt, your job is to output a structurized text of `item;expenses;category`. Make sure there are no semicolon other than th seperator. Just output with that format, if there are more than one item, seperate it with newline. Don't add something that is not human recognizable as an expense"},
        {"role": "user", "content": text}
      ]
    )
    result = completion.choices[0].message.content

    # return the structered
    return result

def pictotext(image_url):
    # Open the image file
    image = Image.open(image_url)

    # Perform OCR using PyTesseract
    text = pytesseract.image_to_string(image)

    # Return the extracted text
    return text

def get_total():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=TOTAL_EXPENSES_RANGE)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    # print("Total Expenses: " + str(values[0][1]))
    # print("Total Item: " + str(values[0][4]))
    return values[0][4]
  except HttpError as err:
    print(err)

def get_total_expenses():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=TOTAL_EXPENSES_RANGE)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    # print("Total Expenses: " + str(values[0][1]))
    # print("Total Item: " + str(values[0][4]))
    return values[0][1]
  except HttpError as err:
    print(err)


def write(expense_array):
  TOTAL_ITEM = int(get_total())
  RANGE_VALUE = "A" + str(TOTAL_ITEM+2) + ":D"
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE_VALUE, valueInputOption='RAW', body={'values':[expense_array]})
        .execute()
    )
    values = result.get("values", [])
  except HttpError as err:
    print(err)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    to_sheet = []
    print(message.content)
    if (message.content):
        structered_receipt = structurized(textified_picture)
        for expense_item in structered_receipt.split("\n"):
        	arrayify_expense = expense_item.split(";")
        	if arrayify_expense[1].replace(".", "").isnumeric():
        		arrayify_expense = [date.today().strftime("%Y-%m-%d"),arrayify_expense[0],float(arrayify_expense[1]),arrayify_expense[2]]
        		to_sheet.append(arrayify_expense)
    if (len(message.attachments)!=0):
        picture_url = message.attachments[0].url
        local_url = "temp.png"
        print(picture_url)
        await message.attachments[0].save(local_url)
        textified_picture = pictotext(local_url)
        # print(textified_picture)
        structered_receipt = structurized(textified_picture)
        for expense_item in structered_receipt.split("\n"):
        	arrayify_expense = expense_item.split(";")
        	if arrayify_expense[1].replace(".", "").isnumeric():
        		arrayify_expense = [date.today().strftime("%Y-%m-%d"),arrayify_expense[0],float(arrayify_expense[1]),arrayify_expense[2]]
        		to_sheet.append(arrayify_expense)

    for expense_array in to_sheet:
    	write(expense_array)
    total_expense_now = get_total_expenses()
    print("Total Expenses Til Now = " + str(total_expense_now))

    response = "Progress saved ✅\nTotal Expense = " + str(total_expense_now)
    await message.channel.send(response)

client.run(TOKEN)