from api import ArazimWarsBot, Emote, Exceptions, Monkeys
import random

EMOTES = [
    # Emote.NONE,
    Emote.ANGRY,
    # Emote.COOL,
    # Emote.CRYING,
    Emote.FACEPALM,
    # Emote.IDEA_THOUGHT,
    # Emote.LAUGHING,
    # Emote.LOVE,
    Emote.POINTING,
    # Emote.SHOCKED,
    # Emote.SMILE,
    # Emote.THUMBS_DOWN,
    # Emote.THUMBS_UP,
]


class MyBot(ArazimWarsBot):
    def setup(self) -> None:
        self.emote_index = 0
        self.emote_wait = False

    def run(self) -> None:
        self.handle_emotes()

    def handle_emotes(self) -> None:
        """
        emote handling
        """

        self.emote_index += 1
        if random.randint(0, 60 * 4) == 0:
            self.emote_wait = True

        if self.emote_index % 120 == 0:
            self.emote_wait = False

        if self.emote_wait:
            return

        self.context.display_emote(EMOTES[(self.emote_index) % len(EMOTES)])
