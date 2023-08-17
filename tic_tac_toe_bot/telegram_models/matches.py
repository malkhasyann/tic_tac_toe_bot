from telegram_models.gamer import Gamer
from telegram_models.pair_session import PairSession
from models.session import GameSession


class Matches:
    def __init__(self):
        self.data: dict[tuple, PairSession] = {}
        self.gamers: list[Gamer] = []
        self.sessions: list[PairSession] = []
    
    def add_match(self, session: PairSession) -> None:
        self.data[(session.gamer1.user.id, session.gamer2.user.id)] = session
        if session in self.sessions:
            self.sessions.remove(session)
        
    def add_session(self, session: PairSession) -> None:
        self.sessions.append(session)
        
    def add_gamer(self, gamer: Gamer) -> None:
        self.gamers.append(gamer)
        
    def delete_gamer(self, gamer: Gamer) -> None:
        if gamer in self.gamers:
            self.gamers.remove(gamer)
            
    def delete_match_by_gamer_id(self, id: int) -> None:
        opp = self.get_gamer_opponent_by_id(id)
        if opp:
            try:
                del self.data[(id, opp.user.id)]
            except:
                del self.data[(opp.user.id, id)]
        
    def get_gamer_by_id(self, id: int) -> Gamer | None:
        for gamer in self.gamers:
            if gamer.user.id == id:
                return gamer
            
        return None
    
    def get_session_by_id(self, id: int) -> PairSession | None:
        for ids, session in self.data.items():
            if id in ids:
                 return session
             
        return None
    
    def get_session_by_code(self, code: str) -> PairSession | None:
        for session in self.sessions:
            if session.code == code:
                return session
            
        return None    
    
    def get_gamer_opponent_by_id(self, id: int) -> Gamer | None:
        for (id1, id2) in self.data:
            if id == id1:
                return self.get_gamer_by_id(id2)
            if id == id2:
                return self.get_gamer_by_id(id1)
        return None
    
    def get_game_session_by_gamer(self, gamer: Gamer) -> GameSession | None:
        for pair in self.data:
            if gamer.user.id in pair:
                return self.data[pair].session
            
        return None
    
    def get_waiting_session_by_id(self, id: int) -> PairSession | None:
        for session in self.sessions:
            if session.gamer1.user.id == id:
                return session
            
        return None