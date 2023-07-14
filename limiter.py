from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def configure_rate_limits(app, default_limits=["20 per hour"]):
    limiter = Limiter(key_func=get_remote_address, app=app, default_limits=default_limits)
 

    return app
