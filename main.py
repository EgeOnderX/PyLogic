import pygame
import sys
import random
import json
import os
import tkinter as tk
from tkinter import messagebox
from gates import MyGate, MySwitch, MyLight, MyWire

CONFIG_FILE = "config.cfg"

config_data = {
    "language": "EN",
    "fullscreen": False,
    "theme": "DARK"
}

if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r") as f:
            loaded_config = json.load(f)
            config_data.update(loaded_config)
    except Exception:
        pass

current_lang = config_data["language"]
is_fullscreen = config_data["fullscreen"]
current_theme_key = config_data["theme"]

def save_config():
    """Kapanışta mevcut durumu config.cfg'ye yazar."""
    with open(CONFIG_FILE, "w") as f:
        json.dump({
            "language": current_lang,
            "fullscreen": is_fullscreen,
            "theme": current_theme_key
        }, f, indent=4)

pygame.init()

WIDTH, HEIGHT = 1100, 700
SIDEBAR_WIDTH = 210
MENU_BAR_HEIGHT = 45
COMPONENT_BUTTON_HEIGHT = 42

if is_fullscreen:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
    
pygame.display.set_caption("PyLogic")
clock = pygame.time.Clock()


LANGUAGES = {
    "TR": {
        "file": "Dosya", "settings": "Ayarlar", "about": "Hakkında",
        "save": "Kaydet (S)", "open": "Aç (L)", "exit": "Çıkış",
        "fullscreen": "Tam Ekran", "theme": "Tema Değiştir", "language": "Dil",
        "dark": "Karanlık Mod", "light": "Aydınlık Mod", "saved": "Devre başarıyla kaydedildi!", "loaded": "Devre yüklendi!"
    },
    "EN": {
        "file": "File", "settings": "Settings", "about": "About",
        "save": "Save (S)", "open": "Open (L)", "exit": "Exit",
        "fullscreen": "Fullscreen", "theme": "Toggle Theme", "language": "Language",
        "dark": "Dark Mode", "light": "Light Mode", "saved": "Circuit saved successfully!", "loaded": "Circuit loaded!"
    },
    "DE": {
        "file": "Datei", "settings": "Einstellungen", "about": "Über",
        "save": "Speichern (S)", "open": "Öffnen (L)", "exit": "Beenden",
        "fullscreen": "Vollbild", "theme": "Theme wechseln", "language": "Sprache",
        "dark": "Dunkelmodus", "light": "Hellmodus", "saved": "Schaltung gespeichert!", "loaded": "Schaltung geladen!"
    },
    "FR": {
        "file": "Fichier", "settings": "Paramètres", "about": "À propos",
        "save": "Enregistrer (S)", "open": "Ouvrir (L)", "exit": "Quitter",
        "fullscreen": "Plein écran", "theme": "Changer le thème", "language": "Langue",
        "dark": "Mode sombre", "light": "Mode clair", "saved": "Circuit enregistré!", "loaded": "Circuit chargé!"
    }
}

THEMES = {
    "LIGHT": {
        "bg": (248, 249, 250),
        "grid": (230, 233, 236),
        "sidebar": (233, 236, 239),
        "menubar": (222, 226, 230),
        "btn": (206, 212, 218),
        "btn_hover": (173, 181, 189),
        "text": (33, 37, 41),
        "accent": (0, 122, 255),
        "wire_preview": (108, 117, 125)
    },
    "DARK": {
        "bg": (24, 24, 28),
        "grid": (34, 34, 40),
        "sidebar": (32, 32, 38),
        "menubar": (40, 40, 48),
        "btn": (52, 58, 64),
        "btn_hover": (73, 80, 87),
        "text": (248, 249, 250),
        "accent": (10, 132, 255),
        "wire_preview": (142, 142, 147)
    }
}

colors = THEMES[current_theme_key]

font = pygame.font.SysFont("Segoe UI", 15)
font_bold = pygame.font.SysFont("Segoe UI", 15, bold=True)

COMPONENTS = ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR", "Switch", "LED"]
gates = []
switches = []
leds = []
wires = []

selected_component = None
dragging_component = None
current_wire = None

active_menu = None

