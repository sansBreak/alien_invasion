import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()  # 创建一个Settings实例，并赋给self.settings

        # 将游戏设为全屏模式
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # 通过设置类中的配置，来设置游戏的分辨率
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # 引入实例ship
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # 设置背景色
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 通过构筑辅助方法_check_events，来管理事件
            self._check_events()
            # 时刻更新飞船位置
            self.ship.update()
            # 更新子弹位置
            self._update_bullets()
            # 通过构筑辅助方法_update_screen，来更新屏幕
            self._update_screen()

    def _check_events(self):
        """监视键盘和鼠标事件"""
        # 当玩家单击游戏窗口的关闭按钮时，检测到pygame.QUIT事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # 通过方向键，持续控制飞船移动
            # 按下方向键
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # 抬起方向键
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        # 按下“q"键时退出游戏
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        # 更新屏幕上的图像，并切换到新屏幕
        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        # 将飞船绘制到屏幕上
        self.ship.blitme()
        # 将子弹绘制到屏幕上
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
