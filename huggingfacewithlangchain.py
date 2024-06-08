# pip install huggingface pip install transformers
# pip install accelerate pip install bitsandbytes
import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain import HuggingFaceHub

os.environ["HUGGINGFACE_API_TOKEN"] = "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"
