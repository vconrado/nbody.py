import numpy as np
from tkinter import *

tk = Tk()
tk.resizable(0, 0)
W, H = 800,800
COLOR='blue'
pos_scale = 200
canvas = Canvas(tk, width=W, height=H)
canvas.pack()

class Body:
    def __init__(self, pos, vel, acc, mass):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.mass = mass
        self.obj = None
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return f"Body({self.pos}, {self.vel}, {self.acc}, {self.mass}"
    
    def draw(self):
        size =  (self.mass**0.5)/pos_scale
        
        x0 = self.pos[0] - size/2
        y0 = self.pos[1] - size/2

        xf = self.pos[0] + size/2
        yf = self.pos[1] + size/2

        # scale
        x0 *= pos_scale
        y0 *= pos_scale
        xf *= pos_scale
        yf *= pos_scale

        # center
        x0 += W/2
        y0 += H/2
        xf += W/2
        yf += H/2

        if not self.obj:
            self.obj = canvas.create_oval(x0, y0, xf, yf, fill=COLOR)
        else:
            canvas.moveto(self.obj, x0, y0)

    
    def remove_obj(self):
        canvas.delete(self.obj)
        self.obj = None

    def __del__(self):
        self.remove_obj()

    def calc_acc(self, others, G):
        ax = 0.
        ay = 0.
        softening = 0.1
        for o in others:
            dx = o.pos[0] - self.pos[0]
            dy = o.pos[1] - self.pos[1]
            inv_r3 = (dx**2 + dy**2 + softening**2)**(-1.5)
            ax += G * dx * inv_r3 * o.mass
            ay += G * dy * inv_r3 * o.mass
        
        self.acc = np.array([ax, ay])


def gen_data_rand(n):
    l = list()
    for _ in range(n):
        l.append(
            Body(4*(np.random.rand(2)-0.5), 
                 2*(np.random.rand(2)-0.5),
                 np.zeros(2),
                 500*np.random.rand(1)[0]
                )
        )
    return l


def gen_data_test():
        l = list()
        l.append(Body( np.zeros(2), 
                np.zeros(2),
                np.zeros(2),
                 1000.
                ))

        l.append(Body(np.array([0.,0.5]), 
                 np.zeros(2),
                 np.zeros(2),
                 500.
                ))

        l.append(Body(np.array([0.,-0.5]), 
                 np.zeros(2),
                 np.zeros(2),
                 500.
                ))

        return l


def integrate(bs, G, dt):
    N = len(bs)
    for i in range(N):
        bs[i].vel += bs[i].acc * dt/2
        bs[i].pos += bs[i].vel * dt

        bs[i].calc_acc(bs, G)
        
        bs[i].vel += bs[i].acc * dt/2



bs = gen_data_rand(50)
G = 0.001
dt = 1/1000

def main_loop():
    
    integrate(bs, G, dt)

    # draw
    for b in bs:
        b.draw()    
    
    tk.after(1, main_loop)


tk.after(1, main_loop)
tk.mainloop()

    
