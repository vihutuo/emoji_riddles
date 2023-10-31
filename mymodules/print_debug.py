import flet as ft
import pendulum


def GetCurrentDateTime(tmz="Asia/Kolkata"):
    now = pendulum.now(tmz)
    return now


class PrintDebug:

    def __init__(self, txt_msg: ft.Text, is_debug=True):
        self.txt_msg = txt_msg
        self.is_debug = is_debug

    async def print_msg(self,msg: str):
        self.txt_msg.value += GetCurrentDateTime().to_iso8601_string() + " : " + str(msg) + "\n"
        await self.txt_msg.update_async()
