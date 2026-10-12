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
        self.players_alive = 0
        self.emote_timer = 0
        self.spam_timer = 0

    def run(self) -> None:
        self.handle_emotes()

    def handle_emotes(self) -> None:
        """
        emote handling
        """

        curr_alive = 0

        for i in range(self.context.get_player_count()):
            if self.context.is_player_active(i):
                curr_alive += 1

        if self.emote_timer <= 0:
            self.context.display_emote(Emote.COOL)
        self.emote_timer -= 1

        if curr_alive < self.players_alive:
            self.context.display_emote(Emote.LAUGHING)
            self.emote_timer = 60 * 4

        self.player_count = curr_alive

        if random.randint(0, 60 * 10):
            self.spam_timer = 60 * 4
            

