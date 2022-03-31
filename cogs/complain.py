from discord import Message, Embed
from discord.ext.commands import Cog, command, Bot


class TimComplain(Cog):
    def __init__(self, bot: Bot):
        self.tim = bot
        self.complaints = [
            [
                [
                    "c1",
                    "ots"
                ],
                "I don't want to do a C1 OTS"
            ],
            [
                [
                    "situ"
                ],
                "VATCANSitu is a terrible plugin, change my mind"
            ],
            [
                [
                    "c-mode"
                ],
                "C mode is too hard to use"
            ]
        ]

    def find_matching_complaint(self, keywords: list):
        for item in self.complaints:
            print(f"Looking inside {item} with keywords {keywords}")
            if keywords == item[0]:
                print(f"Match, {keywords}")
                return item[1]
        return None

    @Cog.listener()
    async def on_message(self, message: Message):
        content: str = message.content
        if "tim" in content.lower():
            keywords = ["situ", "c1", "ots", "c-mode"]
            if any([keyword in keywords for keyword in message.content.lower().split(" ")]):
                ctxkws = []
                for word in message.content.lower().split(" "):
                    if word in keywords:
                        ctxkws.append(word)
                complaint = self.find_matching_complaint(ctxkws)
                if complaint is None:
                    return
                await message.channel.send(complaint)
        await self.tim.process_commands(message)


def setup(bot):
    return bot.add_cog(TimComplain(bot))
