from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from todos.models import Todo
from users.tests.api.factories import UserFactory


class TodoFactory(DjangoModelFactory):
    class Meta:
        model = Todo

    user = SubFactory(UserFactory)
    title = Faker("sentence", nb_words=4)
    description = Faker("text")
    completed = Faker("boolean")
    created_at = Faker("date_time_this_year")
