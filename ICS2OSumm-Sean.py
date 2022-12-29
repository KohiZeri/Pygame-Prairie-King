import sys, pygame, pygame.mixer
import random
from pygame.locals import *

pygame.init()

# Displays screen size
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

# Define the User object by extending pygame.sprite.Sprite
# The image you load on the screen is now an attribute of 'User'
class User(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self) # construct the parent component
    self.image = pygame.image.load("facing up.png").convert_alpha()
    self.facing = 0 # 0 is up, 1 is down, 2 is left, and 3 is right
    self.rect = self.image.get_rect()

    # User spawnpoint
    self.rect.topleft = (320,240)
    self.dir_x = 1
    self.dir_y = 1
    self.delta = (0,0)

  # Allows movement of the sprite
  def update(self):
    # Move the sprite based on speed
    self.rect.move_ip(self.delta[0], self.delta[1])
    self.delta = (0,0)
    
  # Stops sprite when reaching edges and corners
  def movement(self, delta):
    self.delta = delta
    if self.rect.topleft[0] - self.delta[0] < 23 and self.facing == 2:
      self.delta = (0,self.delta[1])
    elif self.rect.topleft[0] + self.delta[0] > screen.get_width() - 23 and self.facing == 3:
      self.delta = (0,self.delta[1])
    if self.rect.topleft[1] - self.delta[1] < 23 and self.facing == 0:
      self.delta = (self.delta[0], 0)
    elif self.rect.topleft[1] + self.delta[1] > screen.get_height() - 23 and self.facing == 1:
      self.delta = (self.delta[0], 0)

  # sprite image direction
  # - up
  # - down
  # - left 
  # - right 
  def change_image_up(self):
    self.image = pygame.image.load("facing up.png").convert_alpha()
    self.facing = 0
  def change_image_down(self):
    self.image = pygame.image.load("facing down.png").convert_alpha()
    self.facing = 1
  def change_image_left(self):
    self.image = pygame.image.load("facing left.png").convert_alpha()
    self.facing = 2
  def change_image_right(self):
    self.image = pygame.image.load("facing right.png").convert_alpha()
    self.facing = 3

# Define the Entity object by extending pygame.sprite.Sprite
# The image you load on the screen is now an attribute of 'Entity'
class Entity(pygame.sprite.Sprite):  
  def __init__(self):
    pygame.sprite.Sprite.__init__(self) # construct the parent component
    self.image = pygame.image.load("Entity.png").convert_alpha()
    self.rect = self.image.get_rect() 
    
    # randomly spawns 'Entity' outside at set coordinates
    spawn_choice = random.randint(0,3)
    if spawn_choice == 0:
      init_pos = (23, 240)
      direction = (1, 0)
    elif spawn_choice == 1:
      init_pos = (617, 240)
      direction = (-1,0)
    elif spawn_choice == 2:
      init_pos = (320, 23)
      direction = (0, 1)
    elif spawn_choice == 3:
      init_pos = (320, 457)
      direction = (0, -1)

    self.rect.topleft = init_pos
    self.dir_x = direction[0]
    self.dir_y = direction[1]
    self.speed = 1

  # Follows the User position
  def update(self, player_pos): # dir_x = 1 is right, dir_x = -1 is left, 
    if player_pos[0] > self.rect.topleft[0]:
      self.dir_x = 1
    elif player_pos[0] < self.rect.topleft[0]:
      self.dir_x = -1
    else:
      self.dir_x = 0

    if player_pos[1] > self.rect.topleft[1]:
      self.dir_y = 1
    elif player_pos[1] < self.rect.topleft[1]:
      self.dir_y = -1
    else:
      self.dir_y = 0  

    # Stops Entity from going diagonal
    # (1, 1), (1, -1), (-1, 1), (-1, -1)
    if self.dir_x != 0 and self.dir_y != 0: 
      if random.randint(0,1) == 0:
        self.dir_x = 0
      else:
        self.dir_y = 0
    # Move the sprite based on speed
    self.rect.move_ip(self.speed*self.dir_x, self.speed*self.dir_y)

