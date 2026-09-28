import os, datetime, threading, webbrowser, requests
from kivy.core.text import LabelBase
Labelbase.register(name='roboto',fn_regular='assets/chinese_font.ttf')
from kivy.app import App
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

Window.clearcolor = (0.95, 0.95, 0.98, 1)

class CalendarApp(App):
    def build(self):
        self.user_data = {"is_logged_in": False, "nickname": "未登录", "signature": "许你一生不嵩手🍃", "avatar": "", "background": ""}
        self.about_click_count = 0
        self.contact_click_count = 0
        self.custom_time_enabled = False
        self.alarm_time = None
        self.alarm_ringtone = ""

        self.root_layout = FloatLayout()
        self.bg_image = Image(source="", allow_stretch=True, keep_ratio=False, size_hint=(1, 1), opacity=0.8)
        self.root_layout.add_widget(self.bg_image)

        self.main_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.content_area = BoxLayout(orientation='vertical')
        self.main_layout.add_widget(self.content_area)

        dock = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5), padding=dp(5))
        dock.add_widget(Button(text="主页", background_color=(0.4, 0.6, 0.9, 1), on_release=self.show_home))
        dock.add_widget(Button(text="我", background_color=(0.4, 0.6, 0.9, 1), on_release=self.show_me))
        self.main_layout.add_widget(dock)

        self.root_layout.add_widget(self.main_layout)
        self.show_home()
        return self.root_layout

    def show_home(self, *args):
        self.content_area.clear_widgets()
        self.home_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.date_label = Label(text="日期：加载中...", font_size=dp(22), size_hint_y=None, height=dp(45))
        self.time_label = Label(text="时间：加载中...", font_size=dp(24), size_hint_y=None, height=dp(45))
        self.weather_label = Label(text="天气：加载中...", font_size=dp(20), size_hint_y=None, height=dp(45))
        self.home_layout.add_widget(self.date_label)
        self.home_layout.add_widget(self.time_label)
        self.home_layout.add_widget(self.weather_label)
        self.custom_card_container = BoxLayout(orientation='vertical', size_hint_y=None, height=0)
        self.home_layout.add_widget(self.custom_card_container)
        self.content_area.add_widget(self.home_layout)
        threading.Thread(target=self.fetch_network_data, daemon=True).start()

    def fetch_network_data(self):
        now = datetime.datetime.now()
        date_str = now.strftime("%Y年%m月%d日")
        time_str = now.strftime("%H:%M:%S")
        city = "未知"
        try:
            loc_resp = requests.get("http://ip-api.com/json/", timeout=5).json()
            if loc_resp.get("status") == "success": city = loc_resp.get("city", "未知")
        except: city = "定位失败"
        weather_str = "天气获取失败"
        try:
            weather_resp = requests.get("https://api.open-meteo.com/v1/forecast?latitude=39.9042&longitude=116.4074&current_weather=true", timeout=5).json()
            weather_str = f"{city} | {weather_resp['current_weather']['temperature']}°C"
        except: pass
        Clock.schedule_once(lambda dt: self.update_ui(date_str, time_str, weather_str), 0)

    def update_ui(self, date_str, time_str, weather_str):
        if hasattr(self, 'date_label'):
            self.date_label.text = f"📅 {date_str}"
            self.time_label.text = f"🕒 {time_str}"
            self.weather_label.text = f"🌤️ {weather_str}"

    def show_about(self, *args):
        self.content_area.clear_widgets()
        self.about_click_count = 0
        layout = BoxLayout(orientation='vertical', padding=dp(20))
        layout.add_widget(Label(size_hint_y=None, height=dp(50)))
        app_name = Label(text="日历工具箱", font_size=dp(32), bold=True, size_hint_y=None, height=dp(60))
        layout.add_widget(app_name)
        layout.add_widget(Label(text="宫本，_____。", font_size=dp(16), color=(0.4, 0.4, 0.4, 1), size_hint_y=None, height=dp(30)))
        contact_btn = Button(text="联系作者", size_hint_y=None, height=dp(50), background_color=(0.3, 0.6, 0.9, 1))
        contact_btn.bind(on_release=self.handle_contact_author)
        layout.add_widget(contact_btn)
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        layout.add_widget(Label(text="版本 0.1", font_size=dp(14), color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=dp(30)))
        app_name.bind(on_touch_down=self.on_about_touch)
        self.content_area.add_widget(layout)

    def on_about_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.about_click_count += 1
            if self.about_click_count == 5:
                self.show_toast("一直点这里干嘛，这里没东西😣")
                if self.custom_time_enabled:
                    self.custom_time_enabled = False
                    self.custom_card_container.clear_widgets()
                    self.custom_card_container.height = 0
            elif self.about_click_count >= 10:
                self.about_click_count = 0
                self.custom_time_enabled = True
                self.show_custom_time_dialog()

    def handle_contact_author(self, instance):
        self.contact_click_count += 1
        if self.contact_click_count == 1:
            Clipboard.copy("44521667")
            self.show_custom_popup("你联系我干嘛", "关闭", self.close_contact_popup)
        elif self.contact_click_count == 2:
            self.show_custom_popup("你真的要联系我吗？", "关闭", self.close_contact_popup)
        elif self.contact_click_count >= 3:
            self.contact_click_count = 0
            content = BoxLayout(orientation='horizontal', spacing=dp(10), padding=dp(10))
            close_btn = Button(text="关闭", background_color=(0.8, 0.3, 0.3, 1))
            qq_btn = Button(text="QQ", background_color=(0.3, 0.8, 0.3, 1))
            popup = Popup(title="既然你这么坚持那就满足你吧😄", size_hint=(0.8, 0.4))
            def close_action(instance): popup.dismiss()
            def qq_action(instance):
                Clipboard.copy("44521667")
                popup.dismiss()
                self.show_toast("作者QQ已复制，去QQ粘贴搜索吧")
                Clock.schedule_once(lambda dt: self.try_open_qq(), 5)
            close_btn.bind(on_release=close_action)
            qq_btn.bind(on_release=qq_action)
            content.add_widget(close_btn)
            content.add_widget(qq_btn)
            popup.content = content
            popup.open()

    def close_contact_popup(self, instance):
        instance.parent.parent.dismiss()

    def show_custom_popup(self, text, btn_text, callback):
        layout = BoxLayout(orientation='vertical', padding=dp(10))
        layout.add_widget(Label(text=text, font_size=dp(18)))
        btn = Button(text=btn_text, size_hint_y=None, height=dp(45))
        btn.bind(on_release=callback)
        layout.add_widget(btn)
        popup = Popup(title="提示", content=layout, size_hint=(0.8, 0.4))
        popup.open()

    def try_open_qq(self):
        try: webbrowser.open("mqqwpa://im/chat?chat_type=wpa&uin=44521667&version=1&src_type=web")
        except: pass

    def show_me(self, *args):
        self.content_area.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        avatar_btn = Button(text="头像", size_hint=(None, None), size=(dp(100), dp(100)), background_color=(0.7, 0.8, 1, 1))
        avatar_btn.pos_hint = {'center_x': 0.5}
        if self.user_data["is_logged_in"]:
            avatar_btn.text = "点击修改"
            avatar_btn.bind(on_release=self.edit_profile_dialog)
        else:
            avatar_btn.bind(on_release=self.login_action)
        layout.add_widget(avatar_btn)
        nickname_lbl = Label(text=self.user_data["nickname"], font_size=dp(24), size_hint_y=None, height=dp(40))
        layout.add_widget(nickname_lbl)
        signature_lbl = Label(text=self.user_data["signature"], font_size=dp(14), color=(0.3, 0.3, 0.3, 1), size_hint_y=None, height=dp(30))
        if self.user_data["is_logged_in"]:
            signature_lbl.bind(on_touch_down=self.edit_signature_action)
        layout.add_widget(signature_lbl)
        layout.add_widget(Button(text="设置背景图", size_hint_y=None, height=dp(45), on_release=self.show_bg_options))
        layout.add_widget(Button(text="闹钟设置", size_hint_y=None, height=dp(45), on_release=self.alarm_setup_dialog))
        about_btn = Button(text="关于", size_hint_y=None, height=dp(45), background_color=(0.2, 0.5, 0.8, 1))
        about_btn.bind(on_release=self.show_about)
        layout.add_widget(about_btn)
        self.content_area.add_widget(layout)

    def login_action(self, instance):
        self.user_data["is_logged_in"] = True
        self.user_data["nickname"] = "点击修改昵称"
        self.show_me()

    def edit_profile_dialog(self, instance):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        layout.add_widget(Label(text="输入新昵称 (最多14字符或8个汉字，不能有空格)："))
        nickname_input = TextInput(text=self.user_data["nickname"], multiline=False)
        layout.add_widget(nickname_input)
        layout.add_widget(Label(text="头像路径 (可留空)"))
        avatar_input = TextInput(text="", multiline=False)
        layout.add_widget(avatar_input)
        confirm_btn = Button(text="保存", size_hint_y=None, height=dp(50))
        popup = Popup(title="修改资料", content=layout, size_hint=(0.9, 0.7))
        def save_profile(instance):
            new_nickname = nickname_input.text.strip()
            if " " in new_nickname or len(new_nickname) > 14:
                self.show_toast("昵称不规范！不能有空格，且最长14字符")
                return
            self.user_data["nickname"] = new_nickname if new_nickname else self.user_data["nickname"]
            if avatar_input.text.strip(): self.user_data["avatar"] = avatar_input.text.strip()
            popup.dismiss()
            self.show_me()
            self.show_toast("资料已保存")
        confirm_btn.bind(on_release=save_profile)
        layout.add_widget(confirm_btn)
        popup.open()

    def edit_signature_action(self, instance, touch):
        if instance.collide_point(*touch.pos):
            layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
            layout.add_widget(Label(text="修改个性签名 (字数不限)："))
            sig_input = TextInput(text=self.user_data["signature"], multiline=True)
            layout.add_widget(sig_input)
            confirm_btn = Button(text="保存", size_hint_y=None, height=dp(50))
            popup = Popup(title="修改签名", content=layout, size_hint=(0.9, 0.6))
            def save_sig(instance):
                self.user_data["signature"] = sig_input.text.strip()
                popup.dismiss()
                self.show_me()
                self.show_toast("签名已保存")
            confirm_btn.bind(on_release=save_sig)
            layout.add_widget(confirm_btn)
            popup.open()

    def show_bg_options(self, instance):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        layout.add_widget(Label(text="选择自定义背景图片，或使用内置图"))
        file_input = TextInput(text="/sdcard/Download/", multiline=False)
        layout.add_widget(file_input)
        apply_btn = Button(text="应用自定义背景", size_hint_y=None, height=dp(45))
        popup = Popup(title="背景设置", content=layout, size_hint=(0.9, 0.6))
        def apply_bg(instance):
            path = file_input.text.strip()
            if os.path.exists(path):
                self.bg_image.source = path
                self.show_toast("背景已应用")
            else: self.show_toast("文件不存在，请检查路径")
            popup.dismiss()
        apply_btn.bind(on_release=apply_bg)
        layout.add_widget(apply_btn)
        inner_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        for i in range(1, 6):
            img_btn = Button(text=f"内置{i}")
            img_btn.bind(on_release=lambda instance, idx=i: self.apply_inner_bg(idx))
            inner_layout.add_widget(img_btn)
        layout.add_widget(inner_layout)
        popup.open()

    def apply_inner_bg(self, idx):
        path = f"assets/bg{idx}.jpg"
        if os.path.exists(path):
            self.bg_image.source = path
            self.show_toast(f"已应用内置图 {idx}")
        else: self.show_toast(f"内置图 {idx} 不存在，请放入 assets/bg{idx}.jpg")

    def alarm_setup_dialog(self, instance):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        layout.add_widget(Label(text="设置闹钟时间 (时:分):"))
        time_input = TextInput(text="07:00", multiline=False)
        layout.add_widget(time_input)
        layout.add_widget(Label(text="铃声路径 (填写本地文件绝对路径，如 /sdcard/Music/ring.mp3):"))
        ring_input = TextInput(text="", multiline=False)
        layout.add_widget(ring_input)
        confirm_btn = Button(text="设置闹钟", size_hint_y=None, height=dp(50))
        popup = Popup(title="闹钟设置", content=layout, size_hint=(0.9, 0.7))
        def set_alarm(instance):
            self.alarm_time = time_input.text.strip()
            self.alarm_ringtone = ring_input.text.strip()
            popup.dismiss()
            self.show_toast(f"闹钟已设置为 {self.alarm_time}")
        confirm_btn.bind(on_release=set_alarm)
        layout.add_widget(confirm_btn)
        popup.open()

    def show_custom_time_dialog(self):
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        layout.add_widget(Label(text="设置年份："))
        year_input = TextInput(text="2026", input_filter='int', multiline=False)
        layout.add_widget(year_input)
        layout.add_widget(Label(text="设置月份 (最高 14)："))
        month_input = TextInput(text="9", input_filter='int', multiline=False)
        layout.add_widget(month_input)
        layout.add_widget(Label(text="设置日期 (最高 32)："))
        day_input = TextInput(text="31", input_filter='int', multiline=False)
        layout.add_widget(day_input)
        layout.add_widget(Label(text="设置星期 (最高 8)："))
        week_input = TextInput(text="8", input_filter='int', multiline=False)
        layout.add_widget(week_input)
        confirm_btn = Button(text="生成选项卡", size_hint_y=None, height=dp(50), background_color=(0.3, 0.6, 1, 1))
        popup = Popup(title="自定义时间", content=layout, size_hint=(0.9, 0.8))
        def create_tab(instance):
            year, month, day, week = year_input.text or "2026", month_input.text or "1", day_input.text or "1", week_input.text or "1"
            if int(month) > 14: month = "14"
            if int(day) > 32: day = "32"
            custom_text = f"自定义时间：{year}年{month}月{day}日 星期{week}"
            self.custom_card_container.clear_widgets()
            self.custom_card_container.add_widget(Label(text=custom_text, font_size=dp(18), color=(0.8, 0.2, 0.2, 1)))
            self.custom_card_container.height = dp(50)
            popup.dismiss()
            self.show_toast("自定义时间已生成")
        confirm_btn.bind(on_release=create_tab)
        layout.add_widget(confirm_btn)
        popup.open()

    def show_toast(self, message):
        popup = Popup(title="提示", content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

if __name__ == '__main__':
    CalendarApp().run()
