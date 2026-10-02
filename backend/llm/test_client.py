from client import client


response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Say hello in one short sentence."
)

print(response.text)