from openai import OpenAI
client = OpenAI()
 
assistant = client.beta.assistants.create(
  name="Code Documentation Assistant",
  instructions="You are an expert Developer specialised in deploying Infrastucture as Code (IaC) with Terraform and Python. You work for a team that uses various Terraform product repositories to deploy and manage assets in AWS across multiple AWS accounts. Your knowledge base includes the README file of every Terraform product and module that the team uses to manage the AWS infra. Use your knowledge base to answer questions about the documentation and the Terraform products that they pertain to.",
  model="gpt-4-turbo",
  tools=[{"type": "file_search"}],
)

# Create a vector store caled "Financial Statements"
vector_store = client.beta.vector_stores.create(name="Public Cloud READMEs")

# Ready the files for upload to OpenAI
file_paths = ["found-documents/goog-10k.pdf", "found-documents/brka-10k.txt"]
file_streams = [open(path, "rb") for path in file_paths]

# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)

# You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)
