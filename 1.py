import pygame, random

#from pygame.sprite import _Group
ANCHO = 1200
ALTO = 550
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN =(0,255,0)
pygame.init()
pygame.mixer.init()
ventana = pygame.display.set_mode((ANCHO,ALTO))
pygame.display.set_caption("Goku vs Naruto")
icono = pygame.image.load("Desktop\proyecto\icono.png")
pygame.display.set_icon(icono)
fps = pygame.time.Clock()
fondoinicio = pygame.image.load("Desktop\proyecto\inicio.png")

#sirve para escribir texto mas que nada para el final del juego el game over
def draw_text(surface, text, size, x,y):
    font= pygame.font.SysFont("impact",size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

#para la vida del personaje 
def draw_shield_bar (pantalla, x, y,percentaje):
    BAR_LENGHT = 100
    BAR_HEIGHT = 20
    fill = (percentaje /100)*BAR_LENGHT
    border = pygame.Rect(x, y,BAR_LENGHT,BAR_HEIGHT)
    fill = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(pantalla,GREEN,fill)
    pygame.draw.rect(pantalla,WHITE,border,2)

#aca va todo del personaje escudo, sprites, colisiones
class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Desktop\proyecto\disparo.png")
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = 50
        self.rect.bottom = 450
        self.speed_x = 0
        self.shield = 100

#movimientos y velocidad
    def update (self):
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate [pygame.K_LEFT]:
            self.speed_x = -5
        if keystate [pygame.K_RIGHT]:
            self.speed_x = 5
        if keystate [pygame.K_UP]:
            self.speed_y = -5
        if keystate [pygame.K_DOWN]:
            self.speed_y = 5
#movimientos en la pantalla
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > ANCHO -100:
            self.rect.right = ANCHO - 100
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > 540:
            self.rect.bottom = 540
        if self.rect.y <  220:
            self.rect.y = 220

#EL DISPARO
    def shoot(self):
        bala = Bala(self.rect.centerx, self.rect.centery -18)
        all_sprites.add(bala)
        balas.add(bala)
        laser_sound.play()

#clase del enemigo
class Enemigos(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.x = random.randint(1000,1050)
        self.rect.y = random.randrange(220,450)

        self.speedx = random.randrange(3, 6)
    def update(self):

        self.rect.x -= self.speedx
        if self.rect.left < 0:
            self.rect.x = random.randint(1050,1150)
            self.rect.y = random.randrange(220, 450)
            self.speedx = random.randrange (3,6)

#DEFINIR LOS ELEMENTOS DE BALA EN UNA CLASE
class Bala(pygame.sprite.Sprite):
    def __init__(self,x, y):
        super().__init__()
        self.image = pygame.image.load("Desktop\proyecto\laser2.png")
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.x = x
        self.rect.centery = y
        self.speedx = 10
    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > ANCHO:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center):
        super().__init__()
        self.image = explosion_anima[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 #velocidad de la explosion
    def update (self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1  #enn caso de ser cierto poner 1 frame mas para la explosion
            if self.frame == len(explosion_anima):
                self.kill()
            else:
                center= self.rect.center
                self.image = explosion_anima[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#para que inicie el juego y cierre
def titles():
    ventana.blit(fondoinicio, [0,0])
    draw_text(ventana, "presiona ESPACIO PARA JUGAR", 40,ANCHO//2,ALTO*3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        fps.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

#aca va el texto utilzando en el juego, 
def show_go_screen():
    ventana.blit(fondo,[0,0])
    draw_text(ventana,"Te moristee",65, ANCHO//2,ALTO//4)
    draw_text(ventana, f"puntos totales:{score}",50,ANCHO//2,ALTO//2)
    draw_text(ventana, "presiona ESPACIO PARA REVIVIR", 40,ANCHO//2,ALTO*3/4)
    pygame.display.flip()
    waiting = True
# este while sirve para poder jugar de nuevo ya qe l while recorre     
    while waiting:
        fps.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

#la variable list que tiene adentro las imagenes de los enemigos
meteor_images= []
meteor_list = ["Desktop\proyecto\zomder1.png",
               "Desktop\proyecto\zomder2.png",
               "Desktop\proyecto\zomder3.png",
               "Desktop\proyecto\zomder4.png"
               ,"Desktop\proyecto\zomder5.png",
               "Desktop\proyecto\zomder6.png",
               "Desktop\proyecto\zomder7.png",
               "Desktop\proyecto\zomder8.png",
               "Desktop\proyecto\zomder9.png",
               "Desktop\proyecto\zomder10.png",
               "Desktop\proyecto\zomder11.png",
               "Desktop\proyecto\zomder12.png",
               "Desktop\proyecto\zomder13.png",
               "Desktop\proyecto\zomder14.png",
               "Desktop\proyecto\zomder15.png",
               "Desktop\proyecto\zomder16.png"]
#meteor_list.set_colorkey([0, 255, 255])


#para el fondo del juego
for img in meteor_list:
    meteor_images.append(pygame.image.load(img))
    

#tiene la imagen de las explosiones
#explosiones meteoritos
explosion_anima = []
for i in range(9):
    file = "Desktop\proyecto\Explosion0.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(WHITE)
    img_scale = pygame.transform.scale(img, (70,70))
    explosion_anima.append(img_scale)
x = 0
fondo = pygame.image.load ("Desktop\proyecto\calle.png").convert()


#cargar sonidos
laser_sound = pygame.mixer.Sound("Desktop\proyecto\pistola.wav")
risa = pygame.mixer.Sound("Desktop\proyecto\jaja.ogg")
gritoplayer = pygame.mixer.Sound("Desktop\proyecto\ohnoo.ogg")
explosion_sound = pygame.mixer.Sound("Desktop\proyecto\grito-de-zombie-sonido.ogg")
pygame.mixer.music.load("Desktop\proyecto\musicazombie.wav")#musica de fondo
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(loops=1) #cuanto se repite la musica

#variables especificadas
all_sprites = pygame.sprite.Group()
enemigos_list = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
balas = pygame.sprite.Group()


for i in range (8):
    enemigos = Enemigos()
    all_sprites.add(enemigos)
    # poniendo .add añade a la lista lo que se le pida
    enemigos_list.add(enemigos)
score = 0

#game over
#variables booleanas que se van a utilizar para iniciar el juego y empieze en el inicio
game_over = True

running = True
titles ()

#while principal del juego
while running:
    if game_over:
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemigos_list = pygame.sprite.Group()
        player = Player() #iguala la clase "Player" para que sea variable
        all_sprites.add(player) #añade la variable a la lista ahora si
        balas = pygame.sprite.Group()
        for i in range (8):
            enemigos = Enemigos()
            all_sprites.add(enemigos)
            enemigos_list.add(enemigos)
        score = 0
    
    fps.tick(60)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#si el juego tiene el evento cerrar juego entonces running cera false
#de esta manera se cierra el juego
        
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        #para que al apretar espacio el player dispare
    
    
    #colisiones de objetos: 
    #"Videojuego de Zombies en Python con Pygame" minuto 6:42
    hits = pygame.sprite.groupcollide(enemigos_list,balas,True,True, pygame.sprite.collide_circle)
    for hit in hits:
    # para cuando colisiones los enemigos se sume al score +10 y suene el sonido de explosion  
        score += 10
        explosion_sound.play()
# para que salga el sprite de explosion
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)

#esto sirve para cuando se elemine un zombie aparezca otro
        enemigos =  Enemigos()
        all_sprites.add(enemigos)
        enemigos_list.add(enemigos)


    hits = pygame.sprite.spritecollide(player, enemigos_list, True, pygame.sprite.collide_circle)
    #la colisiones del jugador con los enemigos
    for hit in hits:
        explosion_sound.play()
        booom0 = Explosion(hit.rect.center)
        all_sprites.add(booom0)
        player.shield -= 10
        #al golpear el zombie al jugador cargan los sprites
        enemigos = Enemigos()
        all_sprites.add(enemigos)
        enemigos_list.add (enemigos)

        #en caso del que jugador muera o tenga 0 de shield
        if player.shield <= 0:
            explosion_sound.play()
            boom = Explosion(player.rect.center)
            all_sprites.add(boom)
            player.kill()
            gritoplayer.play()
            risa.play()
            game_over = True
            show_go_screen ()

    all_sprites.update()

    #esto sirve para que la imagen se vaya moviendo a la izquierda constantemente
    x_relativa = x % fondo.get_rect().width
    ventana.blit(fondo,(x_relativa - fondo.get_rect().width, 0))
    if x_relativa < ANCHO:
        ventana.blit(fondo, (x_relativa, 0))
    x -=1

    all_sprites.draw(ventana)
    draw_text(ventana,f"puntos:{score}",25,ANCHO//2,10)
    draw_shield_bar(ventana, 5,5,player.shield)
    pygame.display.update()
    pygame.display.flip()
pygame.quit()