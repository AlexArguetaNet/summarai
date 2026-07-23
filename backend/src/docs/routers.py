
# Descriptions for summary router

SUMMARIZE_ENDPOINT_DESCRIPTION= """
Processes a block of text and generates a three-bullet-point summary using Meta **Llama 3.1 8B**.

### Key Requirements & Constraints:
* **Minimum Length:** Input text must contain at least **250 characters**.
* **Input Payload:** JSON object containing a `text` string field.

### Expected Output:
* Returns a JSON object with a `summary` key containing three single-sentence bullet points marked by asterisks.
* Accelerated by Groq LPU hardware for low-latency processing.
"""


