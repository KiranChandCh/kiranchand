import requests
import json

url = "https://michaelgathara.com/api/python-challenge"

response = requests.get(url)
challenges = response.json()

print(challenges)

def getResultFromResponse(input):
    try:
        result = eval(input)
        return result
    except ZeroDivisionError:
        return "Division by zero won't work"
    except SyntaxError:
        return "Syntax Error"

for item in challenges:
    getProblemValue = item['problem']
    
    # Remove the operator symbol
    inputData = getProblemValue[:-1]

    result = getResultFromResponse(inputData)
    print(f"Input: {getProblemValue} Output: {result}")
