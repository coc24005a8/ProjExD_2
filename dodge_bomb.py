import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or ばくだんRect
    戻り値：判定結果タプル（横方向，縦方向）
    画面内ならTrue／画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向にはみ出ていたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向にはみ出ていたら
        tate = False
    return yoko, tate

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []  # 爆弾画像リスト
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))  # 爆弾用の空Surface
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  # 赤い爆弾円
        bb_img.set_colorkey((0, 0, 0))  # 四隅の黒い部分を透過
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]  # 爆弾加速度リスト
    return bb_imgs, bb_accs


def gameover(screen: pg.Surface) -> None:
    #black haikei
    black = pg.Surface((WIDTH, HEIGHT))
    black.fill((0, 0, 0))
    black.set_alpha(150)
    screen.blit(black, (0, 0))
    # Game Over
    font = pg.font.Font(None, 60)
    text = font.render("Game Over", True, (255, 255, 255))
    tx = WIDTH // 2 - text.get_width() // 2
    ty = HEIGHT // 2 - text.get_height() // 2
    screen.blit(text, (tx, ty))
    #cry koukaton
    kk_over = pg.image.load("fig/8.png")
    kk_over = pg.transform.rotozoom(kk_over, 0, 0.6)
    #left koukaton
    left_rct = kk_over.get_rect(center=(tx - 80, HEIGHT // 2))
    screen.blit(kk_over, left_rct)
    #right koukaton
    right_rct = kk_over.get_rect(center=(tx + text.get_width() + 80, HEIGHT // 2))
    screen.blit(kk_over, right_rct)

    pg.display.update()
    time.sleep(5)
 
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bb_imgs, bb_accs = init_bb_imgs() 
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = bb_imgs[0]  # 最初は一番小さい爆弾
    bb_rct = bb_img.get_rect()

    bb_rct.centerx = random.randint(0, WIDTH)  # 爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT)  # 爆弾縦座標
    vx, vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        # 1) 時間に応じて爆弾のサイズ・加速度を切替
        idx = min(tmr // 500, 9)
        old_center = bb_rct.center
        bb_img = bb_imgs[idx]
        bb_rct = bb_img.get_rect(center=old_center)
        ax = vx * bb_accs[idx]
        ay = vy * bb_accs[idx]
        bb_rct.move_ip(ax, ay)  # 爆弾移動（加速付き）

        #イベント処理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        #background
        screen.blit(bg_img, [0, 0])

        #move koukaton
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        #爆弾の反射判定
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        #当たり判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        #描画
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()

        #フレーム
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()