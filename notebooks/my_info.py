import os
from dotenv import load_dotenv, set_key

class MyInfo:
    def __init__(self, env_path = '.env'):
        self._env_path = env_path

    def _load_env_variable(self, var_name, value_type=str, split_char=','):
        load_dotenv(self._env_path, override=True)
        var_str = os.getenv(var_name)
        if not var_str:
            raise ValueError(f'{var_name} missing from .env - run setup_notebook.ipynb.')
        return [value_type(item) for item in var_str.split(split_char)]
    
    def _set_env_variable(self, key, values):
        value = ','.join(str(v) for v in values)
        set_key(self._env_path, key, value)

    def get_wallets(self):
        wallets = self._load_env_variable('MY_WALLETS')
        return wallets
    
    def set_wallets(self, wallets):
        wallets = [wallet.lower() for wallet in wallets]
        self._set_env_variable('MY_WALLETS', wallets)
        self.get_wallets()

    def get_club_ids(self):
        club_ids = self._load_env_variable('MY_CLUB_IDS', value_type=int)
        return club_ids

    def set_club_ids(self, club_ids):
        self._set_env_variable('MY_CLUB_IDS', club_ids)
        self.get_club_ids()

    def get_owner_ids(self):
        owner_ids = self._load_env_variable('MY_OWNER_IDS', value_type=int)
        return owner_ids
    
    def set_owner_ids(self, owner_ids):
        self._set_env_variable('MY_OWNER_IDS', owner_ids)
        self.get_owner_ids()

