import chainlit as cl
import os
from agents import Agent, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI, Runner
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

agent = Agent(
    name="Panaversity Support Agent",
    model=model,
    instructions="You are a helpful assistant."
)

# @cl.on_chat_start
# async def on_chat_start():
#     cl.user_session.set("history", [])
#     await cl.Message(content="Welcome to the Panaversity Support Agent! How can I assist you today?").send()

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    welcome_text = (
        "Welcome to BilalCode Support Agent!\n\n"
        "I'm here to assist you with any inquiries regarding our educational programs, "
        "technical support, and general information. Please don't hesitate to ask your questions.\n\n"
        "Let's get started!"
    )
    await cl.Message(content=welcome_text).send()

# @cl.on_message
# async def on_message(message: cl.Message):
#     history = cl.user_session.get("history", [])

#     # Append user input to history
#     history.append({"role": "user", "content": message.content})

#     # Create a prompt by concatenating history messages
#     prompt = ""
#     for entry in history:
#         role = entry["role"]
#         content = entry["content"]
#         if role == "user":
#             prompt += f"User: {content}\n"
#         else:
#             prompt += f"Assistant: {content}\n"

#     # Run agent with full conversation prompt
#     res = await Runner.run(
#         starting_agent=agent,
#         input=prompt,
#         run_config=config
#     )

#     # Append assistant response to history
#     history.append({"role": "assistant", "content": res.final_output})

#     cl.user_session.set("history", history)

#     await cl.Message(content=res.final_output).send()


# ! Eample 3
import chainlit as cl
import os
import asyncio
import re
from agents import Agent, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI, Runner
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Setup OpenAI-compatible provider for Gemini
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

agent = Agent(
    name="BilalCode Support Agent",
    model=model,
    instructions="You are a helpful and professional assistant."
)

# On chat start
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    welcome_text = (
        "👋 Welcome to **BilalCode Support Agent**!\n\n"
        "I'm here to assist you with any inquiries regarding development, learning, technical support, "
        "or general questions.\n\n"
        "💬 Just type your question to get started!"
    )
    await cl.Message(content=welcome_text).send()

# On user message
@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history", [])
    history.append({"role": "user", "content": message.content})

    # Create prompt from history
    prompt = ""
    for entry in history:
        role = entry["role"]
        content = entry["content"]
        prompt += f"{'User' if role == 'user' else 'Assistant'}: {content}\n"

    # Get agent response
    res = await Runner.run(
        starting_agent=agent,
        input=prompt,
        run_config=config
    )

    # Add assistant reply to history
    history.append({"role": "assistant", "content": res.final_output})
    cl.user_session.set("history", history)

    # Streaming output
    msg = cl.Message(content="")
    await msg.send()

    # Tokenize response smartly (preserve newlines)
    tokens = re.findall(r'\S+|\n', res.final_output)

    for token in tokens:
        await msg.stream_token(token + " ")
        await asyncio.sleep(0.03)  # Adjust speed here

    await msg.update()


# ! example 1
# import chainlit as cl
# import os
# import asyncio
# from agents import Agent, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI, Runner
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY")
# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY environment variable is not set.")

# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=provider
# )

# config = RunConfig(
#     model=model,
#     model_provider=provider,
#     tracing_disabled=True
# )

# agent = Agent(
#     name="BilalCode Support Agent",
#     model=model,
#     instructions="You are a helpful assistant."
# )

# @cl.on_chat_start
# async def on_chat_start():
#     cl.user_session.set("history", [])
#     welcome_text = (
#         "Welcome to BilalCode Support Agent!\n\n"
#         "I'm here to assist you with any inquiries regarding our educational programs, "
#         "technical support, and general information. Please don't hesitate to ask your questions.\n\n"
#         "Let's get started!"
#     )
#     await cl.Message(content=welcome_text).send()

# @cl.on_message
# async def on_message(message: cl.Message):
#     history = cl.user_session.get("history", [])

#     # Append user input to history
#     history.append({"role": "user", "content": message.content})

#     # Create a prompt by concatenating history messages
#     prompt = ""
#     for entry in history:
#         role = entry["role"]
#         content = entry["content"]
#         if role == "user":
#             prompt += f"User: {content}\n"
#         else:
#             prompt += f"Assistant: {content}\n"

#     # Run agent with full conversation prompt
#     res = await Runner.run(
#         starting_agent=agent,
#         input=prompt,
#         run_config=config
#     )

#     # Append assistant response to history
#     history.append({"role": "assistant", "content": res.final_output})
#     cl.user_session.set("history", history)

#     # Streaming response to user
#     msg = cl.Message(content="")
#     await msg.send()

#     for token in res.final_output.split():
#         await msg.stream_token(token + " ")
#         await asyncio.sleep(0.01)  # Slow down streaming if needed

#     await msg.update()


# ! Example 2
# import chainlit as cl
# import os
# import asyncio
# from agents import Agent, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI, Runner
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY")
# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY environment variable is not set.")

# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=provider
# )

# config = RunConfig(
#     model=model,
#     model_provider=provider,
#     tracing_disabled=True
# )

# agent = Agent(
#     name="Panaversity Support Agent",
#     model=model,
#     instructions="You are a helpful assistant."
# )

# @cl.on_chat_start
# async def on_chat_start():
#     cl.user_session.set("history", [])
#     await cl.Message(content="Welcome to the Panaversity Support Agent! How can I assist you today?").send()

# @cl.on_message
# async def on_message(message: cl.Message):
#     history = cl.user_session.get("history", [])

#     # Append user input to history
#     history.append({"role": "user", "content": message.content})

#     # Create a prompt by concatenating history messages
#     prompt = ""
#     for entry in history:
#         role = entry["role"]
#         content = entry["content"]
#         if role == "user":
#             prompt += f"User: {content}\n"
#         else:
#             prompt += f"Assistant: {content}\n"

#     # Run agent with full conversation prompt
#     res = await Runner.run(
#         starting_agent=agent,
#         input=prompt,
#         run_config=config
#     )

#     # Append assistant response to history
#     history.append({"role": "assistant", "content": res.final_output})
#     cl.user_session.set("history", history)

#     # Simulate streaming by sending tokens/chunks one by one
#     msg = cl.Message(content="")
#     await msg.send()

#     for token in res.final_output.split():
#         await msg.stream_token(token + " ")
#         await asyncio.sleep(0.01)  # Adjust speed here

#     await msg.update()

