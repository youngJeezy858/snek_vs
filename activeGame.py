from pygame.locals import *
from pellet import *
from random import randint
import startMenu
import pygame
import copy
from gameScreen import *
from player import *
from playerExplosion import *
from logger import *
from constants.debugging_flags import *
from buttons.buttonGrid import *
from buttons.playAgainButton import *
from buttons.mainMenuButton import *
from buttons.quitGameButton import *
from computerPlayer import *


class ActiveGame(GameScreen):

    # Win conditions
    WIN_CONDITION_SOLO = 0
    WIN_CONDITION_FFA = 1
    WIN_CONDITION_TEAM = 2
    # Game state conditions
    GAME_STATE_ACTIVE = 100
    GAME_STATE_STARTING = 101
    GAME_STATE_PAUSED = 102
    GAME_STATE_FINISHED = 103

    def __init__(self, screen, clock, players, win_condition):
        super(ActiveGame, self).__init__(screen, clock)
        self.logger = Logger("Active Game", DEBUG_ACTIVE_GAME)
        # Bump dat shit
        pygame.mixer.init()
        pygame.mixer.music.load('music/11-dreamland.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        self.player_sprites = pygame.sprite.Group()
        self.pellet_sprites = pygame.sprite.Group()
        self.tail_leftovers = pygame.sprite.Group()
        self.explosion_sprites = pygame.sprite.Group()
        # Instantiate the pellet
        self.pellet = Pellet('images/pellet.png', (25, 25), self.screen.get_width(), self.screen.get_height())
        self.pellet_sprites.add(self.pellet)
        if len(players) == 1:
            self.win_condition = self.WIN_CONDITION_SOLO
        else:
            self.win_condition = win_condition
        # Instantiate the players
        self.og_players = self.copy_players(players)
        for player in players:
            self.player_sprites.add(player)
        # Everyone is a winner!
        self.winner = []
        self.determine_winner()
        self.game_state = self.GAME_STATE_STARTING
        self.timer_constant = 300
        self.active_game_timer = self.timer_constant
        self.tail_pop_timer = self.timer_constant
        self.announcement_font = pygame.font.SysFont("monospace", 24)
        self.prompt_font = pygame.font.SysFont("monospace", 36)
        self.fader_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        pygame.draw.rect(
            self.fader_surface,
            (0, 0, 0),
            (0, 0, self.screen.get_width(), self.screen.get_height())
        )
        self.fader_surface.set_alpha(0)
        self.endgame_button_grid = ButtonGrid(1, 3)
        self.endgame_button_sprites = pygame.sprite.Group()
        self.button_play_again = PlayAgainButton()
        self.button_main_menu = MainMenuButton()
        button_quit = QuitGameButton()
        self.endgame_button_grid.add_button(button_quit, 0, 0)
        self.endgame_button_grid.add_button(self.button_main_menu, 0, 1)
        self.endgame_button_grid.add_button(self.button_play_again, 0, 2)
        self.endgame_button_sprites.add(button_quit)
        self.endgame_button_sprites.add(self.button_main_menu)
        self.endgame_button_sprites.add(self.button_play_again)
        self.fader_surface_rect = self.fader_surface.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2)
        )
        self.paused_display = self.prompt_font.render("PAUSED", True, (255, 255, 255))
        self.paused_display_rect = self.paused_display.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 3)
        )

    def copy_players(self, players):
        players_copy = []
        for player in players:
            # Pygame doesn't allow deep copies, what a piece of shit
            if player.controller_id == player.COMPUTER:
                players_copy.append(ComputerPlayer(
                    player.player_id,
                    player.color,
                    player.shade_id,
                    player.dimensions,
                    player.position,
                    player.movement_speed
                ))
            else:
                players_copy.append(Player(
                    player.player_id,
                    player.color,
                    player.shade_id,
                    player.dimensions,
                    player.position,
                    player.controller_id,
                    player.movement_speed
                ))
        return players_copy

    def next_screen(self):
        pygame.mixer.music.stop()
        if self.button_main_menu.state == Button.ACTIVE:
            return startMenu.StartMenu(self.screen, self.clock)
        elif self.button_play_again.state == Button.ACTIVE:
            return ActiveGame(self.screen, self.clock, self.og_players, self.win_condition)

    def check_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE or \
                event.type == JOYBUTTONDOWN and event.button == 7:
            if self.game_state == self.GAME_STATE_ACTIVE:
                self.fader_surface.set_alpha(200)
                self.game_state = self.GAME_STATE_PAUSED
                self.active_game_timer = self.timer_constant
            elif self.game_state == self.GAME_STATE_PAUSED:
                self.fader_surface.set_alpha(0)
                self.game_state = self.GAME_STATE_STARTING
        for player in self.player_sprites:
            player.check_event(event)
        if self.game_state == self.GAME_STATE_FINISHED:
            self.endgame_button_grid.check_event(event)

    def update(self):
        super(ActiveGame, self).update()
        # Updoot any actions occurring with the players
        for player in self.player_sprites:
            # Draw yo stats foo'
            self.update_player_stats(player)
            # Skip dis if you dead
            if player.state == Player.DEAD:
                continue
            # Process the computer player
            if player.controller_id == player.COMPUTER:
                player.determine_movement(self.pellet, self.player_sprites, self.tail_leftovers)
            # Get some noms
            if pygame.sprite.collide_circle(player, self.pellet):
                player.add_tail()
                self.reset_pellet_position()
            # Skip dis if you invulnerable dawg
            if player.invulnerable:
                continue
            # DEATH CONDITIONS!!!!!
            if self.check_boundary_death(player) or \
                    self.check_suicide(player) or \
                    self.check_homicide(player) or \
                    self.check_landmine_death(player):
                self.determine_winner()
                continue
        # Clean up the explosion sprites
        for sprite in self.explosion_sprites:
            if sprite.state == PlayerExplosion.CLEAN_UP:
                self.explosion_sprites.remove(sprite)
        # Update sprites
        if self.game_state == self.GAME_STATE_ACTIVE:
            self.pellet_sprites.update()
            self.update_tail_pop_timer()
            self.player_sprites.update()
            for player in self.player_sprites:
                player.update_tail()
        self.explosion_sprites.update()
        # Draw Sprites
        self.player_sprites.draw(self.screen)
        for player in self.player_sprites:
            player.draw_tail(self.screen)
        self.pellet_sprites.draw(self.screen)
        self.tail_leftovers.draw(self.screen)
        self.explosion_sprites.draw(self.screen)
        # Draw and upoot prompts depending on the inactive game, otherwise updoot the tail pop timer
        if self.game_state == self.GAME_STATE_STARTING:
            self.update_start_timer()
        elif self.game_state == self.GAME_STATE_FINISHED:
            self.draw_end_game_prompt()
        elif self.game_state == self.GAME_STATE_PAUSED:
            self.draw_paused_prompt()

    def draw_paused_prompt(self):
        self.screen.blit(self.fader_surface, self.fader_surface_rect)
        self.screen.blit(self.paused_display, self.paused_display_rect)

    def draw_end_game_prompt(self):
        curr_alpha = self.fader_surface.get_alpha()
        if curr_alpha != 200:
            self.fader_surface.set_alpha(curr_alpha + 2)
            endgame_surface_rect = self.fader_surface.get_rect(
                center=(self.screen.get_width() / 2, self.screen.get_height() / 2)
            )
            self.screen.blit(self.fader_surface, endgame_surface_rect)
        else:
            endgame_surface_rect = self.fader_surface.get_rect(
                center=(self.screen.get_width() / 2, self.screen.get_height() / 2)
            )
            self.screen.blit(self.fader_surface, endgame_surface_rect)
            if len(self.winner) == 0:
                winner_display = self.prompt_font.render("DRAW", True, (255, 255, 255))
            else:
                winner_display = self.prompt_font.render(
                    self.winner[0].color + " WINS!", True, self.winner[0].font_color
                )
            winner_display_rect = winner_display.get_rect(
                center=(self.screen.get_width() / 2, self.screen.get_height() / 3)
            )
            self.screen.blit(winner_display, winner_display_rect)
            self.endgame_button_sprites.update()
            self.endgame_button_sprites.draw(self.screen)
            if self.button_main_menu.state == Button.ACTIVE or self.button_play_again.state == Button.ACTIVE:
                self.needs_switch = True

    def check_landmine_death(self, player):
        for tail in self.tail_leftovers:
            if pygame.sprite.collide_circle(player, tail):
                self.logger.debug(
                    "check_landmine_death",
                    "Player %s ate a leftover carcass!" % player.player_id
                )
                self.kill_player(player)
                return True
        return False

    def check_homicide(self, player):
        for other_player in self.player_sprites:
            if other_player.player_id == player.player_id:
                continue
            # Check if you tried eating another player (tsk tsk)
            else:
                if pygame.sprite.collide_circle(player, other_player):
                    self.logger.debug(
                        "check_homicide",
                        "Player %s tried eating dat boi Player %s's head!" %
                        (player.player_id, other_player.player_id)
                    )
                    self.kill_player(player)
                    self.kill_player(other_player)
                    return True
                for tail in other_player.tail:
                    if pygame.sprite.collide_circle(player, tail):
                        self.logger.debug(
                            "check_homicide",
                            "Player %s tried eating dat boi Player %s's tail!" %
                            (player.player_id, other_player.player_id)
                        )
                        self.kill_player(player)
                        return True
        return False

    def check_suicide(self, player):
        for tail in player.tail[1:]:
            if pygame.sprite.collide_circle(player, tail):
                self.logger.debug(
                    "check_suicide",
                    "Player %s ate demselves!" % player.player_id
                )
                self.kill_player(player)
                return True
        return False

    def check_boundary_death(self, player):
        if player.position[0] < player.dimensions[0] / 2 or \
                player.position[0] > int(self.screen.get_width() - player.dimensions[0] / 2) or \
                player.position[1] < player.dimensions[1]/2 or \
                player.position[1] > int(self.screen.get_height() - player.dimensions[1]/2):
            self.logger.debug(
                "check_boundary_death",
                "Player %s hit a boundary dawg!" % player.player_id
            )
            self.kill_player(player)
            return True
        return False

    def update_player_stats(self, player):
        stats_x = (self.screen.get_width() / (len(self.player_sprites) + 1)) * (player.player_id + 1)
        stats_y = self.screen.get_height() - 20
        self.screen.blit(player.stats, (stats_x, stats_y))

    def update_tail_pop_timer(self):
        self.tail_pop_timer -= 1
        if self.tail_pop_timer == 0:
            self.tail_pop_timer = 300
            for player in self.player_sprites:
                temp_tail = player.pop_tail()
                if temp_tail is not None:
                    temp_tail.controller_id = -9999
                    self.tail_leftovers.add(temp_tail)
                else:
                    self.logger.debug(
                        "update_tail_pop_timer",
                        "Player %s has no tail!" % player.player_id
                    )
                    self.kill_player(player)
                    continue

    def update_start_timer(self):
        time = str(int(math.ceil(float(self.active_game_timer) / 60.0)))
        timer = self.announcement_font.render(time, True, (255, 255, 255))
        self.screen.blit(timer, (self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.active_game_timer -= 1
        if self.active_game_timer == 0:
            self.game_state = self.GAME_STATE_ACTIVE

    def resize_screen(self, screen):
        super(ActiveGame, self).resize_screen(screen)
        for sprite in self.sprites:
            dimensions = self.calculate_dimensions(sprite.og_dimensions)
            position = self.calculate_position(sprite.og_position)
            sprite.resize(dimensions, position)

    def determine_winner(self):
        if len(self.player_sprites) <= self.win_condition:
            self.winner = self.player_sprites.sprites()
            self.game_state = self.GAME_STATE_FINISHED

    def kill_player(self, player):
        player.state = Player.DEAD
        for p in self.player_sprites:
            if p.player_id == player.player_id:
                while p.tail:
                    temp_tail = player.pop_tail()
                    if temp_tail is not None:
                        temp_tail.controller_id = -9999
                        self.tail_leftovers.add(temp_tail)
                    else:
                        break
                self.player_sprites.remove(player)
                for i in range(0, 10):
                    self.explosion_sprites.add(PlayerExplosion(p, self.screen.get_height()))
                break

    def reset_pellet_position(self, stopper=0):
        if stopper == 30:
            return
        stopper += 1
        self.pellet.reset_position(self.screen.get_width(), self.screen.get_height())
        for player in self.player_sprites:
            if pygame.sprite.collide_circle(self.pellet, player):
                self.logger.debug(
                    "reset_pellet_position",
                    "pellet: %s, player: %s" % (self.pellet.position, player.position)
                )
                return self.reset_pellet_position(stopper)
            for tail in player.tail:
                if pygame.sprite.collide_circle(self.pellet, tail):
                    return self.reset_pellet_position(stopper)
        for leftover in self.tail_leftovers:
            if pygame.sprite.collide_circle(self.pellet, leftover):
                return self.reset_pellet_position(stopper)