def get_txt(key):
    return LANGUAGES[current_lang].get(key, key)

def show_about_window():
    root = tk.Tk()
    root.withdraw()
    license_text = (
        "MIT License\n\n"
        "Copyright (c) 2025 Ege Önder\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE."
    )
    messagebox.showinfo("About PyLogic", license_text)
    root.destroy()

def save_circuit(filename="circuit.json"):
    data = {
        "gates": [{"x": g.x, "y": g.y, "type": g.gate_type, "state": g.state} for g in gates],
        "switches": [{"x": s.x, "y": s.y, "state": s.state} for s in switches],
        "leds": [{"x": l.x, "y": l.y, "state": l.state} for l in leds],
        "wires": []
    }
    for w in wires:
        try:
            start_list = gates + switches
            end_list = gates + leds
            data["wires"].append({
                "start_idx": start_list.index(w.start_comp),
                "start_slot": w.start_slot,
                "end_idx": end_list.index(w.end_comp),
                "end_slot": w.end_slot,
                "color": list(w.color) if hasattr(w, 'color') else [0, 0, 0]
            })
        except ValueError:
            continue
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(get_txt("saved"))

def load_circuit(filename="circuit.json"):
    global gates, switches, leds, wires
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return

    gates = [MyGate(g["x"], g["y"], g["type"]) for g in data["gates"]]
    for g, g_data in zip(gates, data["gates"]): g.state = g_data["state"]

    switches = [MySwitch(s["x"], s["y"]) for s in data["switches"]]
    for s, s_data in zip(switches, data["switches"]): s.state = s_data["state"]

    leds = [MyLight(l["x"], l["y"]) for l in data["leds"]]
    for l, l_data in zip(leds, data["leds"]): l.state = l_data["state"]

    wires = []
    for w_data in data["wires"]:
        try:
            start_list = gates + switches
            end_list = gates + leds
            wires.append(MyWire(start_list[w_data["start_idx"]], w_data["start_slot"], end_list[w_data["end_idx"]], w_data["end_slot"], w_data["color"]))
        except (ValueError, IndexError):
            continue
    print(get_txt("loaded"))

def draw_background_grid():
    grid_size = 25
    for x in range(SIDEBAR_WIDTH, WIDTH, grid_size):
        pygame.draw.line(screen, colors["grid"], (x, MENU_BAR_HEIGHT), (x, HEIGHT), 1)
    for y in range(MENU_BAR_HEIGHT, HEIGHT, grid_size):
        pygame.draw.line(screen, colors["grid"], (SIDEBAR_WIDTH, y), (WIDTH, y), 1)

