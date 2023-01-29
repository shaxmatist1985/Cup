#Паника
#Игрок должен ловить падающий бокал, пока она не упала до земли

from superwires import games, color
import random
games.init(screen_width = 640, screen_height = 480, fps = 50)
class Cart(games.Sprite):
    '''Тележка с которой игрок может ловить падающий бокал.'''
    image = games.load_image('cart.jpg')
    def __init__(self):
        '''Инициализирует объект Cart и создает объект Text для отображения счета.'''
        super(Cart, self).__init__(image = Cart.image,x=games.mouse.x, bottom = games.screen.height)
        self.score = games.Text(value =0, size =25, color =(0,100,0), top = 5, right = games.screen.width -10)
        games.screen.add(self.score)
    def update(self):
        '''Перемещает объект в позицию указателя.'''
        self.x = games.mouse.x
        if self.left<0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width
        self.check_catch()
    def check_catch(self):
        '''Проверяет поимал ли игрок бокал.'''
        for cup in self.overlapping_sprites:
            self.score.value +=10
            self.score.right = games.screen.width -10
            cup.handle_caught()
class Cup(games.Sprite):
    '''Падающий бокал.'''
    image = games.load_image('cup.jpg')
    speed = 1
    def __init__(self, x, y = 90):
        '''Инициализирует объект бокал.'''
        super(Cup, self).__init__(image = Cup.image, x= x, y = y, dy = Cup.speed)
    def update(self):
        '''Проверяет, не коснулась ли нижняя кромка спрайта нижней границы экрана.'''
        if self.bottom>games.screen.height:
            self.end_game()
            self.destroy()
    def handle_caught(self):
        '''Разрушает объект пойманный игроком.'''
        self.destroy()
    def end_game(self):
        '''Завершает игру.'''
        end_message =games.Message(value = 'Game Over', size = 90, color =(100,0,0),
                                   x= games.screen.width/2, y =games.screen.height/2,
                                   lifetime = 5*games.screen.fps,after_death = games.screen.quit)
        games.screen.add(end_message)
class Cat(games.Sprite):
    '''Кошка, которая, двигаясь влева-вправо, разбрасывает бокалы.'''
    image = games.load_image('cat.jpg')
    def __init__(self, y =55, speed =2, odds_change =200):
        """Инициализирует объект Cat."""
        super(Cat, self).__init__(image =Cat.image, x= games.screen.width/2, y=y, dx = speed)
        self.odds_change = odds_change
        self.time_til_drop = 0
    def update(self):
        '''Определяет, надо ли сменить направление.'''
        if self.left <0 or self.right > games.screen.width:
            self.dx=-self.dx
        elif random.randrange(self.odds_change)==0:
            self.dx = -self.dx
        self.check_drop()
    def check_drop(self):
        '''Уменьшает интервал ожидания на единицу или сбрасывает очередной бокал и восстанавливает исходный интервал.'''
        if self.time_til_drop > 0:
            self.time_til_drop -=1
        else:
            new_cup = Cup(x=self.x)
            games.screen.add(new_cup)
        #вне зависимости от скорости падения бокала "зазор" между падающими кругами принимается равным 30%
        #каждого из них по высоте
            self.time_til_drop = int(new_cup.height*1.3/Cup.speed)+1
def main():
    '''Собственно игровой процесс.'''

    wall_image = games.load_image('wall.jpg', transparent=False)
    games.screen.background = wall_image
    cat=Cat()
    games.screen.add(cat)
    cart= Cart()
    games.screen.add(cart)
    games.mouse.is_visible = False
    games.screen.event_grab = True
    games.screen.mainloop()
#поехали!
if __name__=='__main__':
    main()
