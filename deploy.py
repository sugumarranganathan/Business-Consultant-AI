import vertexai
from vertexai.agent_engines import AdkApp

from agent import root_agent

PROJECT_ID = "project-415b525b-5ad3-4185-aeb"
LOCATION = "asia-south1"
STAGING_BUCKET = "gs://business-consultant-agent-415b525b"

client = vertexai.Client(
    project=PROJECT_ID,
    location=LOCATION,
)

app = AdkApp(
    agent=root_agent,
)

remote_agent = client.agent_engines.create(
    agent=app,
    config={
        "display_name": "Business Consultant AI Agent",
        "staging_bucket": STAGING_BUCKET,
        "requirements": [
            "google-cloud-aiplatform[agent_engines,adk]>=1.112.0",
            "google-adk",
            "cloudpickle",
            "pydantic>=2.6.4",
        ],
    },
)

print("\n========================================")
print("DEPLOYMENT SUCCESSFUL")
print("========================================")
print("Resource name:")
print(remote_agent.api_resource.name)
