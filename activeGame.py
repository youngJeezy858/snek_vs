from pygame.locals import *
from pellet import *
from random import randint
import startMenu
from gameScreen import *
from player import *
from playerExplosion import *
import pygame


class ActiveGame(GameScreen):

    def __init__(self, screen, clock, players):
        super(ActiveGame, self).__init__(screen, clock)
        self.playerSprites = []
        self.pelletSprites = pygame.sprite.Group()
        self.tail_leftovers = pygame.sprite.Group()
        self.explosion_sprites = pygame.sprite.Group()
        # Instantiate the pellet
        self.pellet = Pellet('images/pellet.png', (25, 25),
                             (randint(0, screen.get_width()), randint(0, screen.get_height())))
        self.pelletSprites.add(self.pellet)
        # Playing by myself, I want the game to be over when there are 0 alive peeps.
        # Otherwise the game is over when there's only one player left.
        if len(players) == 1:
            self.game_over_num = 0
        else:
            self.game_over_num = 1
        # Instantiate the players
        self.players = players
        for player in players:
            temp_player_group = pygame.sprite.Group()
            temp_player_group.add(player)
            for t in player.tail:
                temp_player_group.add(t)
            self.playerSprites.append(temp_player_group)
        # Everyone is a winner!
        self.winner = []
        self.determine_winner()
        self.active_game = False
        self.active_game_timer = 300
        self.tail_pop_timer = 300
        self.announcement_font = pygame.font.SysFont("monospace", 24)
        self.winner_font = pygame.font.SysFont("monospace", 36)
        self.prompt_for_exit = False

    def next_screen(self):
        return startMenu.StartMenu(self.screen, self.clock)

    def check_event(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE or \
                event.type == JOYBUTTONDOWN and event.button == 7:
            self.needs_switch = True
        for player in self.players:
            player.check_event(event)

    def update(self):
        super(ActiveGame, self).update()
        # Draw and updoot the start timer
        if not self.active_game and self.active_game_timer != 0:
            timer = self.announcement_font.render(str(self.active_game_timer / 60), True, (255, 255, 255))
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

        # Draw and upoot the end game prompt
        if self.prompt_for_exit:
            exit_prompt = self.announcement_font.render("Press ESC or start button to exit", True, (255, 255, 255))
            exit_prompt_rect = exit_prompt.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
            self.screen.blit(exit_prompt, exit_prompt_rect)
            if len(self.winner) == 0:
                winner_display = self.winner_font.render("DRAW", True, (255, 255, 255))
            else:
                winner_display = self.winner_font.render\
                    (self.winner[0].color + " WINS!", True, self.winner[0].font_color)
            winner_display_rect = winner_display.get_rect\
                (center=(self.screen.get_width() / 2, self.screen.get_height() / 3))
            self.screen.blit(winner_display, winner_display_rect)

        # Updoot any actions occurring with the players
        for player in self.players:
            # Draw yo stats foo'
            stats_x = (self.screen.get_width() / (len(self.players) + 1)) * (player.controller_id + 1)
            stats_y = self.screen.get_height() - 20
            self.screen.blit(player.stats, (stats_x, stats_y))

            # Skip dis if you dead
            # Skip dis if you invulnerable dawg
            if player.state == Player.DEAD or player.invulnerable:
                continue

            # Get some noms
            if pygame.sprite.collide_circle(player, self.pellet):
                tail = player.add_tail()
                self.playerSprites[player.controller_id].add(tail)
                self.pellet.reset_position(self.screen.get_width(), self.screen.get_height())

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
                for i in range(0, 5):
                    self.explosion_sprites.add(PlayerExplosion(p, self.screen.get_height()))
                break
