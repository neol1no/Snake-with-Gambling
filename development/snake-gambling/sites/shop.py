import pygame
from sites.button import Button

class Shop:
    def __init__(self, game):
        self.game = game
        self.current_tab = "upgrades"  # or "cosmetics"
        self.upgrades = {
            "grow_rate": {
                "name": "Slower Growth",
                "description": "Snake grows slower",
                "cost": 10,
                "max_level": 5,
                "current_level": 1
            },
            "currency_multiplier": {
                "name": "Egg Multiplier",
                "description": "Double egg collection",
                "cost": 20,
                "max_level": 3,
                "current_level": 1
            }
        }
        self.skins = {
            "default": {
                "name": "Default",
                "cost": 0,
                "color": (0, 255, 0)
            },
            "gold": {
                "name": "Gold",
                "cost": 50,
                "color": (255, 215, 0)
            },
            "rainbow": {
                "name": "Rainbow",
                "cost": 100,
                "color": None
            }
        }
        self.unlocked_skins = ["default"]
        self.setup_buttons()

    def setup_buttons(self):
        button_width = 200
        button_height = 50
        center_x = self.game.width // 2 - button_width // 2
        
        tab_width = 150
        self.tab_buttons = {
            "upgrades": Button(center_x - tab_width - 10, 200, tab_width, button_height, "Upgrades"),
            "cosmetics": Button(center_x + 10, 200, tab_width, button_height, "Cosmetics")
        }
        
        button_x = self.game.width - button_width - 50
        self.upgrade_buttons = {
            "grow_rate": Button(button_x, 300, button_width, button_height, "Buy Grow Rate"),
            "currency_multiplier": Button(button_x, 370, button_width, button_height, "Buy Currency")
        }
        
        self.cosmetic_buttons = {
            "snake_skin": Button(button_x, 300, button_width, button_height, "Snake Skin: Default")
        }

    def draw(self, screen):
        screen.fill((20, 20, 20))
        font = pygame.font.Font(None, 74)
        title = font.render("Shop", True, (255, 255, 255))
        screen.blit(title, (self.game.width//2 - title.get_width()//2, 50))

        font = pygame.font.Font(None, 36)
        eggs_text = font.render(f"Eggs: {self.game.eggs}", True, (255, 255, 255))
        screen.blit(eggs_text, (10, 10))

        for button_name, button in self.tab_buttons.items():
            button.color = (150, 150, 150) if button_name == self.current_tab else (100, 100, 100)
            button.draw(screen)

        if self.current_tab == "upgrades":
            grow_rate_cost = self.game.upgrades["grow_rate"] * 100
            currency_cost = self.game.upgrades["currency_multiplier"] * 200
            
            grow_rate_text = f"Current: {self.game.upgrades['grow_rate']} eggs per length"
            currency_text = f"Current: {self.game.upgrades['currency_multiplier']}x multiplier"
            
            grow_rate_cost_text = f"Cost: {grow_rate_cost} eggs"
            currency_cost_text = f"Cost: {currency_cost} eggs"
            
            grow_rate_color = (255, 255, 255) if self.game.eggs >= grow_rate_cost else (128, 128, 128)
            currency_color = (255, 255, 255) if self.game.eggs >= currency_cost else (128, 128, 128)
            
            grow_rate_surface = font.render(grow_rate_text, True, grow_rate_color)
            currency_surface = font.render(currency_text, True, currency_color)
            grow_rate_cost_surface = font.render(grow_rate_cost_text, True, grow_rate_color)
            currency_cost_surface = font.render(currency_cost_text, True, currency_color)
            
            text_x = 50
            screen.blit(grow_rate_surface, (text_x, 300))
            screen.blit(grow_rate_cost_surface, (text_x, 330))
            screen.blit(currency_surface, (text_x, 370))
            screen.blit(currency_cost_surface, (text_x, 400))
            
            for button in self.upgrade_buttons.values():
                button.draw(screen)
        else:
            self.cosmetic_buttons["snake_skin"].text = f"Snake Skin: {self.game.snake_skin}"
            for button in self.cosmetic_buttons.values():
                button.draw(screen)

        back_text = font.render("Press ESC to return", True, (255, 255, 255))
        screen.blit(back_text, (self.game.width//2 - back_text.get_width()//2, self.game.height - 50))

    def handle_click(self, pos):
        # Check tab buttons
        for button_name, button in self.tab_buttons.items():
            if button.rect.collidepoint(pos):
                self.current_tab = button_name
                return

        # Check content buttons based on current tab
        if self.current_tab == "upgrades":
            for button_name, button in self.upgrade_buttons.items():
                if button.rect.collidepoint(pos):
                    if button_name == "grow_rate":
                        cost = self.game.upgrades["grow_rate"] * 100
                        if self.game.eggs >= cost:
                            self.game.eggs -= cost
                            self.game.upgrades["grow_rate"] += 1
                    elif button_name == "currency_multiplier":
                        cost = self.game.upgrades["currency_multiplier"] * 200
                        if self.game.eggs >= cost:
                            self.game.eggs -= cost
                            self.game.upgrades["currency_multiplier"] += 1
        else:
            for button_name, button in self.cosmetic_buttons.items():
                if button.rect.collidepoint(pos):
                    if button_name == "snake_skin":
                        # Add cosmetic skin logic here
                        pass 