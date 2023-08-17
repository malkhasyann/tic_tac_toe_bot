from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr  # SecretStr for confidential data
    
    # Nested class for additional settings
    class Config:
        env_file = '.env'  # file name
        env_file_encoding = 'utf-8'  # file encoding
        
        
config = Settings()        