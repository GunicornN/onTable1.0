import requests

url = "http://127.0.0.1:8000/api/companies/le-coq-69006/carts/"

payload = "{\n    \"table_number\" : 1,\n    \"payment_method\" : \"CB\",\n    \"person_name\" : \"Jean\",\n    \"company_slug\" : \"le-coq-69006\", \n    \"products\":[\n    \t{\n\t\t\t\"slug\":\"saucisson-de-lyon-le-vrai\",\n\t\t\t\"quantity\":2\n    \t},\n       \t{\n\t\t\t\"slug\":\"anchois-a-la-sauce-tomate\",\n\t\t\t\"quantity\":4\n    \t}\n    ],\n    \"formulas\": [\n    ]\n} "
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
