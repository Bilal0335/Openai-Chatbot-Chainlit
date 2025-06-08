import os
from dotenv import load_dotenv
import chainlit as cl
import asyncio
from agents import Agent, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI, Runner

# Load environment variables
load_dotenv()

# Load Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Step 1: Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Step 2: Model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

# Step 3: Config
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# Step 4: Agent
agent = Agent(
    name="Panaversity Support Agent",
    model=model,
    instructions="You are a helpful assistant."
)

# Step 5: Chainlit message handler with streaming support
@cl.on_message
async def main(message: cl.Message):
    # Create a streaming message to send tokens incrementally
    msg = cl.Message(content="", stream=True)
    await msg.send()

    # Run the agent to get the response
    res = await Runner.run(
        starting_agent=agent,
        input=message.content,
        run_config=config
    )

    # Stream the response token-by-token (simulated)
    for token in res.final_output.split():
        await msg.stream_token(token + " ")
        await asyncio.sleep(0.02)  # Adjust delay for smoother streaming

    # Finalize the message update
    await msg.update()
