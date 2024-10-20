import os
from random import randint
from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

# Set service name
resource = Resource(attributes={
    ResourceAttributes.SERVICE_NAME: "dice-server"
})



# Retrieve Jaeger configuration from environment variables
JAEGER_HOST = os.getenv("JAEGER_AGENT_HOST", "localhost")  # Default to "localhost" if not set
JAEGER_PORT = int(os.getenv("JAEGER_AGENT_PORT", 6831))  # Default to port 6831 if not set

# Set up Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name=JAEGER_HOST,
    agent_port=JAEGER_PORT,
)

# Configure the tracer provider with a resource (service name)
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer_provider().get_tracer("diceroller.tracer")
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)

@app.route("/rolldice")
def roll_dice():
    return str(roll())

def roll():
    with tracer.start_as_current_span("roll") as rollspan:
        res = randint(1, 6)
        rollspan.set_attribute("roll.value", res)
        return res

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
