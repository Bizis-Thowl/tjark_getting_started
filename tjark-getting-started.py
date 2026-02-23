from openai import OpenAI
import os
from dotenv import load_dotenv
import instructor
from response_model.Capital import CapitalResponse
from prompts.capital import CAPITAL_PROMPT
from init_phoenix import init_phoenix
from opentelemetry.trace import StatusCode
load_dotenv()

MODEL = os.getenv("MODEL")

def main(user_request: str, tracer):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("BASE_URL"))
    client = instructor.from_openai(client)
    prompt = CAPITAL_PROMPT.format(user_request=user_request)
    
    with tracer.start_as_current_span("Capital", openinference_span_kind="agent") as span:
        span.set_input("user_request_prompt", prompt)
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            response_model=CapitalResponse
        )
        span.set_output("capital_response", response)
        span.set_status(StatusCode.OK)
    return response
    
    
if __name__ == "__main__":
    
    tracer = init_phoenix("tjark-getting-started")
    
    
    main(user_request="What is the capital of France?", tracer=tracer)