
import tkinter as tk
import random
from datetime import datetime, timedelta

# 游戏初始化设置
initial_army_count = 10  # 我方军营的初始兵力
initial_enemy_army_count = 10  # 敌方军营的初始兵力
circle_radius = 20  # 圆圈的半径

class Game:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        
        # 初始日期（公元183年1月1日）
        self.current_date = datetime(183, 1, 1)
        
        # 体力系统
        self.max_stamina = 5
        self.stamina = self.max_stamina
        
        # 游戏资源
        self.army_count = initial_army_count
        self.enemy_army_count = initial_enemy_army_count
        self.resources = {"粮食": 100, "金钱": 50, "木材": 30}

        # 内政系统
        self.commerce_level = 1
        self.agriculture_level = 1
        self.security_level = 1
        self.wall_repair_level = 0

        self.cities = []  # 存储所有城市和军营的位置及兵力
        
        self.init_main_menu()

    def init_main_menu(self):
        """初始化主界面"""
        self.clear_screen()
        
        # 顶部日期和体力显示
        self.date_label = tk.Label(self.root, text=f"日期: {self.current_date.strftime('%Y年%m月%d日')}", font=("Arial", 14))
        self.date_label.pack(pady=5, anchor='n')
        
        self.stamina_label = tk.Label(self.root, text=f"体力: {self.stamina}/{self.max_stamina}", font=("Arial", 14))
        self.stamina_label.pack(pady=5, anchor='n')
        
        # 右上角的内政数值GUI
        self.info_frame = tk.Frame(self.root, bg="lightgray", bd=2, relief="solid")
        self.info_frame.place(x=600, y=50, width=180, height=250)
        
        self.army_label = tk.Label(self.info_frame, text=f"我方兵力: {self.army_count}", bg="lightgray")
        self.army_label.pack(pady=5)

        self.resources_label = tk.Label(self.info_frame, text=f"资源: 粮食 {self.resources['粮食']} 金钱 {self.resources['金钱']} 木材 {self.resources['木材']}", bg="lightgray")
        self.resources_label.pack(pady=5)

        self.commerce_label = tk.Label(self.info_frame, text=f"商业: {self.commerce_level}", bg="lightgray")
        self.commerce_label.pack(pady=5)

        self.agriculture_label = tk.Label(self.info_frame, text=f"农业: {self.agriculture_level}", bg="lightgray")
        self.agriculture_label.pack(pady=5)

        self.security_label = tk.Label(self.info_frame, text=f"治安: {self.security_level}", bg="lightgray")
        self.security_label.pack(pady=5)

        self.wall_repair_label = tk.Label(self.info_frame, text=f"城墙修复: {self.wall_repair_level}", bg="lightgray")
        self.wall_repair_label.pack(pady=5)

        # 内政按钮
        self.commerce_button = tk.Button(self.root, text="提升商业", command=self.upgrade_commerce)
        self.commerce_button.pack(pady=5)

        self.agriculture_button = tk.Button(self.root, text="提升农业", command=self.upgrade_agriculture)
        self.agriculture_button.pack(pady=5)

        self.security_button = tk.Button(self.root, text="提升治安", command=self.upgrade_security)
        self.security_button.pack(pady=5)

        self.repair_wall_button = tk.Button(self.root, text="修复城墙", command=self.repair_wall)
        self.repair_wall_button.pack(pady=5)

        # 新增住宅按钮
        self.house_button = tk.Button(self.root, text="建设住宅", command=self.build_house)
        self.house_button.pack(pady=5)

        # 战斗按钮
        self.battle_button = tk.Button(self.root, text="开始战斗", command=self.start_battle)
        self.battle_button.pack(pady=10)

        # “征兵”按钮
        self.recruit_button = tk.Button(self.root, text="征兵", command=self.recruit_soldiers)
        self.recruit_button.pack(pady=10)

    def start_battle(self):
        """开始战斗，进入战斗界面"""
        if self.stamina > 0:
            self.stamina -= 1
            self.update_stamina()
            self.clear_screen()
            self.create_battle_map()
        else:
            print("体力不足，无法开始战斗。")

    def create_battle_map(self):
        """创建战斗地图"""
        # 使用Canvas绘制战斗地图
        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack(pady=20)
        
        # 创建我方和敌方的军营
        self.create_city(100, 100, "我方军营", "blue", self.army_count)
        self.create_city(700, 100, "敌方军营", "red", self.enemy_army_count)
        
        # 创建几个随机城市或村庄
        for _ in range(3):
            x = random.randint(100, 700)
            y = random.randint(100, 300)
            self.create_city(x, y, "村庄", "green", random.randint(5, 20))

    def create_city(self, x, y, label, color, army_count):
        """在地图上创建城市或军营"""
        # 检查新位置是否与现有城市重叠
        if self.check_overlap(x, y):
            return  # 如果重叠则不创建新城市
        
        # 绘制圆圈表示城市或军营
        circle = self.canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, fill=color, outline="black")
        
        # 添加士兵数量标签
        self.canvas.create_text(x, y, text=f"{army_count}兵", fill="white", font=("Arial", 10))
        
        # 保存该城市的信息（位置和兵力）
        self.cities.append({"x": x, "y": y, "label": label, "army_count": army_count, "circle_id": circle})

        # 绑定点击事件
        self.canvas.tag_bind(circle, "<Button-1>", lambda event, label=label, army_count=army_count, x=x, y=y: self.city_click(label, army_count, x, y))

    def check_overlap(self, x, y):
        """检查新城市是否与已有城市重叠"""
        for city in self.cities:
            dist = ((x - city["x"])**2 + (y - city["y"])**2)**0.5  # 计算两个圆心之间的距离
            if dist < circle_radius * 2:  # 如果距离小于两个圆的直径，认为是重叠
                return True
        return False

    def city_click(self, label, enemy_army_count, x, y):
        """处理点击城市或军营事件"""
        if label == "我方军营":
            print("选择了我方军营，不能攻击自己！")
            return
        
        if label == "敌方军营":
            self.start_attack(x, y, enemy_army_count)
        elif label == "村庄":
            self.attack_village(x, y, enemy_army_count)
        else:
            print(f"点击了城市 ({x}, {y})，无法进行攻击。")
    
    def start_attack(self, x, y, enemy_army_count):
        """启动攻击，进行战斗"""
        if self.army_count > 0:
            attack_strength = self.army_count  # 我方士兵数量决定攻击强度
            print(f"攻击敌方军营：{attack_strength} vs {enemy_army_count}")
            
            if enemy_army_count > attack_strength:
                new_enemy_strength = enemy_army_count - attack_strength
                print(f"敌方兵力减少，剩余 {new_enemy_strength}")
                
                # 更新敌方军营士兵数量
                self.update_city(x, y, "敌方军营", new_enemy_strength)
            else:
                # 我方占领敌方区域
                self.army_count -= enemy_army_count  # 减少我方兵力
                print(f"我方占领敌方军营，剩余兵力：{self.army_count}")
                
                # 修改为我方占领
                self.canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, fill="blue", outline="black")
                self.canvas.create_text(x, y, text="我方占领", fill="white", font=("Arial", 10))
                
                # 移除敌方的城市
                self.cities = [city for city in self.cities if not (city["x"] == x and city["y"] == y)]
                
    def attack_village(self, x, y, village_army_count):
        """攻击村庄"""
        if self.army_count > 0:
            attack_strength = self.army_count  # 我方士兵数量决定攻击强度
            print(f"攻击村庄：{attack_strength} vs {village_army_count}")
            
            # 我方胜利
            self.army_count += village_army_count  # 村庄的兵力加入我方
            print(f"占领村庄，我方兵力增加，当前兵力: {self.army_count}")
            
            # 修改为我方占领
            self.canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, fill="blue", outline="black")
            self.canvas.create_text(x, y, text="我方占领", fill="white", font=("Arial", 10))
            
            # 移除村庄的兵力信息
            self.cities = [city for city in self.cities if not (city["x"] == x and city["y"] == y)]

    def update_city(self, x, y, label, new_army_count):
        """更新城市的士兵数量"""
        for city in self.cities:
            if city["x"] == x and city["y"] == y:
                city["army_count"] = new_army_count
                self.canvas.create_text(x, y, text=f"{new_army_count}兵", fill="white", font=("Arial", 10))
                break

    def recruit_soldiers(self):
        """征兵功能，增加兵力"""
        if self.stamina > 0:
            self.stamina -= 1
            self.update_stamina()
            recruit_count = 5
            self.army_count += recruit_count
            print(f"征兵成功！我方兵力增加了 {recruit_count}。当前兵力: {self.army_count}")
            
            # 更新军营兵力显示
            self.update_city(100, 100, "我方军营", self.army_count)
        else:
            print("体力不足，无法征兵。")

    def build_house(self):
        """建设住宅，恢复体力"""
        if self.stamina < self.max_stamina:
            self.stamina = self.max_stamina
            self.update_stamina()
            self.current_date += timedelta(days=1)
            self.date_label.config(text=f"日期: {self.current_date.strftime('%Y年%m月%d日')}")
            print("住宅建设完成，体力恢复！")
        else:
            print("体力已满，无需恢复。")

    def upgrade_commerce(self):
        """提升商业"""
        if self.stamina > 0:
            self.stamina -= 1
            self.update_stamina()
            if self.resources["金钱"] >= 20:
                self.resources["金钱"] -= 20
                self.commerce_level += 1
                print(f"商业提升到 {self.commerce_level} 级")
                self.commerce_label.config(text=f"商业: {self.commerce_level}")
            else:
                print("金钱不足，无法提升商业。")
        else:
            print("体力不足，无法提升商业。")

    def upgrade_agriculture(self):
        """提升农业"""
        if self.stamina > 0:
            self.stamina -= 1
            self.update_stamina()
            if self.resources["木材"] >= 15:
                self.resources["木材"] -= 15
                self.agriculture_level += 1
                print(f"农业提升到 {self.agriculture_level} 级")
                self.agriculture_label.config(text=f"农业: {self.agriculture_level}")
            else:
                print("木材不足，无法提升农业。")
        else:
            print("体力不足，无法提升农业。")

    def upgrade_security(self):
        """提升治安"""
        if self.stamina > 0:
            self.stamina -= 1
            self.update_stamina()
            if self.resources["粮食"] >= 10:
                self.resources["粮食"] -= 10
                self.security_level += 1
                print(f"治安提升到 {self.security_level} 级")
                self.security_label.config(text=f"治安: {self.security_level}")
            else:
                print("粮食不足，无法提升治安。")
        else:
            print("体力不足，无法提升治安。")

    def repair_wall(self):
        """修复城墙"""
        if self.stamina > 0:
            self.stamina -= 1
            self.update_stamina()
            if self.resources["金钱"] >= 30:
                self.resources["金钱"] -= 30
                self.wall_repair_level += 1
                print(f"城墙修复到 {self.wall_repair_level} 级")
                self.wall_repair_label.config(text=f"城墙修复: {self.wall_repair_level}")
            else:
                print("金钱不足，无法修复城墙。")
        else:
            print("体力不足，无法修复城墙。")

    def update_stamina(self):
        """更新体力显示"""
        self.stamina_label.config(text=f"体力: {self.stamina}/{self.max_stamina}")

    def clear_screen(self):
        """清空当前界面"""
        for widget in self.root.winfo_children():
            widget.destroy()

# 设置主窗口
root = tk.Tk()
root.title("帝国建设游戏")
game = Game(root)

# 启动游戏
root.mainloop()
