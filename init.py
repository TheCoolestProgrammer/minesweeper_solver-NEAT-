import pyautogui
from PIL import Image
import time
import random
class App:
    def __init__(self):
        self.field_width = 9
        self.field_height = 9
        self.visibility_area = 5

        self.numbers_colors = {
            # None:{(255,255,255)},
            1:{(0,0,255),},
            2: {(0,128,0),},
            3: {(255,0,0),},
            4: {(0,0,128),},
            5: {(128,0,0),},
            6: {(0,128,128),},
            7: {(0,0,0),},
            # 8: {(128,128,128),},
            "flag":{(255,0,0),(0,0,0),}
        }
        self.allowed_colors= [(0,0,255), (0,128,0),(255,0,0),(0,0,128),(128,0,0),(0,128,128),(0,0,0),(255,255,255)]

        time.sleep(5)
        screen = pyautogui.screenshot("screenshot.png")
        screen = Image.open("screenshot.png")
        pix = screen.load()

        width,height = screen.width,screen.height
        left_timer_founded=False
        left_timer_cords=[]
        for y in range(height//2, 0,-1):
            for x in range(width//2,0,-1):
                if pix[x,y] == (255,0,0):
                    left_timer_cords=[x,y]
                    left_timer_founded=True
                    break
            if left_timer_founded:
                break

        self.menu_begin_height=0
        for y in range(left_timer_cords[1], 0, -1):
            if pix[left_timer_cords[0],y] == (128,128,128):
                self.menu_begin_height= y

        self.field_begin_cords=[0,0]
        targets=[(128,128,128),(255,255,255)]
        color_now=0
        for y in range(left_timer_cords[1],height):
            if pix[left_timer_cords[0],y] == targets[color_now]:
                color_now+=1
                if color_now==len(targets):
                    self.field_begin_cords[1]=y
                    break

        for x in range(left_timer_cords[0],0,-1):
            if pix[x,self.field_begin_cords[1]]==(128,128,128):
                self.field_begin_cords[0]=x+1
                break
        x,y = self.field_begin_cords[0],self.field_begin_cords[1]
        targets=[(198,198,198),(255,255,255)]
        color_now=0
        while pix[x,y] != targets[color_now]:
            x+=1
            y+=1
        color_now+=1
        while pix[x,y] != targets[color_now]:
            x+=1
            y+=1

        self.cell_size = x-self.field_begin_cords[0]
        self.field=[[-1]*self.field_height for y in range(self.field_height)]

        self.black_pix_in_menu_normal=0
        self.smile_cords=[]
        for y in range(self.menu_begin_height, self.field_begin_cords[1]):
            for x in range(self.field_begin_cords[0],self.field_begin_cords[0]+self.cell_size*self.field_width):
                if pix[x,y]== (244,243,21):
                    self.smile_cords=[x,y]
                elif pix[x,y] ==(0,0,0):
                    self.black_pix_in_menu_normal+=1
        self.touch_threshold = 0.7

    def update_data(self):
        screen = pyautogui.screenshot("screenshot.png")
        screen = Image.open("screenshot.png")
        # screen = Image.open("test.png")
        pix = screen.load()
        for y in range(self.field_height):
            for x in range(self.field_width):
                cell_colors=set()
                for y2 in range(y*self.cell_size,(y+1)*self.cell_size):
                    for x2 in range(x*self.cell_size,(x+1)*self.cell_size):
                        # if x ==6 and y == 0 and y2-y >=9:
                        #     print(pix[self.field_begin_cords[0]+x2,self.field_begin_cords[1]+y2])
                        if pix[self.field_begin_cords[0]+x2,self.field_begin_cords[1]+y2] not in cell_colors \
                                and pix[self.field_begin_cords[0]+x2,self.field_begin_cords[1]+y2] in self.allowed_colors:
                            cell_colors.add(pix[self.field_begin_cords[0]+x2,self.field_begin_cords[1]+y2])
                res =0
                for i,j in zip(self.numbers_colors.keys(),self.numbers_colors.values()):
                    if cell_colors== j:
                        res = i
                        break
                if not res:
                    if cell_colors == {(255,255,255)}:
                        res = -1
                self.field[y][x] = res

    def is_game_over(self):
        # time.sleep((5))
        screen = pyautogui.screenshot("screenshot.png")
        screen = Image.open("screenshot.png")
        pix = screen.load()
        black_pix =0
        for y in range(self.menu_begin_height, self.field_begin_cords[1]):
            for x in range(self.field_begin_cords[0],self.field_begin_cords[0]+self.cell_size*self.field_width):
                if pix[x,y] ==(0,0,0):
                    black_pix+=1
        if black_pix == self.black_pix_in_menu_normal:
            return False
        else:
            return True

    def create_new_game(self):
        pyautogui.moveTo(self.smile_cords[0],self.smile_cords[1], duration=random.randint(21,32)/100)
        pyautogui.click()

        # border = self.visibility_area // 2
        # x = self.field_begin_cords[0]+ border * self.cell_size+5
        # y =self.field_begin_cords[1]+ border * self.cell_size+5
        # x,y=self.field_begin_cords[0]-5,self.field_begin_cords[1]-5
        # pyautogui.moveTo(x, y, duration=random.randint(56, 326) / 100)
        # pyautogui.click()
        pyautogui.moveTo(random.randint(0,600),random.randint(0,self.menu_begin_height-20), duration=random.randint(22,32)/100)
    def open_cells2(self,x,y,border,network):
        x_begin,x_end = x-border,x+border
        y_begin,y_end = y-border,y+border
        opened_cells=0
        game_over=False
        wrong_opened_cells=0
        for yy in range(y-border,y+border+1):
            for xx in range(x-border,x+border+1):

                field = [self.field[y2][x_begin:x_end+1] for y2 in range(y_begin, y_end + 1)]
                field = [j for i in field for j in i]
                res = network.activate(field)
                res = [res[self.visibility_area * i:self.visibility_area * (i + 1)] for i in range(self.visibility_area)]
                # id = yy*xx-(self.visibility_area-xx-1)
                if res[y_end-yy][x_end-xx] >=self.touch_threshold:
                    pyautogui.moveTo((x_begin + xx) * self.cell_size + self.field_begin_cords[0] + 5,
                                     (y_begin + yy) * self.cell_size + self.field_begin_cords[1] + 5,
                                     random.randint(21, 66) / 100)
                    pyautogui.click()
                    pyautogui.moveTo(random.randint(0, 600), random.randint(0, self.menu_begin_height))
                    if self.is_game_over():
                        game_over = True
                        break
                    else:
                        if self.field[yy][xx] !=-1:
                            # wrong_opened_cells+=1
                            pass
                        else:
                            opened_cells += 1
                            self.update_data()
            if game_over:
                break
        return opened_cells,wrong_opened_cells
    def open_cells(self,x,y,border,res):
        x_begin = x-border
        y_begin = y-border
        game_over=False
        opened_cells=0
        wrong_touches=0
        for i in range(len(res)):
            for j in range(len(res[i])):
                if res[i][j] >= self.touch_threshold:

                # if res[i][j] >=self.touch_threshold and self.field[y_begin+i][x_begin+j] == -1:
                    pyautogui.moveTo((x_begin+j)*self.cell_size+self.field_begin_cords[0]+5,
                                     (y_begin+i)*self.cell_size+self.field_begin_cords[1]+5,
                                     random.randint(21, 96) / 100)
                    pyautogui.click()
                    pyautogui.moveTo(random.randint(0, 600), random.randint(0, self.menu_begin_height))
                    if self.is_game_over():
                        game_over=True
                        wrong_touches+=1
                        break
                    else:
                        if res[i][j] >=self.touch_threshold and self.field[y_begin+i][x_begin+j] != -1:
                            wrong_touches+=1
                        else:
                            opened_cells+=1
                    # self.update_data()
                    # self.field[x_begin+i][y_begin+j] = res[i][j]
        # screen = pyautogui.screenshot("screenshot.png")
            if game_over:
                break
        return opened_cells,wrong_touches



