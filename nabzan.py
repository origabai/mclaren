from api import ArazimWarsBot, Emote, Exceptions, Monkeys
import random

EMOTES = [
    Emote.NONE,
    Emote.ANGRY,
    Emote.COOL,
    Emote.CRYING,
    Emote.FACEPALM,
    Emote.IDEA_THOUGHT,
    Emote.LAUGHING,
    Emote.LOVE,
    Emote.POINTING,
    Emote.SHOCKED,
    Emote.SMILE,
    Emote.THUMBS_DOWN,
    Emote.THUMBS_UP,
]

class MyBot(ArazimWarsBot):
    def setup(self) -> None:
        pass

    def run(self) -> None:
        self.handle_emotes()

    def handle_emotes(self) -> None:
        """
        emote handling
        """
        
        if random.randint(0, 240) == 0:
            self.context.log_info("EMOTED")
            self.context.display_emote(EMOTES[int(self.context.get_current_time()) % len(EMOTES)])
