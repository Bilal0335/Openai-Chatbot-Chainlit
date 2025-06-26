import chainlit as cl
import os
import asyncio
import re
from agents import Agent, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI, Runner
from dotenv import load_dotenv

# Environment variables load kar rahe hain jisme Gemini API key honi chahiye
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Gemini ko OpenAI-compatible bana kar use kar rahe hain
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

@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history", [])
    history.append({"role": "user", "content": message.content})

    # Purani conversation ko combine kar ke prompt bana rahe hain
    prompt = ""
    for entry in history:
        role = entry["role"]
        content = entry["content"]
        prompt += f"{'User' if role == 'user' else 'Assistant'}: {content}\n"

    res = await Runner.run(
        starting_agent=agent,
        input=prompt,
        run_config=config
    )

    history.append({"role": "assistant", "content": res.final_output})
    cl.user_session.set("history", history)

    msg = cl.Message(content="")
    await msg.send()

    # Streaming effect ke liye response ko token mein tod kar bhej rahe hain
    tokens = re.findall(r'\S+|\n', res.final_output)
    for token in tokens:
        await msg.stream_token(token + " ")
        await asyncio.sleep(0.03)

    await msg.update()
