import minihelper_backend.settings


def proxy():
    if minihelper_backend.settings.USE_PROXY:
        # add proxy if needed
        return {}
    else:
        return {}