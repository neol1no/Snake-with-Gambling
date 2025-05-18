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
                    "description": "Every 1 egg needed",
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
            }
            },
            "skins": {
            "default": {
                "name": "Default",
                    "description": "Default green snake",
                    "cost": 0
            },
            "gold": {
                "name": "Gold",
                    "description": "Golden snake",
                    "cost": 50
            },
            "rainbow": {
                "name": "Rainbow",
                    "description": "Rainbow snake",
                    "cost": 100
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
        
        # title
        title_font = pygame.font.Font(None, int(74 * min(self.game.scale_x, self.game.scale_y)))
        title_shadow = title_font.render("Shop", True, (0, 0, 0))
        title_text = title_font.render("Shop", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.display_width//2, int(200 * self.game.scale_y)))
        screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title_text, title_rect)
        
        # eggs count
        eggs_font = pygame.font.Font(None, int(36 * min(self.game.scale_x, self.game.scale_y)))
        eggs_shadow = eggs_font.render(f"Eggs: {self.game.eggs}", True, (0, 0, 0))
        eggs_text = eggs_font.render(f"Eggs: {self.game.eggs}", True, (255, 255, 255))
        eggs_rect = eggs_text.get_rect(center=(self.game.display_width//2, int(250 * self.game.scale_y)))
        screen.blit(eggs_shadow, (eggs_rect.x + 2, eggs_rect.y + 2))
        screen.blit(eggs_text, eggs_rect)
        
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
        item_width = int(300 * self.game.scale_x)
        item_height = int(180 * self.game.scale_y)  
        item_spacing = int(20 * self.game.scale_x)
        items_per_row = 3
        start_x = (self.game.display_width - (item_width * items_per_row + item_spacing * (items_per_row - 1))) // 2
        
        for i, (item_id, item) in enumerate(self.items[self.tabs[self.current_tab]].items()):
            row = i // items_per_row
            col = i % items_per_row
            item_x = start_x + (col * (item_width + item_spacing))
            item_y = int(380 * self.game.scale_y) + (row * (item_height + int(20 * self.game.scale_y)))
            
            # item background
            pygame.draw.rect(screen, (40, 40, 40), (item_x, item_y, item_width, item_height), border_radius=int(15 * min(self.game.scale_x, self.game.scale_y)))
            pygame.draw.rect(screen, (60, 60, 60), (item_x, item_y, item_width, item_height), 2, border_radius=int(15 * min(self.game.scale_x, self.game.scale_y)))
            
            # item name
            name_font = pygame.font.Font(None, int(36 * min(self.game.scale_x, self.game.scale_y)))
            name_text = name_font.render(item['name'], True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(item_x + item_width//2, item_y + int(30 * self.game.scale_y)))
            screen.blit(name_text, name_rect)
            
            # item cost
            cost_font = pygame.font.Font(None, int(24 * min(self.game.scale_x, self.game.scale_y)))
            cost_text = cost_font.render(f"Cost: {item['cost']} eggs", True, (255, 255, 0))
            cost_rect = cost_text.get_rect(center=(item_x + item_width//2, item_y + int(60 * self.game.scale_y)))
            screen.blit(cost_text, cost_rect)
            
            # item description
            desc_font = pygame.font.Font(None, int(24 * min(self.game.scale_x, self.game.scale_y)))
            desc_text = desc_font.render(item['description'], True, (200, 200, 200))
            desc_rect = desc_text.get_rect(center=(item_x + item_width//2, item_y + int(90 * self.game.scale_y)))
            screen.blit(desc_text, desc_rect)
            
            # level and status for upgrades
            if self.tabs[self.current_tab] == "upgrades":
                level_text = cost_font.render(f"Level: {item['level']}/{item['max_level']}", True, (200, 200, 200))
                level_rect = level_text.get_rect(center=(item_x + item_width//2, item_y + int(120 * self.game.scale_y)))
                screen.blit(level_text, level_rect)
                
                status_text = cost_font.render(item['status'], True, (200, 200, 200))
                status_rect = status_text.get_rect(center=(item_x + item_width//2, item_y + int(150 * self.game.scale_y)))
                screen.blit(status_text, status_rect)
                
                button_text = "Full" if item['level'] >= item['max_level'] else "Buy"
            else:  # Skins tab
                button_text = "Owned" if item_id in self.game.owned_skins else "Buy"
 
            button_width = int(100 * self.game.scale_x)
            button_height = int(30 * self.game.scale_y)
            button_x = item_x + (item_width - button_width) // 2
            button_y = item_y + item_height - int(40 * self.game.scale_y)
            
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

        item_width = int(300 * self.game.scale_x)
        item_height = int(180 * self.game.scale_y)
        item_spacing = int(20 * self.game.scale_x)
        items_per_row = 3
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
                                item['status'] = f"Every {item['level']} eggs"
                                item['description'] = f"Every {item['level']} eggs needed"
                            elif item_id == "currency_multiplier":
                                item['status'] = f"{item['level']}x eggs"
                                item['description'] = f"{item['level']}x eggs per collect"
                            self.game.upgrades[item_id] = item['level']
                    elif self.tabs[self.current_tab] == "skins":
                        self.game.eggs -= item['cost']
                        self.game.snake_skin = item_id
                return

        if self.buttons["back"].handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': pos})):
            self.game.start_transition(self.game.previous_state) 