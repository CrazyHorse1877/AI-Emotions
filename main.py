import pygame
import sys
import random
from settings import *
from agent import Agent
from prey import Prey
from predator import Predator

pygame.init()

# Larger screen for extended UI
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Emotions Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 48)

message_log = ""
message_timer = 0

# Draw smooth, rounded progress bar
def draw_progress_bar(screen, x, y, width, height, value, max_value, label, colour):
    pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height), border_radius=8)  # background
    fill_width = int(width * (value / max_value))
    pygame.draw.rect(screen, colour, (x, y, fill_width, height), border_radius=8)
    label_surface = font.render(f"{label}: {int(value)}", True, (255, 255, 255))
    screen.blit(label_surface, (x, y - 22))

# Top-centre emotion panel
def draw_emotion_panel(screen, emotion, colour):
    panel_width, panel_height = 300, 60
    panel_x = (SCREEN_WIDTH - panel_width) // 2
    panel_y = 20
    panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel_surface.fill((0, 0, 0, 160))  # translucent black
    screen.blit(panel_surface, (panel_x, panel_y))

    text_surface = large_font.render(emotion, True, colour)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, panel_y + panel_height // 2))
    screen.blit(text_surface, text_rect)

# Bottom message log
def draw_message_log(screen, message):
    if message:
        text_surface = font.render(message, True, (200, 200, 200))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(text_surface, text_rect)


def main():
    global message_log, message_timer
    debug_mode = True
    agent = Agent()
    prey_list = [Prey() for _ in range(20)]
    predator_list = [Predator() for _ in range(3)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    agent.save_action_log("agent_log.json")
                elif event.key == pygame.K_d:
                    debug_mode = not debug_mode

        screen.fill(BG_COLOUR)

        # Update and draw prey
        for prey in prey_list[:]:
            prey.update(prey_list)
            prey.draw(screen)

        # Update and draw predators
        for predator in predator_list:
            predator.update(prey_list, predator_list)
            predator.draw(screen)

        # Predator eats prey on contact
        for predator in predator_list:
            for prey in prey_list[:]:
                if pygame.Vector2(predator.x, predator.y).distance_to(prey.get_position()) < predator.radius + prey.radius:
                    prey_list.remove(prey)

        # Track emotion change for message log
        prev_emotion = agent.emotion
        agent.update(prey_list, predator_list)
        if agent.emotion != prev_emotion:
            message_log = f"The agent feels {agent.emotion.lower()}..."
            message_timer = 180  # 3 seconds

        # Occasionally spawn new prey
        if random.random() < 0.01 and len(prey_list) < 50:
            prey_list.append(Prey())

        agent.draw(screen, font)

        # Draw emotion panel
        emotion_colour = EMOTION_COLOURS.get(agent.emotion, (255, 255, 255))
        draw_emotion_panel(screen, agent.emotion, emotion_colour)

        # Progress bars (top-left)
        bar_x = 20
        bar_y_start = 100
        bar_width = 200
        bar_height = 20
        bar_spacing = 40

        draw_progress_bar(screen, bar_x, bar_y_start + 0 * bar_spacing, bar_width, bar_height, agent.health, 100, "Health", (0, 255, 0))
        draw_progress_bar(screen, bar_x, bar_y_start + 1 * bar_spacing, bar_width, bar_height, agent.hunger, 100, "Hunger", (255, 165, 0))
        draw_progress_bar(screen, bar_x, bar_y_start + 2 * bar_spacing, bar_width, bar_height, agent.energy, 100, "Energy", (0, 150, 255))
        draw_progress_bar(screen, bar_x, bar_y_start + 3 * bar_spacing, bar_width, bar_height, agent.stimulation, 100, "Stimulation", (255, 255, 0))

        # Thought bubble for active emotions
        if agent.emotion in ["Curious", "Fearful"]:
            pygame.draw.circle(screen, (255, 255, 255), (int(agent.x), int(agent.y - 30)), 5)
            pygame.draw.circle(screen, (255, 255, 255), (int(agent.x), int(agent.y - 40)), 3)

        # Show message log
        if message_timer > 0:
            draw_message_log(screen, message_log)
            message_timer -= 1

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
