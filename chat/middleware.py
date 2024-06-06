import logging
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from useraccount.models import User
from urllib.parse import parse_qs



logger = logging.getLogger(__name__)


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self,scope,receive,send):
        query_string = parse_qs(scope['query_string'].decode())
        token = query_string.get("token")
        if token:
            try:
                access_token = AccessToken(token[0])
                user = await User.objects.aget(id=access_token['user_id'])
                scope['user'] = user
            except Exception as e:
                logger.error(f'Token authentication failed: {e}')
                scope['user'] = None
        else:
            scope['user'] = None
        return await super().__call__(scope,receive,send)