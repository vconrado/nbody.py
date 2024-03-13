import numpy as np  
from tkinter import * 

tk = Tk()  # Cria a janela principal da interface gráfica.
tk.resizable(0, 0)  # Desabilita a possibilidade de redimensionar a janela.
W, H = 800, 800  # Define a largura e altura da janela.
COLOR = 'blue'  # Define a cor dos corpos celestes na simulação.
pos_scale = 200  # Fator de escala para a posição dos corpos no canvas.
canvas = Canvas(tk, width=W, height=H)  # Cria um canvas (área de desenho) na janela principal.
canvas.pack()  # Empacota o canvas na janela, tornando-o visível.

class Body:
    """
    Representa um corpo celeste com posição, velocidade, aceleração e massa.

    Attributes:
        pos (np.array): Posição do corpo no espaço bidimensional.
        vel (np.array): Velocidade do corpo.
        acc (np.array): Aceleração do corpo.
        mass (float): Massa do corpo.
        obj (int): Identificador do objeto gráfico associado no canvas.
    """
    def __init__(self, pos, vel, acc, mass):
        """
        Inicializa uma instância de Body.

        Args:
            pos (np.array): Posição inicial [x, y].
            vel (np.array): Velocidade inicial [vx, vy].
            acc (np.array): Aceleração inicial [ax, ay].
            mass (float): Massa do corpo.
        """
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.mass = mass
        self.obj = None
        
    def __repr__(self):
        """
        Representação textual da instância.
        
        Returns:
            str: Representação em string do corpo.
        """
        return self.__str__()
    
    def __str__(self):
        """
        Fornece uma representação em string da instância para facilitar a leitura.

        Returns:
            str: String formatada representando o corpo.
        """
        return f"Body({self.pos}, {self.vel}, {self.acc}, {self.mass})"
    
    def draw(self):
        """
        Desenha o corpo no canvas, representado por um círculo.
        """
        size = (self.mass**0.5) / pos_scale  # Calcula o tamanho visual do corpo.
        
        # Define as coordenadas do círculo.
        x0 = self.pos[0] - size / 2
        y0 = self.pos[1] - size / 2
        xf = self.pos[0] + size / 2
        yf = self.pos[1] + size / 2

        # Aplica escala e centraliza no canvas.
        x0 *= pos_scale
        y0 *= pos_scale
        xf *= pos_scale
        yf *= pos_scale
        x0 += W / 2
        y0 += H / 2
        xf += W / 2
        yf += H / 2

        if not self.obj:
            # Cria um círculo se ainda não existir.
            self.obj = canvas.create_oval(x0, y0, xf, yf, fill=COLOR)
        else:
            # Move o círculo existente para a nova posição.
            canvas.moveto(self.obj, x0, y0)
    
    def remove_obj(self):
        """
        Remove o objeto gráfico do canvas, se existir.
        """
        if self.obj:
            canvas.delete(self.obj)
            self.obj = None

    def __del__(self):
        """
        Garante a remoção do objeto gráfico ao deletar a instância.
        """
        self.remove_obj()

    def calc_acc(self, others, G):
        """
        Calcula a aceleração do corpo devido à interação gravitacional com outros corpos.

        Args:
            others (list): Lista de outros corpos no sistema.
            G (float): Constante gravitacional.
        """
        ax = 0.0
        ay = 0.0
        softening = 0.1  # Termo para evitar divisão por zero em distâncias muito pequenas.
        for o in others:
            dx = o.pos[0] - self.pos[0]
            dy = o.pos[1] - self.pos[1]
            inv_r3 = (dx**2 + dy**2 + softening**2)**(-1.5)
            ax += G * dx * inv_r3 * o.mass
            ay += G * dy * inv_r3 * o.mass
        
        self.acc = np.array([ax, ay])

def gen_data_rand(n):
    """
    Gera `n` corpos com propriedades aleatórias.

    Args:
        n (int): Número de corpos a serem gerados.

    Returns:
        list: Lista de instâncias de `Body`.
    """
    l = []
    for _ in range(n):
        l.append(
            Body(4 * (np.random.rand(2) - 0.5), 
                 2 * (np.random.rand(2) - 0.5),
                 np.zeros(2),
                 500 * np.random.rand(1)[0])
        )
    return l

def gen_data_test():
    """
    Gera uma lista de corpos para testes com propriedades predefinidas.

    Returns:
        list: Lista de instâncias de `Body` para testes.
    """
    l = []
    l.append(Body(np.zeros(2), np.zeros(2), np.zeros(2), 1000.))
    l.append(Body(np.array([0., 0.5]), np.zeros(2), np.zeros(2), 500.))
    l.append(Body(np.array([0., -0.5]), np.zeros(2), np.zeros(2), 500.))
    return l

def integrate(bs, G, dt):
    """
    Realiza um passo de integração no tempo para atualizar posição e velocidade dos corpos.

    Args:
        bs (list): Lista de corpos a serem integrados.
        G (float): Constante gravitacional.
        dt (float): Passo de tempo para a integração.
    """
    N = len(bs)
    for i in range(N):
        bs[i].vel += bs[i].acc * dt / 2
        bs[i].pos += bs[i].vel * dt

        bs[i].calc_acc(bs, G)
        
        bs[i].vel += bs[i].acc * dt / 2

bs = gen_data_rand(50)  # Gera 50 corpos com dados aleatórios.
G = 0.001  # Constante gravitacional para a simulação.
dt = 1 / 1000  # Passo de tempo para a integração.

def main_loop():
    """
    Função principal que executa a simulação, atualizando estados e redesenhando os corpos.
    """
    integrate(bs, G, dt)  # Integra as equações do movimento.

    # Desenha cada corpo no canvas.
    for b in bs:
        b.draw()    
    
    tk.after(1, main_loop)  # Agenda a próxima execução do loop principal após 1ms.

tk.after(1, main_loop)  # Inicia o loop principal.
tk.mainloop()  # Entra no loop de eventos do tkinter, mantendo a janela aberta.