from langchain_core.messages import SystemMessage
from langchain.chat_models import init_chat_model
from langchain_core.messages.utils import count_tokens_approximately
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres import AsyncPostgresStore
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langmem.short_term import SummarizationNode
from database.config import load_config_to_env
from database.user import get_user_by_id
from agents.tools import coding_tools, researcher_tools
from dotenv import load_dotenv
from agents import tools

# -------------------
# Setup
# -------------------
load_dotenv()
DB_URI = "postgresql://Magomed:1M2a3g4a5.@localhost:5432/agent_db"
llm = init_chat_model("groq:qwen/qwen3-32b", temperature=0)

summarization_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=llm,
    max_tokens=4000,
    max_summary_tokens=1000,
    output_messages_key="llm_input_messages",
)

coding_agent = create_react_agent(
    llm,
    tools=coding_tools,
    name="coding_agent",
    prompt="You can only generate code ... ALWAYS web_search before coding.",
    pre_model_hook=summarization_node
)

supervisor = create_supervisor(
    model=llm,
    tools=researcher_tools,
    agents=[coding_agent],
    prompt="You are a supervisor agent ... do one agent at a time.",
    add_handoff_back_messages=True,
    output_mode="full_history",
    pre_model_hook=summarization_node
)

# -------------------
# Call Assistant
# -------------------

async def call_assistant(message, user_id: str):
    user_info = await get_user_by_id(user_id=user_id)
    tools.user_id = user_id
    await load_config_to_env(user_id=user_id)

    async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer, \
               AsyncPostgresStore.from_conn_string(
                   DB_URI,
                   index={"embed": "huggingface:sentence-transformers/all-mpnet-base-v2",
                          "dims": 1536,
                          "fields": ["text"]}
               ) as store:
        await checkpointer.setup()
        await store.setup()
        graph = supervisor.compile(checkpointer=checkpointer, store=store)
        system_msg = SystemMessage(
            content=f"""
                You are an intelligent, helpful personal assistant built using a multi-agent system architecture. Your tools include web search, weather and time lookups, code execution, and GitHub integration. You work inside a Telegram interface and respond concisely, clearly, and informatively.

                The user you are assisting is:
                - **Name**: {user_info.get('first_name', 'Unknown') or 'Unknown'} {user_info.get('last_name', '') or ''}
                - **User ID**: {user_id}
                - **Location**: {user_info.get('location', 'Unknown') or 'Unknown'}
                - **Coordinates**: ({user_info.get('latitude', 'N/A') or 'N/A'}, {user_info.get('longitude', 'N/A') or 'N/A'})

                You may use their location when answering weather or time-related queries. If the location is unknown, you may ask the user to share it.

                Stay helpful, respectful, and relevant to the user's query.
            """.strip()
        )

        result = await graph.ainvoke(
            input={"messages": [system_msg, message]},
            config={"configurable": {"thread_id": user_id}}
        )
        for m in result['messages']:
            m.pretty_print()
        return result
