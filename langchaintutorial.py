import langchain
import openai

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

mykey = "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"
openai.api_key = mykey
client = OpenAI(openai_api_key=mykey)

prompt = """can u tell me the total number of countries in asia.
can you give me top 10 countries name?"""

# zero shot prompting
client.predict(prompt).strip()

client.predict("what is the capital of india?")

prompt = PromptTemplate(
    input_variables=["country"], template="what is the capital of {country}"
)

prompt.format(country="india")

client.predict(prompt.format(country="india"))
prompt = prompt.from_template("what is the name of a good {product} company?")

client.predict(prompt.format(product="toys"))

prompt = "can you tell me the current GDP of India"
client.predict(prompt)

# agents:used to connect to a 3rd party api or function
# for extracting real time info, i will use serp api
# and using serp api, i will call google search engine
# and i will extract real time info

# pip install google-search-results
serpapi_key = "04fc30e3a403b39135121001f14016593add706a9f8958a6bfbb542bed6cfaa8"

from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from langchain.llms import OpenAI

client = OpenAI(openai_api_key=mykey)

tool = load_tools(["serpapi"], serpapi_api_key=serpapi_key, llm=client)

agent = initialize_agent(
    tool, client, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run("who won the world cup recently")

# pip install wikipedia

tool = load_tools(["wikipedia"], llm=client)
agent = initialize_agent(
    tool, client, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
agent.run("can you tell me about recent world cup")

# chains
prompt = PromptTemplate.from_template("name any company that makes {product}")

from langchain.chains import LLMChain

chain = LLMChain(llm=client, prompt=prompt)
chain.run("wine").strip()


prompt_template = PromptTemplate(
    input_variables=["startup_name"],
    template="I want to start a startup for {startup_name}, suggest me a good and eye catching name",
)

name_chain = LLMChain(llm=client, prompt=prompt_template)

prompt_template2 = PromptTemplate(
    input_variables=["name"],
    template="How should i start with building {name} startup?",
)

name_chain2 = LLMChain(llm=client, prompt=prompt_template2)

from langchain.chains import SimpleSequentialChain

newchain = SimpleSequentialChain(chains=[name_chain, name_chain2])
newchain.run("data science")

pt1 = PromptTemplate(
    input_variables=["cuisine"],
    template="I want to open a restaurant that has {cuisine}, suggest a fancy name for it",
)
name_chain = LLMChain(llm=client, prompt=pt1, output_key="restaurant_name")

pt2 = PromptTemplate(
    input_variables=["restaurant_name"],
    template="suggest some good selling menu items for {restaurant_name} restaurant",
)
items_chain = LLMChain(llm=client, prompt=pt2, output_key="menu_items")

from langchain.chains import SequentialChain

combinedchain = SequentialChain(
    chains=[name_chain, items_chain],
    input_variables=["cuisine"],
    output_variables=["restaurant_name", "menu_items"],
)

combinedchain({"cuisine": "indian"})

# pip install pypdf
# to use langchain.document_loaders.PyPDFLoader

from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader(r"/Users/aws/Downloads/certificate.pdf")
loader.load_and_split()


# memory


chain1 = LLMChain(llm=client, prompt=pt3)

chain1.run("colorful cups")

chain1.memory

type(chain1.memory)  # this will return NoneType

# conversationbuffermemory
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()

pt3 = PromptTemplate(
    input_variables=["product"],
    template="what is a good name for a company that makes {product}?",
)

chain2 = LLMChain(llm=client, prompt=pt3, memory=memory)

chain2.run("wines")
chain2.run("camera")
chain2.run("drone")
chain2.memory  # this will return a conversationbuffermemory object
chain2.memory.buffer  # this will return convo messages like Human: Wines AI: Vineyard cellars

# conversation chain

from langchain.chains import ConversationChain

convo = ConversationChain(llm=OpenAI(openai_api_key=mykey, temperature=0.7))
convo.prompt  # it will return a PromptTemplate object with some random info and empty human and  ai messages
convo.promt.template  # returns the prompt of above template

convo.run("who won the first world cup?")
convo.run("tell me what is 5+5")
convo.run("tell me what is 10+5")
convo.run("tell me who was the captain of the winning team")

# conversation buffer memory goes growing endlessly
# there is an option to remember last 5 conversation chain or just last 15 to 20 conversation chain

# ConversationBufferWindowMemory

from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=1)

convo = ConversationChain(llm=client, memory=memory)

convo.run("who won first world cup in cricket?")
convo.run("tell me whatis 5+5")
convo.run(
    "who was the captain of the winning team"
)  # it would say that it doesnt know as k =1, can only sustain the conversn memory till first prompt only

# by default with no k, it tracks the whole conversation
