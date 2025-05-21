import pygame
from sites.button import Button

class Shop:
    def __init__(self, game):
        self.game = game
        self.current_tab = 0
        self.tabs = ["upgrades", "skins"]
        self.items = {
            "upgrades": {
            "grow_rate": {
                "name": "Slower Growth",
                    "description": "Grow every 1 egg",
                "cost": 10,
                    "level": 1,
                "max_level": 5,
                    "status": "Every 1 egg"
            },
            "currency_multiplier": {
                "name": "Egg Multiplier",
                    "description": "1x eggs per collect",
                "cost": 20,
                    "level": 1,
                "max_level": 3,
                    "status": "1x eggs"
            },
            "egg_magnet": {
                "name": "Egg Magnet",
                    "description": "Increases egg pickup range",
                "cost": 30,
                    "level": 0,
                "max_level": 3,
                    "status": "No magnet"
            },
            "golden_egg_chance": {
                "name": "Golden Egg Chance",
                "description": "Golden Egg chance: 0%",
                "cost": 50,
                "level": 0,
                "max_level": 5,
                "status": "0% chance"
            }
            },
            "skins": {
            "default": {
                "name": "Default",
                    "description": "Default green snake",
                    "cost": 0
            }
            }
        }
        self.setup_buttons()

    def setup_buttons(self):
        button_width = 200
        button_height = 50
        center_x = self.game.display_width // 2 - button_width // 2
        
        self.buttons = {
            "back": Button(center_x, self.game.height - 100, button_width, button_height, "Back", self.game)
        }

    def draw(self, screen):
        screen.fill((20, 20, 20))
        
        font = pygame.font.Font(None, int(74 * min(self.game.scale_x, self.game.scale_y)))
        title_shadow = font.render("Shop", True, (0, 0, 0))
        title_text = font.render("Shop", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.display_width//2, int(50 * self.game.scale_y)))
        screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title_text, title_rect)
        
        font = pygame.font.Font(None, int(36 * min(self.game.scale_x, self.game.scale_y)))
        eggs_text = font.render(f"{self.game.eggs}", True, (255, 255, 255))
        eggs_shadow = font.render(f"{self.game.eggs}", True, (0, 0, 0))
        egg_img = pygame.image.load("assets/egg.png").convert_alpha()
        egg_img = pygame.transform.scale(egg_img, (int(30 * self.game.scale_x), int(30 * self.game.scale_y)))
        screen.blit(egg_img, (int(10 * self.game.scale_x), int(10 * self.game.scale_y)))
        screen.blit(eggs_shadow, (int(45 * self.game.scale_x), int(12 * self.game.scale_y)))
        screen.blit(eggs_text, (int(43 * self.game.scale_x), int(10 * self.game.scale_y)))
        
        # tabs
        tab_width = int(200 * self.game.scale_x)
        tab_height = int(50 * self.game.scale_y)
        tab_spacing = int(20 * self.game.scale_x)
        total_width = (tab_width * len(self.tabs)) + (tab_spacing * (len(self.tabs) - 1))
        start_x = (self.game.display_width - total_width) // 2
        
        for i, tab in enumerate(self.tabs):
            tab_x = start_x + (i * (tab_width + tab_spacing))
            tab_y = int(300 * self.game.scale_y)
            
            # tab background
            pygame.draw.rect(screen, (40, 40, 40), (tab_x, tab_y, tab_width, tab_height), border_radius=int(10 * min(self.game.scale_x, self.game.scale_y)))
            pygame.draw.rect(screen, (60, 60, 60), (tab_x, tab_y, tab_width, tab_height), 2, border_radius=int(10 * min(self.game.scale_x, self.game.scale_y)))
            
            # tab text
            tab_font = pygame.font.Font(None, int(36 * min(self.game.scale_x, self.game.scale_y)))
            tab_text = tab_font.render(tab.capitalize(), True, (255, 255, 255))
            tab_text_rect = tab_text.get_rect(center=(tab_x + tab_width//2, tab_y + tab_height//2))
            screen.blit(tab_text, tab_text_rect)
        
        # items
        item_width = int(250 * self.game.scale_x)
        item_height = int(180 * self.game.scale_y)  
        item_spacing = int(20 * self.game.scale_x)
        items_per_row = 4
        start_x = (self.game.display_width - (item_width * items_per_row + item_spacing * (items_per_row - 1))) // 2
        
        for i, (item_id, item) in enumerate(self.items[self.tabs[self.current_tab]].items()):
            row = i // items_per_row
            col = i % items_per_row
            item_x = start_x + (col * (item_width + item_spacing))
            item_y = int(380 * self.game.scale_y) + (row * (item_height + int(20 * self.game.scale_y)))
            
            pygame.draw.rect(screen, (40, 40, 40), (item_x, item_y, item_width, item_height), border_radius=int(15 * min(self.game.scale_x, self.game.scale_y)))
            pygame.draw.rect(screen, (60, 60, 60), (item_x, item_y, item_width, item_height), 2, border_radius=int(15 * min(self.game.scale_x, self.game.scale_y)))
            
            name_font = pygame.font.Font(None, int(36 * min(self.game.scale_x, self.game.scale_y)))
            name_text = name_font.render(item['name'], True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(item_x + item_width//2, item_y + int(30 * self.game.scale_y)))
            screen.blit(name_text, name_rect)
            
            cost_font = pygame.font.Font(None, int(24 * min(self.game.scale_x, self.game.scale_y)))
            cost_text = cost_font.render(f"Cost: {item['cost']} eggs", True, (255, 255, 0))
            cost_rect = cost_text.get_rect(center=(item_x + item_width//2, item_y + int(60 * self.game.scale_y)))
            screen.blit(cost_text, cost_rect)
            
            if self.tabs[self.current_tab] == "upgrades":
                level_text = cost_font.render(f"Level: {item['level']}/{item['max_level']}", True, (200, 200, 200))
                level_rect = level_text.get_rect(center=(item_x + item_width//2, item_y + int(85 * self.game.scale_y)))
                screen.blit(level_text, level_rect)
            
            desc_font = pygame.font.Font(None, int(20 * min(self.game.scale_x, self.game.scale_y)))
            desc_text = desc_font.render(item['description'], True, (200, 200, 200))
            desc_rect = desc_text.get_rect(center=(item_x + item_width//2, item_y + int(110 * self.game.scale_y)))
            screen.blit(desc_text, desc_rect)
            
            button_width = int(100 * self.game.scale_x)
            button_height = int(30 * self.game.scale_y)
            button_x = item_x + (item_width - button_width) // 2
            button_y = item_y + item_height - int(40 * self.game.scale_y)
            
            if self.tabs[self.current_tab] == "upgrades":
                button_text = "Full" if item['level'] >= item['max_level'] else "Buy"
            else:  # Skins tab
                button_text = "Owned" if item_id in self.game.owned_skins else "Buy"
 
            pygame.draw.rect(screen, (60, 60, 60), (button_x, button_y, button_width, button_height), border_radius=int(5 * min(self.game.scale_x, self.game.scale_y)))
            pygame.draw.rect(screen, (60, 60, 60), (button_x, button_y, button_width, button_height), 2, border_radius=int(5 * min(self.game.scale_x, self.game.scale_y)))
            
            button_font = pygame.font.Font(None, int(24 * min(self.game.scale_x, self.game.scale_y)))
            button_text = button_font.render(button_text, True, (255, 255, 255))
            button_rect = button_text.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
            screen.blit(button_text, button_rect)
        
        esc_font = pygame.font.Font(None, int(24 * min(self.game.scale_x, self.game.scale_y)))
        esc_text = esc_font.render("Press ESC to go back", True, (200, 200, 200))
        esc_rect = esc_text.get_rect(center=(self.game.display_width//2, self.game.display_height - int(30 * self.game.scale_y)))
        screen.blit(esc_text, esc_rect)

    def handle_click(self, pos):
        tab_width = int(200 * self.game.scale_x)
        tab_height = int(50 * self.game.scale_y)
        tab_spacing = int(20 * self.game.scale_x)
        total_width = (tab_width * len(self.tabs)) + (tab_spacing * (len(self.tabs) - 1))
        start_x = (self.game.display_width - total_width) // 2
        
        for i, tab in enumerate(self.tabs):
            tab_x = start_x + (i * (tab_width + tab_spacing))
            tab_y = int(300 * self.game.scale_y)
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width, tab_height)
            if tab_rect.collidepoint(pos):
                self.current_tab = i
                return

        item_width = int(250 * self.game.scale_x)
        item_height = int(180 * self.game.scale_y)  
        item_spacing = int(20 * self.game.scale_x)
        items_per_row = 4
        start_x = (self.game.display_width - (item_width * items_per_row + item_spacing * (items_per_row - 1))) // 2
        
        for i, (item_id, item) in enumerate(self.items[self.tabs[self.current_tab]].items()):
            row = i // items_per_row
            col = i % items_per_row
            item_x = start_x + (col * (item_width + item_spacing))
            item_y = int(380 * self.game.scale_y) + (row * (item_height + int(20 * self.game.scale_y)))
            
            button_width = int(100 * self.game.scale_x)
            button_height = int(30 * self.game.scale_y)
            button_x = item_x + (item_width - button_width) // 2
            button_y = item_y + item_height - int(40 * self.game.scale_y)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            if button_rect.collidepoint(pos):
                if self.game.eggs >= item['cost']:
                    if self.tabs[self.current_tab] == "upgrades":
                        if item['level'] < item['max_level']:
                            self.game.eggs -= item['cost']
                            item['level'] += 1
                            if item_id == "grow_rate":
                                item['description'] = f"Grow every {item['level']} egg"
                            elif item_id == "currency_multiplier":
                                item['status'] = f"{item['level']}x eggs"
                                item['description'] = f"{item['level']}x eggs per collect"
                            elif item_id == "egg_magnet":
                                if item['level'] == 0:
                                    item['description'] = "Collect eggs by touching"
                                else:
                                    item['description'] = f"Pickup range: {item['level']} grid"
                            elif item_id == "golden_egg_chance":
                                item['description'] = f"Golden Egg chance: {5 * item['level']}%"
                            self.game.upgrades[item_id] = item['level']
                    elif self.tabs[self.current_tab] == "skins":
                        self.game.eggs -= item['cost']
                        self.game.snake_skin = item_id
                return

        if self.buttons["back"].handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos})):
            self.game.start_transition(self.game.previous_state) 