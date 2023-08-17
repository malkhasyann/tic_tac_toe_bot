import random
import string

from models.session import GameSession
from telegram_models.gamer import Gamer

def generate_key() -> str:
    symbols = string.hexdigits
    return ''.join(random.choice(symbols) for i in range(8))


class PairSession:
    def __init__(self, gamer1: Gamer) -> None:
        self.gamer1: Gamer = gamer1
        self.gamer2: Gamer = None
        self.code: str = generate_key()
        self.session: GameSession = None
        
    def to_pair(self, gamer2: Gamer) -> None:
        self.gamer2 = gamer2
        self.session = GameSession(self.gamer1.player, self.gamer2.player)
        
    def __contains__(self, gamer: Gamer) -> bool:
        return gamer is self.gamer1 or gamer is self.gamer2
    
    def get_opponent(self, gamer: Gamer) -> Gamer | None:
        if gamer is self.gamer1: return self.gamer2
        if gamer is self.gamer2: return self.gamer1
        return None