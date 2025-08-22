print('authentication.py importado')

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from passageidentity import Passage, PassageError

# from passageidentity.openapi_client.models import UserInfo
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from core.models import User

PASSAGE_APP_ID = settings.PASSAGE_APP_ID
PASSAGE_API_KEY = settings.PASSAGE_API_KEY
psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY)


class TokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'core.authentication.TokenAuthentication'
    name = 'tokenAuth'
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name='Authorization',
            token_prefix='Bearer',
        )


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request) -> tuple[User, None] | None:
        auth_header = request.headers.get('Authorization')
        print(f'[DEBUG] Authorization header: {auth_header}')

        if not auth_header:
            print('[DEBUG] Nenhum header Authorization encontrado.')
            return None

        try:
            token = auth_header.split()[1]
            print(f'[DEBUG] Token extraído: {token}')
            psg_user_id: str = self._get_user_id(token)
            print(f'[DEBUG] Passage user id validado: {psg_user_id}')
            user: User = self._get_or_create_user(psg_user_id)
            print(f'[DEBUG] Usuário autenticado: {user}')
            return (user, None)
        except IndexError:
            print('[DEBUG] Header Authorization está em formato inválido.')
            return None
        except PassageError as e:
            print(f'[DEBUG] Erro PassageError: {e}')
            return None
        except AuthenticationFailed as e:
            print(f'[DEBUG] AuthenticationFailed: {e}')
            return None

    def _get_or_create_user(self, psg_user_id) -> User:
        try:
            user: User = User.objects.get(passage_id=psg_user_id)
            print(f'[DEBUG] Usuário encontrado no banco: {user}')
        except ObjectDoesNotExist:
            print(f'[DEBUG] Usuário não encontrado no banco, criando novo para Passage ID {psg_user_id}')
            psg_user = psg.user.get(psg_user_id)
            user: User = User.objects.create_user(
                passage_id=psg_user.id,
                email=psg_user.email,
            )
            print(f'[DEBUG] Novo usuário criado: {user}')

        return user

    def _get_user_id(self, token) -> str:
        try:
            psg_user_id: str = psg.auth.validate_jwt(token)
            print(f'[DEBUG] Token JWT validado com Passage, user_id: {psg_user_id}')
        except PassageError as e:
            print(f'[DEBUG] Falha na validação do token JWT: {e}')
            raise AuthenticationFailed(e.message) from e

        return psg_user_id

