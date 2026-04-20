from pydantic import ValidationError
from ..settings import AccountsSettings
import sys
from ..constants import ENV_PREFIX,SERVICE_NAME
from hyperlocal_platform.core.utils.settings_initializer import init_settings


SETTINGS: AccountsSettings  = init_settings(settings=AccountsSettings,service_name=SERVICE_NAME,env_prefix=ENV_PREFIX)
