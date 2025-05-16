import pygame

class Shop:
    def __init__(self, game):
        self.game = game
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

    def draw(self, screen):
        screen.fill((20, 20, 20))
        font = pygame.font.Font(None, 74)
        title = font.render("Shop", True, (255, 255, 255))
        screen.blit(title, (self.game.width//2 - title.get_width()//2, 50))

        font = pygame.font.Font(None, 36)
        eggs_text = font.render(f"Eggs: {self.game.eggs}", True, (255, 255, 255))
        screen.blit(eggs_text, (10, 10))

        y_offset = 150
        for upgrade_id, upgrade in self.upgrades.items():
            color = (255, 255, 255) if self.game.eggs >= upgrade["cost"] else (128, 128, 128)
            name_text = font.render(f"{upgrade['name']} (Level {upgrade['current_level']}/{upgrade['max_level']})", True, color)
            desc_text = font.render(upgrade["description"], True, (200, 200, 200))
            cost_text = font.render(f"Cost: {upgrade['cost']} eggs", True, color)
            
            screen.blit(name_text, (50, y_offset))
            screen.blit(desc_text, (50, y_offset + 30))
            screen.blit(cost_text, (50, y_offset + 60))
            y_offset += 120

        y_offset = 150
        for skin_id, skin in self.skins.items():
            color = (255, 255, 255) if self.game.eggs >= skin["cost"] else (128, 128, 128)
            name_text = font.render(f"{skin['name']} Skin", True, color)
            cost_text = font.render(f"Cost: {skin['cost']} eggs", True, color)
            
            screen.blit(name_text, (self.game.width - 300, y_offset))
            screen.blit(cost_text, (self.game.width - 300, y_offset + 30))
            y_offset += 80

        back_text = font.render("Press ESC to return", True, (255, 255, 255))
        screen.blit(back_text, (self.game.width//2 - back_text.get_width()//2, self.game.height - 50))

    def handle_click(self, pos):
        x, y = pos
        if y < 150:
            return

        upgrade_clicked = False
        y_offset = 150
        for upgrade_id, upgrade in self.upgrades.items():
            if y_offset <= y <= y_offset + 90:
                if self.game.eggs >= upgrade["cost"] and upgrade["current_level"] < upgrade["max_level"]:
                    self.game.eggs -= upgrade["cost"]
                    upgrade["current_level"] += 1
                    upgrade["cost"] *= 2
                    if upgrade_id == "grow_rate":
                        self.game.upgrades["grow_rate"] = upgrade["current_level"]
                    elif upgrade_id == "currency_multiplier":
                        self.game.upgrades["currency_multiplier"] = 2 ** (upgrade["current_level"] - 1)
                upgrade_clicked = True
                break
            y_offset += 120

        if not upgrade_clicked:
            y_offset = 150
            for skin_id, skin in self.skins.items():
                if y_offset <= y <= y_offset + 60:
                    if self.game.eggs >= skin["cost"] and skin_id not in self.unlocked_skins:
                        self.game.eggs -= skin["cost"]
                        self.unlocked_skins.append(skin_id)
                    elif skin_id in self.unlocked_skins:
                        self.game.snake_skin = skin_id
                    break
                y_offset += 80 