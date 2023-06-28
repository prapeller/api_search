import logging

logger = logging.getLogger(__name__)


def elastic_backoff(details):
    e = details['exception']
    message = f'{e.error} {e.info}'.replace('\n', ' ')
    tries = details['tries']
    wait = details['wait']
    logger.error(f'{tries=:}, wait:{wait:0.1f}, {message=:}')
