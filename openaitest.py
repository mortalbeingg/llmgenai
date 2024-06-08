import openai
import pandas as pd
from openai import OpenAI

mykey = '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'

openai.api_key= mykey
models = openai.models.list().data

pd.DataFrame(models)

client = OpenAI(api_key = mykey)

response = client.chat.completions.create(
    model ='gpt-3.5-turbo',
    messages = [
    {
        'role' : 'user',
        'content': 'how can i make money'
    }
      ]
)



response.choices[0].message.content

response1 = client.completions.create(
    model ='gpt-3.5-turbo',
    messages = [
    {
        'role' : 'user',
        'content': 'when did india win the first world cup'
    }
      ]
)

response1.choices[0].message.content 

description = "Aakriti is a student of IIT Delhi. She studies computer science
   engineering. Her last semester grade was 8.85. She is also part of the Data science club in the college."
   
prompt = f'''
 please extract the following information from the given text and return it as a JSON object:
 
 name
 college
 grades
 club

this is the body of the text to extract the information from:
{description}
'''
response2 = client.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages=[
        {
            'role': 'user',
            'content':prompt
            
        }
    ]
)

output = response2.choices[0].message.content
 
import json
output = json.loads(response2) 

student_info = [{           
                "name": "extract_student_info",
                "description": "Get the student description from the given text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "the name of the student",
                        },
                        "college": { "type": "string", 
                                    "description":'the student's college name",
                                    },
                       "grade": {
                            "type": "integer",
                            "description": "the grades of the student",
                        },
                           "club": {
                            "type": "string",
                            "description": "the name of the club the student is a part of",
                        },
                    }
                }
    }
                
]

response3 = client.chat.completions.create( 
    model = 'gpt-3.5=turbo',
    messages = [{'role':'user', 'content': prompt}]
    functions = student_info
    )

print(response3.choices[0].message.function_call.arguments)

json.loads((response3.choices[0].message.function_call.arguments))

student1 = ''' Aakriti is a student of IIT Delhi. She studies computer science engineering.
 Her last semester grade was 8.85. She is also a part of the Data science club in the college.'''
 
student2 = ''' Gauri is a student of IIT Mumbai. She studies computer science engineering.
 Her last semester grade was 9.45. She is also a part of the AI club in the college.'''

student_list =[student1,student2]










