
import pygame
import time
import threading
import json
import os
import sys
from datetime import datetime

class PomodoroTimer:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Window settings
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🍅 PomoPy - Pomodoro Timer")
        
        # Colors
        self.colors = {
            'background': (44, 62, 80),      # Dark blue-gray
            'panel': (52, 73, 94),           # Lighter blue-gray
            'work': (231, 76, 60),           # Red
            'short_break': (52, 152, 219),   # Blue
            'long_break': (155, 89, 182),    # Purple
            'green': (39, 174, 96),          # Green
            'orange': (243, 156, 18),        # Orange
            'white': (255, 255, 255),        # White
            'black': (0, 0, 0),              # Black
            'gray': (149, 165, 166),         # Gray
            'light_gray': (189, 195, 199)    # Light gray
        }
        
        # Fonts
        self.fonts = {
            'large': pygame.font.Font(None, 72),
            'medium': pygame.font.Font(None, 48),
            'small': pygame.font.Font(None, 32),
            'tiny': pygame.font.Font(None, 24)
        }
        
        # Timer variables
        self.time_left = 0
        self.timer_running = False
        self.timer_thread = None
        self.current_mode = "work"
        
        # Default times (in minutes)
        self.work_time = 25
        self.short_break_time = 5
        self.long_break_time = 15
        self.pomodoros_before_long_break = 4
        
        # Session tracking
        self.completed_pomodoros = 0
        self.total_work_time = 0
        
        # UI elements
        self.buttons = {}
        self.create_buttons()
        
        # Load settings
        self.load_settings()
        
        # Set initial mode
        self.set_mode("work")
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
        
    def create_buttons(self):
        """Create button objects for the UI"""
        button_width = 120
        button_height = 50
        spacing = 20
        
        # Control buttons (bottom row)
        start_x = (self.width - (button_width * 3 + spacing * 2)) // 2
        y = self.height - 100
        
        self.buttons['start'] = pygame.Rect(start_x, y, button_width, button_height)
        self.buttons['reset'] = pygame.Rect(start_x + button_width + spacing, y, button_width, button_height)
        self.buttons['pause'] = pygame.Rect(start_x + (button_width + spacing) * 2, y, button_width, button_height)
        
        # Mode buttons (middle row)
        mode_y = y - 80
        self.buttons['work'] = pygame.Rect(50, mode_y, 150, 40)
        self.buttons['short_break'] = pygame.Rect(220, mode_y, 150, 40)
        self.buttons['long_break'] = pygame.Rect(390, mode_y, 150, 40)
        self.buttons['settings'] = pygame.Rect(560, mode_y, 150, 40)
        
    def draw_button(self, rect, text, color, hover_color=None, text_color=None):
        """Draw a button with hover effect"""
        if text_color is None:
            text_color = self.colors['white']
        
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        
        # Choose color based on hover state
        button_color = hover_color if is_hovered and hover_color else color
        
        # Draw button
        pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
        pygame.draw.rect(self.screen, self.colors['black'], rect, 2, border_radius=10)
        
        # Draw text
        text_surface = self.fonts['small'].render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return is_hovered
        
    def draw_progress_bar(self, x, y, width, height, progress):
        """Draw a progress bar"""
        # Background
        pygame.draw.rect(self.screen, self.colors['gray'], (x, y, width, height), border_radius=height//2)
        
        # Progress
        progress_width = int(width * progress / 100)
        if progress_width > 0:
            pygame.draw.rect(self.screen, self.get_mode_color(), 
                           (x, y, progress_width, height), border_radius=height//2)
        
        # Border
        pygame.draw.rect(self.screen, self.colors['black'], (x, y, width, height), 2, border_radius=height//2)
        
    def get_mode_color(self):
        """Get the color for the current mode"""
        if self.current_mode == "work":
            return self.colors['work']
        elif self.current_mode == "short_break":
            return self.colors['short_break']
        else:
            return self.colors['long_break']
            
    def get_mode_name(self):
        """Get the display name for the current mode"""
        if self.current_mode == "work":
            return "WORK TIME"
        elif self.current_mode == "short_break":
            return "SHORT BREAK"
        else:
            return "LONG BREAK"
    
    def draw_timer_display(self):
        """Draw the main timer display"""
        # Timer panel
        panel_rect = pygame.Rect(50, 50, self.width - 100, 200)
        pygame.draw.rect(self.screen, self.colors['panel'], panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.colors['black'], panel_rect, 3, border_radius=15)
        
        # Mode label
        mode_text = self.fonts['medium'].render(self.get_mode_name(), True, self.get_mode_color())
        mode_rect = mode_text.get_rect(center=(self.width//2, 80))
        self.screen.blit(mode_text, mode_rect)
        
        # Time display
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        time_text = self.fonts['large'].render(time_str, True, self.colors['white'])
        time_rect = time_text.get_rect(center=(self.width//2, 140))
        self.screen.blit(time_text, time_rect)
        
        # Progress bar
        if self.current_mode == "work":
            total_time = self.work_time * 60
        elif self.current_mode == "short_break":
            total_time = self.short_break_time * 60
        else:
            total_time = self.long_break_time * 60
        
        progress = ((total_time - self.time_left) / total_time) * 100
        self.draw_progress_bar(100, 180, self.width - 200, 20, progress)
        
        # Progress percentage
        progress_text = self.fonts['tiny'].render(f"{progress:.1f}%", True, self.colors['white'])
        progress_rect = progress_text.get_rect(center=(self.width//2, 210))
        self.screen.blit(progress_text, progress_rect)
    
    def draw_stats(self):
        """Draw statistics panel"""
        # Stats panel
        stats_rect = pygame.Rect(50, 280, self.width - 100, 100)
        pygame.draw.rect(self.screen, self.colors['panel'], stats_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.colors['black'], stats_rect, 3, border_radius=15)
        
        # Stats title
        title_text = self.fonts['small'].render("SESSION STATISTICS", True, self.colors['white'])
        title_rect = title_text.get_rect(center=(self.width//2, 300))
        self.screen.blit(title_text, title_rect)
        
        # Stats content
        stats_text = f"Completed Pomodoros: {self.completed_pomodoros} | Total Work Time: {self.total_work_time} min"
        stats_surface = self.fonts['tiny'].render(stats_text, True, self.colors['white'])
        stats_rect = stats_surface.get_rect(center=(self.width//2, 330))
        self.screen.blit(stats_surface, stats_rect)
    
    def draw_buttons(self):
        """Draw all buttons"""
        # Control buttons
        self.draw_button(self.buttons['start'], "Start", self.colors['green'], 
                        (46, 204, 113), self.colors['white'])
        self.draw_button(self.buttons['reset'], "Reset", self.colors['work'], 
                        (192, 57, 43), self.colors['white'])
        self.draw_button(self.buttons['pause'], "Pause", self.colors['orange'], 
                        (211, 84, 0), self.colors['white'])
        
        # Mode buttons
        self.draw_button(self.buttons['work'], "Work", self.colors['work'], 
                        (192, 57, 43), self.colors['white'])
        self.draw_button(self.buttons['short_break'], "Short Break", self.colors['short_break'], 
                        (41, 128, 185), self.colors['white'])
        self.draw_button(self.buttons['long_break'], "Long Break", self.colors['long_break'], 
                        (142, 68, 173), self.colors['white'])
        self.draw_button(self.buttons['settings'], "Settings", self.colors['gray'], 
                        (108, 122, 137), self.colors['white'])
    
    def draw(self):
        """Draw the complete UI"""
        # Clear screen
        self.screen.fill(self.colors['background'])
        
        # Draw components
        self.draw_timer_display()
        self.draw_stats()
        self.draw_buttons()
        
        # Update display
        pygame.display.flip()
    
    def set_mode(self, mode):
        """Set the current timer mode"""
        self.current_mode = mode
        self.timer_running = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()
        
        if mode == "work":
            self.time_left = self.work_time * 60
        elif mode == "short_break":
            self.time_left = self.short_break_time * 60
        elif mode == "long_break":
            self.time_left = self.long_break_time * 60
    
    def start_timer(self):
        """Start or pause the timer"""
        if not self.timer_running:
            self.timer_running = True
            self.timer_thread = threading.Thread(target=self.timer_loop)
            self.timer_thread.daemon = True
            self.timer_thread.start()
        else:
            self.timer_running = False
    
    def reset_timer(self):
        """Reset the current timer"""
        self.timer_running = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()
        self.set_mode(self.current_mode)
    
    def timer_loop(self):
        """Main timer loop"""
        while self.timer_running and self.time_left > 0:
            time.sleep(1)
            if self.timer_running:
                self.time_left -= 1
        
        if self.time_left <= 0:
            self.timer_finished()
    
    def timer_finished(self):
        """Handle timer completion"""
        self.timer_running = False
        
        # Play sound (if available)
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("notification.wav")
            pygame.mixer.music.play()
        except:
            # Fallback: system beep
            print('\a')
        
        # Show completion message
        if self.current_mode == "work":
            self.completed_pomodoros += 1
            self.total_work_time += self.work_time
            
            if self.completed_pomodoros % self.pomodoros_before_long_break == 0:
                self.show_message("POMODORO COMPLETE!", f"Great job! You've completed {self.completed_pomodoros} pomodoros.\nTime for a LONG BREAK!")
                self.set_mode("long_break")
            else:
                self.show_message("POMODORO COMPLETE!", f"Work session complete!\nTake a short break.")
                self.set_mode("short_break")
        else:
            self.show_message("BREAK COMPLETE!", "Break time is over!\nReady to work again?")
            self.set_mode("work")
    
    def show_message(self, title, message):
        """Show a message dialog"""
        # Create a simple message overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(self.colors['black'])
        self.screen.blit(overlay, (0, 0))
        
        # Message box
        box_width = 500
        box_height = 200
        box_x = (self.width - box_width) // 2
        box_y = (self.height - box_height) // 2
        
        message_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, self.colors['panel'], message_rect, border_radius=15)
        pygame.draw.rect(self.screen, self.colors['black'], message_rect, 3, border_radius=15)
        
        # Title
        title_surface = self.fonts['medium'].render(title, True, self.get_mode_color())
        title_rect = title_surface.get_rect(center=(self.width//2, box_y + 50))
        self.screen.blit(title_surface, title_rect)
        
        # Message
        lines = message.split('\n')
        for i, line in enumerate(lines):
            message_surface = self.fonts['small'].render(line, True, self.colors['white'])
            message_rect = message_surface.get_rect(center=(self.width//2, box_y + 100 + i * 30))
            self.screen.blit(message_surface, message_rect)
        
        # Continue text
        continue_text = self.fonts['tiny'].render("Click anywhere to continue", True, self.colors['gray'])
        continue_rect = continue_text.get_rect(center=(self.width//2, box_y + box_height - 30))
        self.screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()
        
        # Wait for click
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    break
    
    def open_settings(self):
        """Open settings dialog"""
        # This is a simplified settings dialog
        # In a full implementation, you'd create a more complex UI
        self.show_message("SETTINGS", "Settings feature coming soon!\nUse the command-line version for now.")
    
    def save_settings(self):
        """Save settings to file"""
        settings = {
            "work_time": self.work_time,
            "short_break_time": self.short_break_time,
            "long_break_time": self.long_break_time,
            "pomodoros_before_long_break": self.pomodoros_before_long_break
        }
        
        try:
            with open("pomodoro_settings.json", "w") as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists("pomodoro_settings.json"):
                with open("pomodoro_settings.json", "r") as f:
                    settings = json.load(f)
                    self.work_time = settings.get("work_time", 25)
                    self.short_break_time = settings.get("short_break_time", 5)
                    self.long_break_time = settings.get("long_break_time", 15)
                    self.pomodoros_before_long_break = settings.get("pomodoros_before_long_break", 4)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check button clicks
                if self.buttons['start'].collidepoint(mouse_pos):
                    self.start_timer()
                elif self.buttons['reset'].collidepoint(mouse_pos):
                    self.reset_timer()
                elif self.buttons['pause'].collidepoint(mouse_pos):
                    self.start_timer()  # Toggle pause
                elif self.buttons['work'].collidepoint(mouse_pos):
                    self.set_mode("work")
                elif self.buttons['short_break'].collidepoint(mouse_pos):
                    self.set_mode("short_break")
                elif self.buttons['long_break'].collidepoint(mouse_pos):
                    self.set_mode("long_break")
                elif self.buttons['settings'].collidepoint(mouse_pos):
                    self.open_settings()
        
        return True
    
    def run(self):
        """Main application loop"""
        running = True
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Draw everything
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(60)
        
        pygame.quit()

def main():
    """Main function"""
    print("Starting PomoPy with Pygame...")
    timer = PomodoroTimer()
    timer.run()

if __name__ == "__main__":
    main()

