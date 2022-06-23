from datetime import timedelta
from django.utils import timezone
from tokenize import Token
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed



class ExpiringTokenAuthentication(TokenAuthentication):
    """   # expires in :  actual - creada = tiempo que falta
            Se puede optimizar pero para mayor legibilidad lo deje
            de esta manera.
            La variable TOKEN_EXPIRED_AFTER_SECONDS esta en el archivo settings
            
    """
    def expires_in(self,token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds= settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time
    
    
    """Como su nombre dice, verificar si el tiempo del token ha expirado
        Procede a llamar a la funcion expires_in() definida mas arriba.
          Esta fn se encarga de todo el calculo
        Se encarga solo de la comparacion
    """
    def is_token_expired(self,token):
        return self.expires_in(token) < timedelta(seconds = 0)



    """
    Esta funcion se encarga de obtener el valor de lo que ha pasado
    """
    def token_expire_handler(self,token):
        is_expire = self.is_token_expired(token)
        if is_expire:
            print('TOKEN EXPIRADO')
        
        return is_expire

    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.select_related('user').get(key = key)
        except self.get_model().DoesNotExist: #Tipo de exepcion
            raise AuthenticationFailed('Token invalido ')

        if not token.user.is_active:
            raise AuthenticationFailed('Usuario no activo o eliminado')

        is_expired = self.token_expire_handler(token)  
        if is_expired:
            raise AuthenticationFailed('Token invalido') 
        return