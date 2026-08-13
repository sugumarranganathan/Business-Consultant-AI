from functools import cached_property

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.genai import Client
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context



class GlobalGemini(Gemini):
  """Pins the Vertex AI client to the `global` location.

  gemini-3 series models are only served from `global`; the default ADK
  `Gemini` integration constructs a `google.genai.Client` whose location
  defaults to the AgentEngine instance's region (e.g. `us-central1`) and
  fails with model-not-found for these models. Subclassing per the override
  pattern documented on `google.adk.models.google_llm.Gemini` lets the agent
  keep running in its regional AgentEngine instance while routing the model
  request to the global endpoint.
  """

  @cached_property
  def api_client(self) -> Client:
    return Client(vertexai=True, location="global")


business_consultant_ai_agent_google_search_agent = LlmAgent(
  name='Business_Consultant_AI_Agent_google_search_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in performing Google searches.'
  ),
  sub_agents=[],
  instruction='Use the GoogleSearchTool to find information on the web.',
  tools=[
    GoogleSearchTool()
  ],
)
business_consultant_ai_agent_url_context_agent = LlmAgent(
  name='Business_Consultant_AI_Agent_url_context_agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Agent specialized in fetching content from URLs.'
  ),
  sub_agents=[],
  instruction='Use the UrlContextTool to retrieve content from provided URLs.',
  tools=[
    url_context
  ],
)
root_agent = LlmAgent(
  name='Business_Consultant_AI_Agent',
  model=GlobalGemini(model='gemini-3.5-flash'),
  description=(
      'Help small businesses understand and use AI.'
  ),
  sub_agents=[],
  instruction='You are a professional Business Consultant AI Agent.\n\nYour job is to help small businesses understand how they can use Artificial Intelligence.\n\nAlways:\n1. Explain concepts in simple English.\n2. Give practical business examples.\n3. Provide actionable recommendations.\n4. Use clear headings and bullet points.\n5. Avoid unnecessary technical jargon.\n6. If you do not know something, clearly say so.\n7. Never invent facts or business information.',
  tools=[
    agent_tool.AgentTool(agent=business_consultant_ai_agent_google_search_agent),
    agent_tool.AgentTool(agent=business_consultant_ai_agent_url_context_agent)
  ],
)
