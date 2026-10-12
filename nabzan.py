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
        self.player_count = 0
        self.emote_timer = 120

    def run(self) -> None:
        self.handle_emotes()

    def handle_emotes(self) -> None:
        """
        emote handling
        """

        if self.emote_timer <= 0:
            self.context.display_emote(Emote.COOL)
        self.emote_timer -= 1

        curr_count = self.context.get_player_count()
        if curr_count < self.player_count:
            self.context.display_emote(Emote.LAUGHING)
            self.emote_timer = 60 * 4

        self.player_count = curr_count

