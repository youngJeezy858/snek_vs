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


class ActiveGame(GameScreen):

    def __init__(self, screen, clock, players):
        super(ActiveGame, self).__init__(screen, clock)
        self.logger = Logger("Active Game", DEBUG_ACTIVE_GAME)
        # Bump dat shit
        pygame.mixer.init()
        pygame.mixer.music.load('music/11-dreamland.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        self.playerSprites = []
        self.pelletSprites = pygame.sprite.Group()
        self.tail_leftovers = pygame.sprite.Group()
        self.explosion_sprites = pygame.sprite.Group()
        # Instantiate the pellet
        self.pellet = Pellet('images/pellet.png', (25, 25), self.screen.get_width(), self.screen.get_height())
        self.pelletSprites.add(self.pellet)
        # Playing by myself, I want the game to be over when there are 0 alive peeps.
        # Otherwise the game is over when there's only one player left.
        if len(players) == 1:
            self.game_over_num = 0
        else:
            self.game_over_num = 1
        # Instantiate the players
        self.players = players
        self.og_players = []
        for player in players:
            temp_player_group = pygame.sprite.Group()
            temp_player_group.add(player)
            for t in player.tail:
                temp_player_group.add(t)
            self.playerSprites.append(temp_player_group)
            # Pygame doesn't allow deep copy's, what a piece of shit
            self.og_players.append(Player(
                player.color,
                player.shade_id,
                player.dimensions,
                player.position,
                player.controller_id,
                player.movement_speed
            ))
        # Everyone is a winner!
        self.winner = []
        self.determine_winner()
        self.active_game = False
        self.active_game_timer = 300
        self.tail_pop_timer = 300
        self.announcement_font = pygame.font.SysFont("monospace", 24)
        self.winner_font = pygame.font.SysFont("monospace", 36)
        self.endgame_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        pygame.draw.rect(self.endgame_surface, (0, 0, 0), (0, 0, self.screen.get_width(), self.screen.get_height()))
        self.endgame_surface.set_alpha(0)
        self.prompt_for_exit = False
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

    def next_screen(self):
        pygame.mixer.music.stop()
        if self.button_main_menu.state == Button.ACTIVE:
            return startMenu.StartMenu(self.screen, self.clock)
        elif self.button_play_again.state == Button.ACTIVE:
            return ActiveGame(self.screen, self.clock, self.og_players)

    def check_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE or \
                event.type == JOYBUTTONDOWN and event.button == 7:
            self.needs_switch = True
        for player in self.players:
            player.check_event(event)
        if self.prompt_for_exit:
            self.endgame_button_grid.check_event(event)

    def update(self):
        super(ActiveGame, self).update()
        # Draw and updoot the start timer
        if not self.active_game and self.active_game_timer != 0:
            time = str(int(math.ceil(float(self.active_game_timer) / 60.0)))
            timer = self.announcement_font.render(time, True, (255, 255, 255))
            self.screen.blit(timer, (self.screen.get_width() / 2, self.screen.get_height() / 2))
            self.active_game_timer -= 1
            if self.active_game_timer == 0:
                self.active_game = True
        # Updoot the tail pop
        else:
            self.tail_pop_timer -= 1
            if self.tail_pop_timer == 0:
                self.tail_pop_timer = 300
                for player in self.players:
                    temp_tail = player.pop_tail()
                    if temp_tail is not None:
                        temp_tail.controller_id = -9999
                        self.tail_leftovers.add(temp_tail)
                    else:
                        self.kill_player(player)
                        continue

        # Updoot any actions occurring with the players
        for player in self.players:
            # Draw yo stats foo'
            stats_x = (self.screen.get_width() / (len(self.players) + 1)) * (player.controller_id + 1)
            stats_y = self.screen.get_height() - 20
            self.screen.blit(player.stats, (stats_x, stats_y))

            # Skip dis if you dead
            if player.state == Player.DEAD:
                continue

            # Get some noms
            if pygame.sprite.collide_circle(player, self.pellet):
                tail = player.add_tail()
                self.playerSprites[player.controller_id].add(tail)
                self.reset_pellet_position()

            # Skip dis if you invulnerable dawg
            if player.invulnerable:
                continue

            # Check if you dead sucka
            # Check if you hit a boundary
            if player.position[0] < player.dimensions[0]/2 or \
                    player.position[0] > int(self.screen.get_width() - player.dimensions[0]/2):
                print "Player %s hit off that x axis dawg!" % player.controller_id
                self.kill_player(player)
                continue
            if player.position[1] < player.dimensions[1]/2 or \
                    player.position[1] > int(self.screen.get_height() - player.dimensions[1]/2):
                print "Player %s hit off that y axis dawg!" % player.controller_id
                self.kill_player(player)
                continue
            for other_player in self.players:
                # Check if you ate yo'self dumbass
                if other_player.controller_id == player.controller_id:
                    # I don't wanna check my own head and my first tail segment
                    for tail in other_player.tail[1:]:
                        if pygame.sprite.collide_circle(player, tail):
                            print "Player %s ate demselves!" % player.controller_id
                            self.kill_player(player)
                            continue
                # Check if you tried eating another player (tsk tsk)
                else:
                    if pygame.sprite.collide_circle(player, other_player):
                        print "Player %s tried eating dat boi Player %s's head!" %\
                              (player.controller_id, other_player.controller_id)
                        self.kill_player(player)
                        continue
                    for tail in other_player.tail:
                        if pygame.sprite.collide_circle(player, tail):
                            print "Player %s tried eating dat boi Player %s's tail!" % \
                                  (player.controller_id, other_player.controller_id)
                            self.kill_player(player)
                            continue
            for tail in self.tail_leftovers.sprites():
                if pygame.sprite.collide_circle(player, tail):
                    print "Player %s ate a leftover carcass!" % player.controller_id
                    self.kill_player(player)
                    continue

        # Clean up the explosion sprites
        for sprite in self.explosion_sprites:
            if sprite.state == PlayerExplosion.CLEAN_UP:
                self.explosion_sprites.remove(sprite)

        self.determine_winner()

        # Finish updating + drawing the sprites
        for player in self.playerSprites:
            if self.active_game and self.active_game_timer == 0:
                player.update()
            player.draw(self.screen)
        if self.active_game and self.active_game_timer == 0:
            self.pelletSprites.update()
        self.pelletSprites.draw(self.screen)
        self.tail_leftovers.draw(self.screen)
        self.explosion_sprites.update()
        self.explosion_sprites.draw(self.screen)

        # Draw and upoot the end game prompt
        if self.prompt_for_exit:
            curr_alpha = self.endgame_surface.get_alpha()
            if curr_alpha != 200:
                self.endgame_surface.set_alpha(curr_alpha + 2)
                endgame_surface_rect = self.endgame_surface.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2))
                self.screen.blit(self.endgame_surface, endgame_surface_rect)
            else:
                endgame_surface_rect = self.endgame_surface.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()/2))
                self.screen.blit(self.endgame_surface, endgame_surface_rect)
                if len(self.winner) == 0:
                    winner_display = self.winner_font.render("DRAW", True, (255, 255, 255))
                else:
                    winner_display = self.winner_font.render\
                        (self.winner[0].color + " WINS!", True, self.winner[0].font_color)
                winner_display_rect = winner_display.get_rect\
                    (center=(self.screen.get_width() / 2, self.screen.get_height() / 3))
                self.screen.blit(winner_display, winner_display_rect)
                self.endgame_button_sprites.update()
                self.endgame_button_sprites.draw(self.screen)
                if self.button_main_menu.state == Button.ACTIVE or self.button_play_again.state == Button.ACTIVE:
                    self.needs_switch = True

    def resize_screen(self, screen):
        super(ActiveGame, self).resize_screen(screen)
        for sprite in self.sprites:
            dimensions = self.calculate_dimensions(sprite.og_dimensions)
            position = self.calculate_position(sprite.og_position)
            sprite.resize(dimensions, position)

    def determine_winner(self):
        alive_count = 0
        for player in self.players:
            if player.state == Player.DEAD:
                if player in self.winner:
                    self.winner.remove(player)
                continue
            elif player in self.winner:
                alive_count += 1
                continue
            elif len(self.winner) == 0:
                self.winner.append(player)
            elif len(player.tail) == len(self.winner[0].tail):
                self.winner.append(player)
            elif len(player.tail) > len(self.winner[0].tail):
                self.winner = [player]
            alive_count += 1
        if alive_count <= self.game_over_num:
            self.prompt_for_exit = True

    def kill_player(self, player):
        player.state = Player.DEAD
        for p in self.players:
            if p.controller_id == player.controller_id:
                while p.tail:
                    temp_tail = player.pop_tail()
                    if temp_tail is not None:
                        temp_tail.controller_id = -9999
                        self.tail_leftovers.add(temp_tail)
                    else:
                        break
                self.players.remove(p)
                del self.playerSprites[p.controller_id]
                for i in range(0, 10):
                    self.explosion_sprites.add(PlayerExplosion(p, self.screen.get_height()))
                break

    def reset_pellet_position(self, stopper=0):
        if stopper == 30:
            return
        stopper += 1
        self.pellet.reset_position(self.screen.get_width(), self.screen.get_height())
        for player in self.players:
            if pygame.sprite.collide_circle(self.pellet, player):
                self.logger.debug("reset_pellet_position", "pellet: %s, player: %s" %
                                  (self.pellet.position, player.position))
                return self.reset_pellet_position(stopper)
            for tail in player.tail[1:]:
                if pygame.sprite.collide_circle(self.pellet, tail):
                    return self.reset_pellet_position(stopper)
        for leftover in self.tail_leftovers:
            if pygame.sprite.collide_circle(self.pellet, leftover):
                return self.reset_pellet_position(stopper)
