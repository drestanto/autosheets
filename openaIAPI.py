import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

def structurized(text):
	completion = openai.ChatCompletion.create(
	  model="gpt-3.5-turbo",
	  messages=[
	    {"role": "system", "content": "You are a personal finance management system. You get a string of text as a prompt, your job is to output a structurized text of `item,expenses,category`. Just output with that format, if there are more than one item, just seperate it with newline"},
	    {"role": "user", "content": text}
	  ]
	)
	result = completion.choices[0].message.content
	print(result)

if __name__ == "__main__":
	text = (f"East Repair Inc.\n"
			f"\n"
			f"1912 Harvest Lane\n"
			f"New York, NY 12210\n"
			f"\n"
			f"BILLTO SHIP TO\n"
			f"\n"
			f"John Smith, John Smith\n"
			f"\n"
			f"2.Court Square 3787 Pineview Drive\n"
			f"New York, NY 12210 Cambridge, MA 12210\n"
			f"\n"
			f"RECEIPT # uUs-001\n"
			f"RECEIPT DATE 11/02/2019\n"
			f"P.O.# 2312/2019\n"
			f"DUE DATE 26/02/2019\n"
			f"\n"
			f"Receipt Total\n"
			f"\n"
			f"$154.06\n"
			f"\n"
			f"QTY DESCRIPTION\n"
			f"\n"
			f"1 Front and rear brake cables\n"
			f"2 New set of pedal arms\n"
			f"\n"
			f"3 Labor 3hrs\n"
			f"\n"
			f"TERMS & CONDITIONS\n"
			f"\n"
			f"Payment is due within 15 days\n"
			f"\n"
			f"Please make checks payable to: East Repair Inc.\n"
			f"\n"
			f"UNIT PRICE AMOUNT\n"
			f"100.00 100.00\n"
			f"\n"
			f"15.00 30.00\n"
			f"\n"
			f"5.00 15.00\n"
			f"\n"
			f"Subtotal 145.00\n"
			f"\n"
			f"Sales Tax 6.25% 9.06\n"
			f"\n"
			f"Sith,\n"
			f"\n"
			f"\n"
			)
	structurized(text)