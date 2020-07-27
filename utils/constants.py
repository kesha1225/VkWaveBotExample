from vkwave.bots import Keyboard, ButtonColor

MENU_KB = Keyboard()
MENU_KB.add_text_button(text="Игры", payload={"command": "games"}, color=ButtonColor.POSITIVE)
MENU_KB.add_row()
MENU_KB.add_text_button(text="Профиль", payload={"command": "profile"}, color=ButtonColor.SECONDARY)
MENU_KB.add_row()
MENU_KB.add_text_button(text="Бонус", payload={"command": "bonus"}, color=ButtonColor.POSITIVE)

GAMES_KB = Keyboard()
GAMES_KB.add_text_button(text="Орел или Решка", payload={"command": "coin_flip"}, color=ButtonColor.SECONDARY)
GAMES_KB.add_row()
GAMES_KB.add_text_button(text="Меню", color=ButtonColor.NEGATIVE)
