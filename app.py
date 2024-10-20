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

# Configure the tracer provider with a resource (service name)
trace.set_tracer_provider(TracerProvider(resource=resource))

# Set up Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",  # Jaeger service in docker-compose
    agent_port=6831,  # Jaeger agent UDP port
)

# Configure the tracer provider
trace.set_tracer_provider(TracerProvider())
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
