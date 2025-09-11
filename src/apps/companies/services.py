from abc import ABC, abstractmethod


class BaseBotLoader(ABC):

    def __init__(self, bot_id: int):
        self.bot_id = bot_id

    @abstractmethod
    def get_bot(self):
        raise NotImplementedError
