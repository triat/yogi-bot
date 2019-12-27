import factory
from yogi_web import models


class ServerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Server

    name = factory.Faker("word")
    ip = factory.Faker("ipv4")
    port = factory.Faker("pyint", min_value=27015, max_value=27215, step=1)


class MatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Match


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Team