# Define the Bullet object by extending pygame.sprite.Sprite
# The image you load on the screen is now an attribute of 'Bullet'
class Bullet(pygame.sprite.Sprite):
  def __init__(self, init_pos, direction):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("bullet.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.topleft = init_pos
    self.dir_x = direction[0]
    self.dir_y = direction[1]
    self.speed = 1

  # Removes sprite when reaching the edge
  def update(self):
    if self.rect.left < 20 or self.rect.right >= screen.get_width() - 20:
      self.kill()
    if self.rect.top < 20 or self.rect.bottom >= screen.get_height() - 20:
      self.kill()
    self.rect.move_ip(self.speed*self.dir_x, self.speed*self.dir_y)

# Variables for start background, main background, gameover options backgrounds, tutorial background, and win background
start_bg = pygame.image.load("start screen.png")
game_bg = pygame.image.load("Background.png")
gameover1_bg = pygame.image.load("game over 1.png")
gameover2_bg = pygame.image.load("game over 2.png")
tutorial_bg = pygame.image.load("Tutorial.png")
win_bg = pygame.image.load("Win_Screen.png")

# sets screen size
screen = pygame.display.set_mode((640, 480))

# Create group to hold 'User' and 'Entity' when added
bullet_group = pygame.sprite.Group()
entity_group = pygame.sprite.Group()

# creates 'User'
character = User()

# Creates group to hold 'User'
character_group = pygame.sprite.Group(character)

# Firing sound effect
bounce = pygame.mixer.Sound("GUN_FIRE-GoodSoundForYou-820112263.wav")
bounce.set_volume(0.3)

# Background music 1
pygame.mixer.music.load("72 Journey Of The Prairie King - The Outlaw.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

# Adds a font
my_font = pygame.font.Font("Pacifico.ttf", 20)

# background identification(0 = start, 1 = main, 2 = gameover 1, 3 = gameover 2, 4 = tutorial, 5 = win)
bg_id = 0

# Holds the number of 'Entity'
num_entity = 0

# Every turn spawns a random amount of 'num_entity'
game_turn = 0

# Holds the amount of deleted 'entity_group'
kill_count = 0

# Starts the main loop
keep_going = True

# Limiter on 'kill_count'
win_kill_count = 30

while keep_going:
  
  # Frames per second
  clock.tick(80)

  # Gets events from the queue
  for event in pygame.event.get():
    
    # Variable for holding keys
    keys = pygame.key.get_pressed()
    
    if event.type == QUIT:
      # Stops this loop and main loop
      keep_going = False
      break
    
    # Initializes when pressing any key
    if event.type == KEYDOWN:

      # If on Tutorial background
      # Move to main background
      if bg_id == 4:
        bg_id = 1
      
      # If on win background
      # Move to start background
      elif bg_id == 5:
        bg_id = 0

      # When hitting space
      # - Stop background music 1
      # - Play background music 2
      if event.key == K_SPACE:
        pygame.mixer.music.stop()
        pygame.mixer.music.load("73 Journey Of The Prairie King - Final Boss.mp3")
        pygame.mixer.music.set_volume(0.3) 
        pygame.mixer.music.play(-1)

        # When current Background is start
        # Move to tutorial background
        if bg_id == 0:
          bg_id = 4
      
      # When hitting enter
      elif event.key == K_RETURN:
        
        # If on background gameover 2
        # Quit on gameover 2
        if bg_id == 3:
          keep_going = False
          break

        # If on background gameover 1
        # Clear sprites
        # Reset Character(User)
        elif bg_id == 2:
          bullet_group.empty()         
          entity_group.empty()
          
          character = User()
          character_group = pygame.sprite.Group(character)
          bg_id = 1

      # Pressing key up
      elif event.key == K_UP:
        
        # If on main background
        if bg_id == 1:

          # If character is facing up
          if character.facing == 0: 

            # Add bullet
            # Play sound effect
            bullet = Bullet(character.rect.topleft, (0,-1))
            bullet_group.add(bullet)
            bounce.play()
        
        # If on background 3
        # Switching to background 2
        elif bg_id == 3:
          bg_id = 2
      
      # Pressing key down
      elif event.key == K_DOWN:
        
        # If on main background
        if bg_id == 1:

          # If character is facing down
          if character.facing == 1:

            # Add bullet
            # Play sound effect
            bullet = Bullet(character.rect.topleft, (0,1))
            bullet_group.add(bullet)
            bounce.play()
        # If on background 2
        # Switching to background 3
        elif bg_id == 2:
          bg_id = 3

      # Pressing key left    
      elif event.key == K_LEFT:

        # If on main background
        if bg_id == 1:

          # If character is facing left
          if character.facing == 2:

            # Add bullet
            # Play sound effect
            bullet = Bullet(character.rect.topleft, (-1,0))
            bullet_group.add(bullet)
            bounce.play()

      # Pressing key right
      elif event.key == K_RIGHT:

        # If on main background
        if bg_id == 1:

          # If character is facing right
          if character.facing == 3:

            # Add bullet
            # Play sound effect
            bullet = Bullet(character.rect.topleft, (1,0))
            bullet_group.add(bullet)
            bounce.play()
    
    # Holding keys w, s, a, d
    # - w = move character up and switch to sprite facing up
    # - s = move character down and switch to sprite facing down
    # - a = move character left and switch to sprite facing left
    # - d = move character right and switch to sprite facing right
    elif keys[pygame.K_w]:
      if bg_id == 1:
        character.movement((0,-4))
        character.change_image_up()
    elif keys[pygame.K_s]:
      if bg_id == 1:
        character.movement((0,4))
        character.change_image_down()
    elif keys[pygame.K_a]:
      if bg_id == 1:
        character.movement((-4,0))
        character.change_image_left()
    elif keys[pygame.K_d]:
      if bg_id == 1:
        character.movement((4,0))
        character.change_image_right()

  # Background
  # - bg-id 0 == start background 
  # - bg_id 1 == main background 
  # - bg_id 2 == gameover 1 
  # - bg_id 3 == gameover 2 
  # - bg_id 4 == tutorial 
  # - bg_id 5 == win
  if bg_id == 0: 
    screen.fill((0,0,0))
    screen.blit(start_bg, (0,0))
    pygame.display.update()
    game_turn = 0
  elif bg_id == 1:
    
    # Spawns random amount of 'Entity'
    if game_turn % random.randint(50,100) == 1:
      num_entity = 1
      entity_list = []
      
      # Adds the entity to entity_group
      for entity_id in range(num_entity):
        entity = Entity()
        entity_list.append(entity)
      entity_group.add(entity_list)
    
    # Counts 'Entity' before collision 
    entity_before_total = len(entity_group.sprites())    
    
    # Kill bullet_group and entity_group when they colide
    pygame.sprite.groupcollide(bullet_group, entity_group, True, True)
    
    # Recounts 'Entity' total
    entity_after_total = len(entity_group.sprites())    
    kill_count += (entity_before_total - entity_after_total)
    
    # Display kill count
    label = my_font.render(f"{kill_count}/{win_kill_count}", False, (0,0,0))    
    
    # Kill character_group when colliding with entity_group
    pygame.sprite.groupcollide(character_group, entity_group, True, False)
    
    # when 'User' dies
    # Move to background gameover 1
    if len(character_group.sprites()) == 0:
      bg_id = 2
    
    # Displays character 
    character_group.clear(screen, game_bg)    
    character_group.update()

    # Displays bullet 
    bullet_group.clear(screen, game_bg)    
    bullet_group.update()

    # Displays entity 
    entity_group.clear(screen, game_bg)    
    entity_group.update(character.rect.topleft)

    # Draws main background
    screen.blit(game_bg, (0,0))
    
    # Draws each group over the background
    bullet_group.draw(screen)
    character_group.draw(screen)
    entity_group.draw(screen)
    
    # Displays label
    screen.blit(label, (20, 20))
    
    # Update screen
    pygame.display.flip()
    
    # Counts the rounds
    game_turn += 1

    # After reaching the limit
    # Go over to win background
    if kill_count >= win_kill_count:
      
      # Plays background music 3
      pygame.mixer.music.stop()
      pygame.mixer.music.load("69 - Journey Of The Prairie King - Ending.mp3")
      pygame.mixer.music.set_volume(0.3) 
      pygame.mixer.music.play(-1)
      bg_id = 5
  elif bg_id == 2:
    screen.blit(gameover1_bg, (0,0))
    pygame.display.update()
    
    # Kill count returns to 0
    kill_count = 0
  elif bg_id == 3:  
    screen.blit(gameover2_bg, (0,0))
    pygame.display.update()
  elif bg_id == 4:
    screen.blit(tutorial_bg, (0,0))
    pygame.display.update()
  elif bg_id == 5:
    
    # Resets classes
    screen.blit(win_bg, (0,0))
    pygame.display.update()
    kill_count = 0
    bullet_group.empty()         
    entity_group.empty()
    character_group.empty()
    character = User()
    character_group = pygame.sprite.Group(character)