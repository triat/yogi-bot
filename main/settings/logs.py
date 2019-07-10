import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://f1a3c48906a143b29c2a392b4add2828@sentry.io/1501614",
    integrations=[DjangoIntegration()]
)
