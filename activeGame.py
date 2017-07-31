from pygame.locals import *
from pellet import *
from random import randint
import startMenu
from gameScreen import *
from player import *
import pygame


class ActiveGame(GameScreen):

    # Player color list
    player_colors = ['blue', 'red', 'red', 'red']

    def __init__(self, screen, players=1):
        super(ActiveGame, self).__init__(screen)
        self.playerSprites = []
        self.pelletSprites = pygame.sprite.Group()
        self.players = []
        # Instantiate the pellet
        self.pellet = Pellet('images/pellet.png', (25, 25),
                             (randint(0, screen.get_width()), randint(0, screen.get_height())))
        self.pelletSprites.add(self.pellet)
        # Playing by myself, I want the game to be over when there are 0 alive peeps.
        # Otherwise the game is over when there's only one player left.
        if players == 1:
            self.game_over_num = 0
        else:
            self.game_over_num = 1
        # Instantiate the players
        for i in range(players):
            # temp_player = Player(self.player_colors[i], (25, 25), (100, 100 * (i+1)), i, 3)
            temp_player = Player(self.player_colors[i], (25, 25), (100, 100 * (i+1)), -1, 3)
            temp_player_group = pygame.sprite.Group()
            temp_player_group.add(temp_player)
            self.players.append(temp_player)
            for t in temp_player.tail:
                temp_player_group.add(t)
            self.playerSprites.append(temp_player_group)
        # Everyone is a winner!
        self.winner = []
        self.determine_winner()

    def next_screen(self):
        return startMenu.StartMenu(self.screen, self.players, self.winner)

    def check_event(self, event):
        # Start menu listeners
        if event.type == KEYDOWN and event.key == K_ESCAPE or \
                event.type == JOYBUTTONDOWN and event.button == 7:
            self.needs_switch = True
        # Active game listeners
        # if self.is_controller_active(event):
        for player in self.players:
            player.check_event(event)

    def update(self):
        self.screen.fill((0, 0, 0))
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
                self.pellet.reset_position(self.screen.get_width(), self.screen.get_height())

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

        self.determine_winner()

        # Finish updating + drawing the sprites
        for player in self.playerSprites:
            player.update()
            player.draw(self.screen)
        self.pelletSprites.update()
        self.pelletSprites.draw(self.screen)

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
        if alive_count == self.game_over_num:
            self.needs_switch = True

    def kill_player(self, player):
        player.state = Player.DEAD
        for i in self.playerSprites:
            if i.sprites()[0].controller_id == player.controller_id:
                self.playerSprites.remove(i)
                break
