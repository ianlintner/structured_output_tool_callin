"""
Observability configuration for Pet Paradise Shop.
Includes OpenTelemetry tracing, Prometheus metrics, and Jaeger integration.
"""

import logging
import os
from typing import Optional

from dotenv import load_dotenv
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import Counter, Gauge, Histogram, start_http_server

load_dotenv()

# Configuration
SERVICE_NAME_VALUE = os.getenv("SERVICE_NAME", "pet-paradise-shop")
SERVICE_VERSION_VALUE = os.getenv("SERVICE_VERSION", "1.0.0")
OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT", "http://localhost:4317")
JAEGER_ENDPOINT = os.getenv("JAEGER_ENDPOINT", "http://localhost:14268/api/traces")
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "9090"))
ENABLE_TRACING = os.getenv("ENABLE_TRACING", "true").lower() == "true"
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"

# Resource describes the service
resource = Resource.create(
    {
        SERVICE_NAME: SERVICE_NAME_VALUE,
        SERVICE_VERSION: SERVICE_VERSION_VALUE,
        "deployment.environment": os.getenv("ENVIRONMENT", "development"),
    }
)

# Initialize tracer
tracer_provider: Optional[TracerProvider] = None
meter_provider: Optional[MeterProvider] = None

# Prometheus metrics
request_count = Counter("petshop_requests_total", "Total number of requests", ["method", "endpoint", "status"])

request_duration = Histogram("petshop_request_duration_seconds", "Request duration in seconds", ["method", "endpoint"])

active_requests = Gauge("petshop_active_requests", "Number of active requests")

pet_inventory_count = Gauge("petshop_inventory_count", "Number of pets in inventory", ["pet_type"])

order_count = Counter("petshop_orders_total", "Total number of orders", ["status"])

tool_calls = Counter("petshop_tool_calls_total", "Total number of tool calls", ["tool_name", "success"])


def setup_tracing():
    """Configure OpenTelemetry tracing with OTLP and Jaeger exporters."""
    global tracer_provider

    if not ENABLE_TRACING:
        logging.info("Tracing is disabled")
        return

    try:
        # Create OTLP span exporter
        otlp_exporter = OTLPSpanExporter(
            endpoint=OTLP_ENDPOINT, insecure=True  # Use secure=True in production with proper certificates
        )

        # Create trace provider
        tracer_provider = TracerProvider(resource=resource)

        # Add span processor
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

        # Set as global tracer provider
        trace.set_tracer_provider(tracer_provider)

        # Instrument libraries
        FastAPIInstrumentor().instrument()
        HTTPXClientInstrumentor().instrument()
        PymongoInstrumentor().instrument()
        LoggingInstrumentor().instrument(set_logging_format=True)

        logging.info(f"✓ OpenTelemetry tracing configured with endpoint: {OTLP_ENDPOINT}")

    except Exception as e:
        logging.error(f"Failed to setup tracing: {e}")
        logging.info("Application will continue without tracing")


def setup_metrics():
    """Configure OpenTelemetry metrics with Prometheus exporter."""
    global meter_provider

    if not ENABLE_METRICS:
        logging.info("Metrics are disabled")
        return

    try:
        # Create Prometheus metric reader
        prometheus_reader = PrometheusMetricReader()

        # Create OTLP metric exporter
        otlp_metric_exporter = OTLPMetricExporter(endpoint=OTLP_ENDPOINT, insecure=True)

        # Create periodic exporting metric reader for OTLP
        otlp_reader = PeriodicExportingMetricReader(
            otlp_metric_exporter, export_interval_millis=60000  # Export every 60 seconds
        )

        # Create meter provider with both readers
        meter_provider = MeterProvider(resource=resource, metric_readers=[prometheus_reader, otlp_reader])

        # Set as global meter provider
        metrics.set_meter_provider(meter_provider)

        # Start Prometheus HTTP server
        start_http_server(port=PROMETHEUS_PORT)

        logging.info(f"✓ Prometheus metrics server started on port {PROMETHEUS_PORT}")
        logging.info(f"✓ OTLP metrics configured with endpoint: {OTLP_ENDPOINT}")

    except Exception as e:
        logging.error(f"Failed to setup metrics: {e}")
        logging.info("Application will continue without metrics")


def get_tracer(name: str):
    """Get a tracer instance."""
    return trace.get_tracer(name, SERVICE_VERSION_VALUE)


def get_meter(name: str):
    """Get a meter instance."""
    return metrics.get_meter(name, SERVICE_VERSION_VALUE)


def record_request(method: str, endpoint: str, status: int, duration: float):
    """Record HTTP request metrics."""
    try:
        request_count.labels(method=method, endpoint=endpoint, status=status).inc()
        request_duration.labels(method=method, endpoint=endpoint).observe(duration)
    except Exception as e:
        logging.debug(f"Failed to record request metrics: {e}")


def record_pet_inventory(pet_type: str, count: int):
    """Record pet inventory metrics."""
    try:
        pet_inventory_count.labels(pet_type=pet_type).set(count)
    except Exception as e:
        logging.debug(f"Failed to record inventory metrics: {e}")


def record_order(status: str):
    """Record order metrics."""
    try:
        order_count.labels(status=status).inc()
    except Exception as e:
        logging.debug(f"Failed to record order metrics: {e}")


def record_tool_call(tool_name: str, success: bool):
    """Record tool call metrics."""
    try:
        tool_calls.labels(tool_name=tool_name, success=str(success).lower()).inc()
    except Exception as e:
        logging.debug(f"Failed to record tool call metrics: {e}")


def increment_active_requests():
    """Increment active requests counter."""
    try:
        active_requests.inc()
    except Exception as e:
        logging.debug(f"Failed to increment active requests: {e}")


def decrement_active_requests():
    """Decrement active requests counter."""
    try:
        active_requests.dec()
    except Exception as e:
        logging.debug(f"Failed to decrement active requests: {e}")


def init_observability():
    """Initialize all observability components."""
    logging.info("Initializing observability stack...")
    setup_tracing()
    setup_metrics()
    logging.info("✓ Observability stack initialized")


# Initialize on module import if running as main application
if __name__ != "__main__":
    try:
        init_observability()
    except Exception as e:
        logging.warning(f"Observability initialization failed: {e}")
        logging.info("Application will continue without full observability")
