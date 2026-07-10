import pygame
import random

# Orijinal Renk Paleti
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
GRAY = (180, 180, 180)
YELLOW = (255, 255, 100)
WIRE_COLORS = [(0, 0, 0), (50, 50, 200), (200, 50, 50)]

# -----------------------------
# Mantık Kapıları Sınıfı
# -----------------------------
class MyGate:
    def __init__(self, x, y, gate_type):
        self.x = x
        self.y = y
        self.width = 80   
        self.height = 50  
        self.gate_type = gate_type  
        self.type = gate_type
        self.state = False
        self.color = BLUE
        self._update_slots()

    def _update_slots(self):
        if self.type == "NOT":
            self.inputs = [(self.x - 10, self.y + self.height // 2)]
        else:
            self.inputs = [
                (self.x - 10, self.y + 15), 
                (self.x - 10, self.y + self.height - 15)
            ]
        self.output = (self.x + self.width + 10, self.y + self.height // 2)

    def update_slots(self):
        self._update_slots()

    def draw(self, surface):
        # Gövde rengi sabit tutuldu
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=12)
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2, border_radius=12)
        
        font = pygame.font.SysFont("Arial", 18, bold=True)
        text = font.render(self.type, True, WHITE)
        surface.blit(text, (self.x + (self.width - text.get_width()) // 2, self.y + (self.height - text.get_height()) // 2))

        for slot in self.inputs:
            pygame.draw.circle(surface, BLACK, slot, 5)
            
        out_color = GREEN if self.state else RED
        pygame.draw.circle(surface, out_color, self.output, 6)
        pygame.draw.circle(surface, BLACK, self.output, 6, 1)

    def calculate(self, input_states):
        padded = list(input_states)
        if self.type == "NOT":
            val = padded[0] if padded else False
            self.state = not val
        else:
            while len(padded) < 2:
                padded.append(False)
            
            if self.type == "AND":     self.state = all(padded)
            elif self.type == "OR":    self.state = any(padded)
            elif self.type == "NAND":  self.state = not all(padded)
            elif self.type == "NOR":   self.state = not any(padded)
            elif self.type == "XOR":   self.state = padded[0] != padded[1]
            elif self.type == "XNOR":  self.state = padded[0] == padded[1]
            
        return self.state

    def is_clicked(self, pos):
        x, y = pos
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    def get_slot_clicked(self, pos):
        # Tıklama konforu için algılama alanı genişletildi (Mesafe karesi: 144)
        for slot in self.inputs:
            if (pos[0] - slot[0])**2 + (pos[1] - slot[1])**2 < 144:
                return slot
        if (pos[0] - self.output[0])**2 + (pos[1] - self.output[1])**2 < 144:
            return self.output
        return None

# -----------------------------
# Anahtar (Switch) Sınıfı
# -----------------------------
class MySwitch:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 20
        self.state = False
        self._update_slots()

    def _update_slots(self):
        self.output = (self.x + self.width + 10, self.y + self.height // 2)

    def _update_slot(self): self._update_slots()
    def update_slots(self): self._update_slots()

    def toggle(self):
        self.state = not self.state

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 1, border_radius=10)
        
        color = GREEN if self.state else RED
        bx = self.x + self.width - 10 if self.state else self.x + 10
        pygame.draw.circle(surface, color, (bx, self.y + self.height // 2), 8)
        pygame.draw.circle(surface, BLACK, self.output, 5)

    def is_clicked(self, pos):
        x, y = pos
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    def get_slot_clicked(self, pos):
        if (pos[0] - self.output[0])**2 + (pos[1] - self.output[1])**2 < 144:
            return self.output
        return None

# -----------------------------
# LED (Işık) Sınıfı
# -----------------------------
class MyLight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.state = False
        self._update_slots()

    def _update_slots(self):
        self.inputs = [(self.x - 10, self.y + self.height // 2)]

    def _update_slot(self): self._update_slots()
    def update_slots(self): self._update_slots()

    def draw(self, surface):
        color = GREEN if self.state else GRAY
        pygame.draw.ellipse(surface, color, (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(surface, BLACK, (self.x, self.y, self.width, self.height), 1)
        pygame.draw.circle(surface, BLACK, self.inputs[0], 5)

    def is_clicked(self, pos):
        x, y = pos
        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    def get_slot_clicked(self, pos):
        if (pos[0] - self.inputs[0][0])**2 + (pos[1] - self.inputs[0][1])**2 < 144:
            return self.inputs[0]
        return None

# -----------------------------
# Kablo Sınıfı (Akıllı Slot Eşleşmeli)
# -----------------------------
class MyWire:
    def __init__(self, start_comp, start_slot, end_comp=None, end_slot=None, color=None):
        self._start_comp = start_comp
        self._end_comp = end_comp
        self.color = color if color else random.choice(WIRE_COLORS)
        
        self._start_raw = start_slot
        self._end_raw = end_slot
        
        self._start_type = "output"
        self._start_idx = 0
        self._end_type = None
        self._end_idx = 0
        
        self.points = [start_slot]
        
        # Bağlantı haritasını ilk kurulumda tara
        self._update_start_connection()
        self._update_end_connection()

    def _update_start_connection(self):
        if self._start_comp and self._start_raw:
            if hasattr(self._start_comp, 'inputs') and self._start_raw in self._start_comp.inputs:
                self._start_type = "input"
                self._start_idx = self._start_comp.inputs.index(self._start_raw)
            else:
                self._start_type = "output"

    def _update_end_connection(self):
        if self._end_comp and self._end_raw:
            if hasattr(self._end_comp, 'inputs') and self._end_raw in self._end_comp.inputs:
                self._end_type = "input"
                self._end_idx = self._end_comp.inputs.index(self._end_raw)
            elif hasattr(self._end_comp, 'output') and self._end_raw == self._end_comp.output:
                self._end_type = "output"

    @property
    def start_comp(self): return self._start_comp
    @start_comp.setter
    def start_comp(self, val):
        self._start_comp = val
        self._update_start_connection()

    @property
    def start_slot(self):
        if self._start_comp:
            if self._start_type == "output" and hasattr(self._start_comp, 'output'):
                return self._start_comp.output
            elif self._start_type == "input" and hasattr(self._start_comp, 'inputs') and self._start_idx < len(self._start_comp.inputs):
                return self._start_comp.inputs[self._start_idx]
        return self._start_raw
    
    @start_slot.setter
    def start_slot(self, val):
        self._start_raw = val
        self._update_start_connection()

    @property
    def end_comp(self): return self._end_comp
    @end_comp.setter
    def end_comp(self, val):
        self._end_comp = val
        self._update_end_connection()

    @property
    def end_slot(self):
        if self._end_comp:
            if self._end_type == "output" and hasattr(self._end_comp, 'output'):
                return self._end_comp.output
            elif self._end_type == "input" and hasattr(self._end_comp, 'inputs') and self._end_idx < len(self._end_comp.inputs):
                return self._end_comp.inputs[self._end_idx]
        return self._end_raw
    
    @end_slot.setter
    def end_slot(self, val):
        self._end_raw = val
        self._update_end_connection()

    def add_point(self, pos):
        self.points.append(pos)

    def draw(self, surface):
        if self.points:
            self.points[0] = self.start_slot  
            
        pts = self.points[:]
        if self.end_slot:
            pts.append(self.end_slot)  
            
        if len(pts) > 1:
            pygame.draw.lines(surface, self.color, False, pts, 3)

    def transfer_signal(self):
        if self.end_comp and hasattr(self.end_comp, 'state'):
            if not isinstance(self.end_comp, MyGate):
                self.end_comp.state = self.start_comp.state

    def is_clicked(self, pos):
        pts = self.points[:]
        if self.end_slot:
            pts.append(self.end_slot)
            
        for i in range(len(pts) - 1):
            start = pts[i]
            end = pts[i+1]
            
            denom = ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
            if denom == 0: continue
            
            dist = abs((end[1] - start[1])*pos[0] - (end[0] - start[0])*pos[1] + end[0]*start[1] - end[1]*start[0]) / denom
            
            if dist < 6:
                min_x, max_x = min(start[0], end[0]) - 5, max(start[0], end[0]) + 5
                min_y, max_y = min(start[1], end[1]) - 5, max(start[1], end[1]) + 5
                if min_x <= pos[0] <= max_x and min_y <= pos[1] <= max_y:
                    return True
        return False
