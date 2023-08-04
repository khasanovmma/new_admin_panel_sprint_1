from django.conf import settings

from split_settings.tools import include

include(
    "components/database.py",
)
