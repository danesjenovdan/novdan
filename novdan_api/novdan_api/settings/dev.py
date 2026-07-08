from .base import *


# debug toolbar settings
def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    "RESULTS_CACHE_SIZE": 500,
}