def draw_ui():
    mouse_pos = pygame.mouse.get_pos()
    
    pygame.draw.rect(screen, colors["sidebar"], (0, MENU_BAR_HEIGHT, SIDEBAR_WIDTH, HEIGHT - MENU_BAR_HEIGHT))
    pygame.draw.line(screen, colors["grid"], (SIDEBAR_WIDTH, MENU_BAR_HEIGHT), (SIDEBAR_WIDTH, HEIGHT), 2)
    
    for i, name in enumerate(COMPONENTS):
        rect = pygame.Rect(12, MENU_BAR_HEIGHT + 15 + i * (COMPONENT_BUTTON_HEIGHT + 12), SIDEBAR_WIDTH - 24, COMPONENT_BUTTON_HEIGHT)
        is_hover = rect.collidepoint(mouse_pos)
        btn_color = colors["btn_hover"] if is_hover else colors["btn"]
        
        pygame.draw.rect(screen, btn_color, rect, border_radius=8)
        text = font_bold.render(name, True, colors["text"])
        screen.blit(text, (rect.x + 16, rect.y + (COMPONENT_BUTTON_HEIGHT - text.get_height()) // 2))

        if name == selected_component:
            pygame.draw.rect(screen, colors["accent"], rect, 2, border_radius=8)

    pygame.draw.rect(screen, colors["menubar"], (0, 0, WIDTH, MENU_BAR_HEIGHT))
    pygame.draw.line(screen, colors["grid"], (0, MENU_BAR_HEIGHT), (WIDTH, MENU_BAR_HEIGHT), 2)
    
    global menu_file_rect, menu_settings_rect, menu_about_rect
    menu_file_rect = pygame.Rect(10, 6, 90, MENU_BAR_HEIGHT - 12)
    menu_settings_rect = pygame.Rect(105, 6, 110, MENU_BAR_HEIGHT - 12)
    menu_about_rect = pygame.Rect(220, 6, 110, MENU_BAR_HEIGHT - 12)

    for r, text_key in [(menu_file_rect, "file"), (menu_settings_rect, "settings"), (menu_about_rect, "about")]:
        if r.collidepoint(mouse_pos) or (active_menu == "file" and text_key == "file") or (active_menu == "settings" and text_key == "settings"):
            pygame.draw.rect(screen, colors["btn_hover"], r, border_radius=6)
        txt = font_bold.render(get_txt(text_key), True, colors["text"])
        screen.blit(txt, (r.x + (r.width - txt.get_width()) // 2, r.y + (r.height - txt.get_height()) // 2))

    if active_menu == "file": draw_file_dropdown()
    elif active_menu == "settings": draw_settings_dropdown()

def draw_file_dropdown():
    global dropdown_save_rect, dropdown_open_rect, dropdown_exit_rect
    x, y = menu_file_rect.x, MENU_BAR_HEIGHT + 2
    w, h = 180, 38
    mouse_pos = pygame.mouse.get_pos()
    
    dropdown_save_rect = pygame.Rect(x, y, w, h)
    dropdown_open_rect = pygame.Rect(x, y + h, w, h)
    dropdown_exit_rect = pygame.Rect(x, y + h * 2, w, h)

    pygame.draw.rect(screen, colors["menubar"], (x, y, w, h * 3), border_radius=6)
    pygame.draw.rect(screen, colors["btn_hover"], (x, y, w, h * 3), 1, border_radius=6)

    for r, key in [(dropdown_save_rect, "save"), (dropdown_open_rect, "open"), (dropdown_exit_rect, "exit")]:
        if r.collidepoint(mouse_pos):
            pygame.draw.rect(screen, colors["btn_hover"], r, border_radius=4)
        txt = font.render(get_txt(key), True, colors["text"])
        screen.blit(txt, (r.x + 14, r.y + (r.height - txt.get_height()) // 2))

def draw_settings_dropdown():
    global dropdown_fs_rect, dropdown_theme_rect, lang_buttons
    x, y = menu_settings_rect.x, MENU_BAR_HEIGHT + 2
    w, h = 280, 42
    mouse_pos = pygame.mouse.get_pos()

    dropdown_fs_rect = pygame.Rect(x, y, w, h)
    dropdown_theme_rect = pygame.Rect(x, y + h, w, h)
    lang_area_rect = pygame.Rect(x, y + h * 2, w, h + 15)

    pygame.draw.rect(screen, colors["menubar"], (x, y, w, h * 3 + 15), border_radius=6)
    pygame.draw.rect(screen, colors["btn_hover"], (x, y, w, h * 3 + 15), 1, border_radius=6)

    if dropdown_fs_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, colors["btn_hover"], dropdown_fs_rect, border_radius=4)
    txt_fs = font.render(get_txt("fullscreen"), True, colors["text"])
    screen.blit(txt_fs, (dropdown_fs_rect.x + 12, dropdown_fs_rect.y + (h - txt_fs.get_height()) // 2))
    
    cb_rect = pygame.Rect(dropdown_fs_rect.x + w - 32, dropdown_fs_rect.y + (h - 20) // 2, 20, 20)
    pygame.draw.rect(screen, colors["text"], cb_rect, 2, border_radius=4)
    if is_fullscreen:
        pygame.draw.rect(screen, colors["accent"], cb_rect.inflate(-6, -6), border_radius=2)

    if dropdown_theme_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, colors["btn_hover"], dropdown_theme_rect, border_radius=4)
    current_mode_text = get_txt("dark") if current_theme_key == "DARK" else get_txt("light")
    txt_theme = font.render(f"{get_txt('theme')}: {current_mode_text}", True, colors["text"])
    screen.blit(txt_theme, (dropdown_theme_rect.x + 12, dropdown_theme_rect.y + (h - txt_theme.get_height()) // 2))

    txt_lang = font_bold.render(get_txt("language"), True, colors["text"])
    screen.blit(txt_lang, (lang_area_rect.x + 12, lang_area_rect.y + 4))
    
    lang_buttons = {}
    langs = ["TR", "EN", "DE", "FR"]
    btn_w = 52
    for idx, l_code in enumerate(langs):
        bx = lang_area_rect.x + 12 + idx * (btn_w + 8)
        by = lang_area_rect.y + 26
        br = pygame.Rect(bx, by, btn_w, 24)
        lang_buttons[l_code] = br
        
        b_color = colors["accent"] if current_lang == l_code else (colors["btn_hover"] if br.collidepoint(mouse_pos) else colors["btn"])
        pygame.draw.rect(screen, b_color, br, border_radius=5)
        l_txt = font.render(l_code, True, (255, 255, 255) if current_lang == l_code else colors["text"])
        screen.blit(l_txt, (br.x + (br.width - l_txt.get_width()) // 2, br.y + (br.height - l_txt.get_height()) // 2))

running = True
while running:
    colors = THEMES[current_theme_key]
    screen.fill(colors["bg"])
    draw_background_grid()

    for gate in gates: gate.draw(screen)
    for s in switches: s.draw(screen)
    for led in leds: led.draw(screen)
    for w in wires: w.draw(screen)

    if current_wire:
        pts = current_wire.points + [pygame.mouse.get_pos()]
        if len(pts) > 1:
            pygame.draw.lines(screen, colors["wire_preview"], False, pts, 3)

    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s: save_circuit()
            elif event.key == pygame.K_l: load_circuit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if active_menu == "file":
                if dropdown_save_rect.collidepoint(mouse_pos):
                    save_circuit(); active_menu = None; continue
                elif dropdown_open_rect.collidepoint(mouse_pos):
                    load_circuit(); active_menu = None; continue
                elif dropdown_exit_rect.collidepoint(mouse_pos):
                    running = False; continue
                    
            elif active_menu == "settings":
                if dropdown_fs_rect.collidepoint(mouse_pos):
                    is_fullscreen = not is_fullscreen
                    
                    pygame.display.quit()
                    pygame.display.init()
                    
                    if is_fullscreen:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
                        
                    pygame.display.set_caption("PyLogic")
                    
                    colors = THEMES[current_theme_key]
                    screen.fill(colors["bg"])
                    draw_background_grid()
                    draw_ui() 
                    pygame.display.flip()
                    
                    active_menu = None
                    continue
                elif dropdown_theme_rect.collidepoint(mouse_pos):
                    current_theme_key = "DARK" if current_theme_key == "LIGHT" else "LIGHT"
                    continue
                else:
                    lang_clicked = False
                    for l_code, rect in lang_buttons.items():
                        if rect.collidepoint(mouse_pos):
                            current_lang = l_code
                            lang_clicked = True
                            break
                    if lang_clicked: continue

            if menu_file_rect.collidepoint(mouse_pos):
                active_menu = "file" if active_menu != "file" else None
                continue
            elif menu_settings_rect.collidepoint(mouse_pos):
                active_menu = "settings" if active_menu != "settings" else None
                continue
            elif menu_about_rect.collidepoint(mouse_pos):
                active_menu = None
                show_about_window()
                continue

            if mouse_pos[1] < MENU_BAR_HEIGHT or (active_menu and mouse_pos[0] > menu_settings_rect.x + 280):
                active_menu = None

            if event.button == 1:  # Sol Tık İşlemleri
                if mouse_pos[0] < SIDEBAR_WIDTH and mouse_pos[1] > MENU_BAR_HEIGHT:
                    for i, name in enumerate(COMPONENTS):
                        rect = pygame.Rect(12, MENU_BAR_HEIGHT + 15 + i * (COMPONENT_BUTTON_HEIGHT + 12), SIDEBAR_WIDTH - 24, COMPONENT_BUTTON_HEIGHT)
                        if rect.collidepoint(mouse_pos):
                            selected_component = name
                            break
                    continue

                if mouse_pos[1] < MENU_BAR_HEIGHT: continue

                for s in switches:
                    if s.is_clicked(mouse_pos): s.toggle()

                for c in gates + switches + leds:
                    if c.is_clicked(mouse_pos): dragging_component = c

                slot_clicked = False
                for c in gates + switches + leds:
                    slot = c.get_slot_clicked(mouse_pos) if hasattr(c, "get_slot_clicked") else None
                    if slot:
                        slot_clicked = True
                        if current_wire is None:
                            current_wire = MyWire(c, slot)
                            if not hasattr(current_wire, 'points') or not current_wire.points:
                                current_wire.points = [mouse_pos]
                        else:
                            current_wire.end_comp = c
                            current_wire.end_slot = slot
                            wires.append(current_wire)
                            current_wire = None
                        break

                if current_wire and not slot_clicked and mouse_pos[0] > SIDEBAR_WIDTH:
                    if hasattr(current_wire, 'add_point'):
                        current_wire.add_point(mouse_pos)
                    elif hasattr(current_wire, 'points'):
                        if len(current_wire.points) == 0 or (mouse_pos[0] - current_wire.points[-1][0])**2 + (mouse_pos[1] - current_wire.points[-1][1])**2 > 25:
                            current_wire.points.append(mouse_pos)

                if selected_component and mouse_pos[0] > SIDEBAR_WIDTH and mouse_pos[1] > MENU_BAR_HEIGHT:
                    if selected_component in ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"]:
                        gates.append(MyGate(mouse_pos[0], mouse_pos[1], selected_component))
                    elif selected_component == "Switch":
                        switches.append(MySwitch(mouse_pos[0], mouse_pos[1]))
                    elif selected_component == "LED":
                        leds.append(MyLight(mouse_pos[0], mouse_pos[1]))
                    selected_component = None

            elif event.button == 3:
                wire_removed = False
                for w in wires:
                    if hasattr(w, 'is_clicked') and w.is_clicked(mouse_pos):
                        wires.remove(w)
                        wire_removed = True
                        break
                
                if not wire_removed:
                    for comp_list in [gates, switches, leds]:
                        for c in comp_list:
                            if c.is_clicked(mouse_pos):
                                wires[:] = [w for w in wires if w.start_comp != c and w.end_comp != c]
                                comp_list.remove(c)
                                break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: dragging_component = None

        elif event.type == pygame.MOUSEMOTION:
            if dragging_component:
                dx, dy = event.rel  # Farenin bağıntılı hareket miktarı
                
                nx = max(SIDEBAR_WIDTH + 25, min(WIDTH - 25, dragging_component.x + dx))
                ny = max(MENU_BAR_HEIGHT + 25, min(HEIGHT - 25, dragging_component.y + dy))
                
                real_dx = nx - dragging_component.x
                real_dy = ny - dragging_component.y
                
                dragging_component.x = nx
                dragging_component.y = ny
                
                # Dahili güncelleyicileri tetikle
                for m in ["_update_slots", "update_slots", "update"]:
                    if hasattr(dragging_component, m): getattr(dragging_component, m)()
                
                for attr_name in dir(dragging_component):
                    try:
                        attr = getattr(dragging_component, attr_name)
                        if isinstance(attr, pygame.Rect):
                            attr.x += real_dx
                            attr.y += real_dy
                        elif isinstance(attr, list):
                            for item in attr:
                                if isinstance(item, pygame.Rect):
                                    item.x += real_dx
                                    item.y += real_dy
                                elif hasattr(item, 'rect') and isinstance(item.rect, pygame.Rect):
                                    item.rect.x += real_dx
                                    item.rect.y += real_dy
                    except Exception:
                        pass

    for gate in gates:
        inputs = []
        for w in wires:
            if w.end_comp == gate:
                if hasattr(w.start_comp, "state"): inputs.append(w.start_comp.state)
        try:
            gate.calculate(inputs)
        except Exception:
            pass

    for led in leds:
        for w in wires:
            if w.end_comp == led:
                if hasattr(w.start_comp, "state"): led.state = w.start_comp.state

    for w in wires:
        if hasattr(w, 'transfer_signal'): w.transfer_signal()

    pygame.display.flip()
    clock.tick(60)

save_config()

pygame.quit()
sys.exit()
