from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from langchain import LLMChain, PromptTemplate
from langchain.llms import Baseten
from langchain.memory import ConversationBufferWindowMemory

import os

app = Flask(__name__)

template = """Assistant is a large language model.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

I want you to act as Morgan Freeman giving advice and answering questions. You will reply with what he would say.
SMS: {sms_input}
Assistant:"""

prompt = PromptTemplate(input_variables=["sms_input"], template=template)
basten_model_id = os.environ['BASETEN_MODEL_ID']

sms_chain = LLMChain(
    llm=Baseten(model=basten_model_id),
    prompt=prompt,
    memory=ConversationBufferWindowMemory(k=2),
    llm_kwargs={"max_length": 4096}
)

@app.route("/", methods=['GET'])
def hello():
    return "Hi, This Bot has been built with LangChain, Llama2 and Baseten. How may I help you today?"

@app.route("/predict", methods=['GET', 'POST'])
def sms():
    resp = MessagingResponse()
    inb_msg = request.data if request.data else request.form['Body'].lower().strip()
    output = sms_chain.predict(sms_input=inb_msg)
    print(output)
    resp.message(output)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
