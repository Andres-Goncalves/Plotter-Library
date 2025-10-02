from machine import Pin
from utime import sleep_ms
import array
import math

#Constantes
#Rotación
AntiHorario = [
    [1,1,0,0],
    [0,1,1,0],
    [0,0,1,1],
    [1,0,0,1]
    ]
Horario = [
    [0,0,1,1],
    [0,1,1,0],
    [1,1,0,0],
    [1,0,0,1]
    ]

#Limites
XMAXIMA = 4600
YMAXIMA = 4600

#conversor

#  x - 2650 mm
# x2 - 4600 u
# x2 = x * 4600 / 2650
PROPORCIONX = 4600 / 2650

#  y - 2650 mm
# y2 - 4600 u
# x2 = x * 4600 / 2150
PROPORCIONY = 4600 / 2150

#reiniciar memoria
try:
    open('trazado.txt', 'w').close()
except:
    print("archivo trazado no encontrado")
    
class Impresora:

    #Posisión
    X = 0
    Y = 0

    #Marcador
    Modo = 0
    # 0 = Descanso
    # 1 = Arriba/espera
    # 2 = Abajo/escritura
    
    #-----------------------------------------------------------------------------
    def __init__(self,
                 MarcoIN1=5, MarcoIN2=4, MarcoIN3=3, MarcoIN4=2,
                 CarroIN1=9, CarroIN2=8, CarroIN3=7, CarroIN4=6,
                 MarcadorIN1=13, MarcadorIN2=12, MarcadorIN3=11, MarcadorIN4=10):
        #Motores/ejes
        self.Marco = [
             Pin(MarcoIN1, Pin.OUT), # IN1
             Pin(MarcoIN2, Pin.OUT), # IN2
             Pin(MarcoIN3, Pin.OUT), # IN3
             Pin(MarcoIN4, Pin.OUT)  # IN4
             ]

        self.Carro = [
             Pin(CarroIN1, Pin.OUT), # IN1
             Pin(CarroIN2, Pin.OUT), # IN2
             Pin(CarroIN3, Pin.OUT), # IN3
             Pin(CarroIN4, Pin.OUT)  # IN4
             ]

        self.Marcador = [
             Pin(MarcadorIN1, Pin.OUT), # IN1
             Pin(MarcadorIN2, Pin.OUT), # IN2
             Pin(MarcadorIN3, Pin.OUT), # IN3
             Pin(MarcadorIN4, Pin.OUT)  # IN4
             ]
    #------------------------------------------------------------------------------
    
    #conversor---------------------
    def convertirX(self, x):
        return int(x * PROPORCIONX)

    def convertirY(self, y):
        return int(y * PROPORCIONY)
    #------------------------------
    
    #Marcador, cambio de modo---------------------------
    def modo(self, k):
        if k == 2:
            if self.Modo == 1:
                self.bajar()
            elif self.Modo == 0:
                self.preparado()
                self.bajar()
        elif k == 1:
            if self.Modo == 2:
                self.subir()
            elif self.Modo == 0:
                self.preparado()
        elif k == 0:
            if self.Modo == 2:
                self.subir()
                self.descanso()
            elif self.Modo == 1:
                self.descanso()
    #--------------------------------------------------
    
    #--------------------------------------------------------------------------------------------------
    def descanso(self):
        if self.Modo == 1:
            self.Modo = 0 
            for j in range(40):
                for paso in AntiHorario:
                    for i in range(len(self.Marcador)):
                        self.Marcador[i].value(paso[i])
                    sleep_ms(10)
        else:
            print("La impresora no se encuentra en el modo correcto para pasar al modo de descanso")
                
    def preparado(self):
        if self.Modo == 0:
            self.Modo = 1 
            for j in range(40):
                for paso in Horario:
                    for i in range(len(self.Marcador)):
                        self.Marcador[i].value(paso[i])
                    sleep_ms(10)
        else:
            print("La impresora no se encuentra en el modo correcto para pasar al modo de espera")
    #--------------------------------------------------------------------------------------------------

    #--------------------------------------------------------------------------------------------------
    def subir(self):
        if self.Modo == 2:
            self.Modo = 1 
            for j in range(24):
                for paso in AntiHorario:
                    for i in range(len(self.Marcador)):
                        self.Marcador[i].value(paso[i])
                    sleep_ms(10)
        else:
            print("La impresora no se encuentra en el modo correcto para pasar al modo de espera")
                
    def bajar(self):
        if self.Modo == 1:
            self.Modo = 2 
            for j in range(24):
                for paso in Horario:
                    for i in range(len(self.Marcador)):
                        self.Marcador[i].value(paso[i])
                    sleep_ms(10)
        else:
            print("La impresora no se encuentra en el modo correcto para pasar al modo de escritura")
    #--------------------------------------------------------------------------------------------------
            
    #Marco-------------------------------------------
    def ejeXmm(self, k):
        self.ejeX(self.convertirX(k))
            
    def ejeX(self, k):
        if k > 0:
            self.extender(k)
        elif k < 0:
            self.retraer(-k)

    def extender(self, k):
        if k + self.X > XMAXIMA:
            k = XMAXIMA - self.X
            print("Limite máximo X alcanzado")
        self.X += k
        for j in range(k):
            for paso in AntiHorario:
                for i in range(len(self.Marco)):
                    self.Marco[i].value(paso[i])
                sleep_ms(10)
            
    def retraer(self, k):
        if self.X - k < 0:
            k = self.X
            print("Limite mínimo X alcanzado")
        self.X -= k
        for j in range(k):
            for paso in Horario:
                for i in range(len(self.Marco)):
                    self.Marco[i].value(paso[i])
                sleep_ms(10)
    #------------------------------------------------
                
    #Carro-------------------------------------------
    def ejeYmm(self, k):
        self.ejeY(self.convertirY(k))
                
    def ejeY(self, k):
        if k > 0:
            self.alejar(k)
        elif k < 0:
            self.acercar(-k)

    def alejar(self, k):
        if k + self.Y > YMAXIMA:
            k = YMAXIMA - self.Y
            print("Limite máximo Y alcanzado")
        self.Y += k
        for j in range(k):
            for paso in AntiHorario:
                for i in range(len(self.Carro)):
                    self.Carro[i].value(paso[i])
                sleep_ms(2)
            
    def acercar(self, k):
        if self.Y - k < 0:
            k = self.Y
            print("Limite mínimo Y alcanzado")
        self.Y -= k
        for j in range(k):
            for paso in Horario:
                for i in range(len(self.Carro)):
                    self.Carro[i].value(paso[i])
                sleep_ms(2)
    #------------------------------------------------

    #Funsiones conjuntas      

    def signo(self, k):
        if k > 0:
            return 1
        elif k < 0:
            return -1
        else:
            return 0
    
    #Dibujar-----------------------------------------------------------
    def trazar(self, lista): 
        self.modo(1)
        self.mover_a_punto(self.convertirX(lista[0][0]),self.convertirY(lista[0][1]))
        cont = len(lista)
        
        for punto in lista:
            self.modo(punto[2])
            self.mover_a_punto(self.convertirX(punto[0]),self.convertirY(punto[1]))
            #print(cont)
            cont -= 1
        
        self.modo(1)
    
    def trazar_archivo(self): 
        self.modo(1)
        try:
            archivo = open("trazado.txt", "r")
            try: 
                linea = archivo.readline().split(",")
                self.mover_a_punto(self.convertirX(int(linea[0])),self.convertirY(int(linea[1])))
                
                linea = archivo.readline().split(",")
                while linea:
                    self.modo(int(linea[2]))
                    self.mover_a_punto(self.convertirX(int(linea[0])),self.convertirY(int(linea[1])))
                    linea = archivo.readline().split(",")
            except Exception as ex:
                print("error al dibujar:", ex)
            finally:
                archivo.close()
        except Exception as ex:
            print("error al abrir el archivo:", ex)
        
        self.modo(1)
    #------------------------------------------------------------------
           
    #Dibujar-----------------------------------------------------------
    def mover_a_punto(self, x, y):
        self.mover_en_direccion((x-self.X), (y-self.Y))
    #-------------------------------
        
    def mover_en_direccion(self, x, y):
        ax = abs(x)
        ay = abs(y)
        sx = self.signo(x)
        sy = self.signo(y)
        
        if x == 0:
            self.ejeY(y)
        elif y == 0:
            self.ejeX(x)
        elif ax > ay:
            j = ay
            i = int(ax / (ay+1))
            k = ax % (ay+1)
            print("x:",i,"k:",k,"y:",j)
            self.diagonalX(i,k,j,sx,sy)
        elif ax < ay:
            i = ax
            j = int(ay / (ax+1))
            k = ay % (ax+1)
            print("x:",i,"y:",j,"k:",k)
            self.diagonalY(i,j,k,sx,sy)
        else:
            self.diagonal(x,sx,sy)
    #-------------------------------

    def diagonal(self, k, sx, sy):
        for j in range(k):
            self.ejeX(sx)
            self.ejeY(sy)
    #-------------------------------

    def diagonalX(self, i, k, j, sx, sy):
        
        aux = 0
        cambio = 0
        proporcion = 1
        
        if k == 0:
            aux = [i] * (j+1)
        else:
            if k <= (j+1)/2:
                aux = [i] * (j+1)
                cambio = 1
                proporcion = (j+1)/k
            else:
                aux = [i+1] * (j+1)
                cambio = -1
                proporcion = (j+1)/(j+1-k)
                k = j+1-k
            
        i2 = array.array('i',aux)

        for l in range(k):
            if k <= 0:
                break
                
            i2[int((l+1)*proporcion)-1] += cambio
            k -= 1
        
        suma = 0
        for l in range(j+1):
            self.ejeX(i2[l]*sx)
            if not l == 0:
                self.ejeY(sy)
                
            suma += i2[l] 
        print(i2, suma*sx, j*sy)
    #-------------------------------

    def diagonalY(self, i, j, k, sx, sy):
        
        aux = 0
        cambio = 0
        proporcion = 1
        
        if k == 0:
            aux = [j] * (i+1)
        else:
            if k <= (i+1)/2:
                aux = [j] * (i+1)
                cambio = 1
                proporcion = (i+1)/k
            else:
                aux = [j+1] * (i+1)
                cambio = -1
                proporcion = (i+1)/(i+1-k)
                k = i+1-k
            
        j2 = array.array('i',aux)

        for l in range(k):
            if k <= 0:
                break
                
            j2[int((l+1)*proporcion)-1] += cambio
            k -= 1
        
        suma = 0
        for l in range(i+1):
            self.ejeY(j2[l]*sy)
            if not l == 0:
                self.ejeX(sx)
                
            suma += j2[l] 
        print(i*sx, suma*sy, j2)
    #------------------------------------------------------------------
              
    #Reset-------------------------------------------------------------
    def inicio(self):

        if self.Modo == 2:
            self.subir()
            self.descanso()
        elif self.Modo == 1:
            self.descanso()

        k = 0
        
        if self.X < self.Y:
            k = self.X
        else:
            k = self.Y
        
        for j in range(k):
            for paso in Horario:
                for i in range(len(self.Marco)):
                    self.Marco[i].value(paso[i])
                for i in range(len(self.Carro)):
                    self.Carro[i].value(paso[i])
                sleep_ms(5)
            if self.X > 0:
                self.X -= 1
            if self.Y > 0:
                self.Y -= 1
        
        if self.X > 0:
            k = self.X
            for j in range(k):
                for paso in Horario:
                    for i in range(len(self.Marco)):
                        self.Marco[i].value(paso[i])
                    sleep_ms(5)
                self.X -= 1
        elif self.Y > 0:
            k = self.Y
            for j in range(k):
                for paso in Horario:
                    for i in range(len(self.Carro)):
                        self.Carro[i].value(paso[i])
                    sleep_ms(2)
                self.Y -= 1
    #------------------------------------------------------------------
    def dibujar_numero(self, num, x, y):
        val = []
        print(num)
        num = int(num)
        print(num)
        sig = self.signo(num)
        num = abs(num)
        
        if sig == -1:
            lista = [[x, y+75, 2], [x+75, y+75, 2]]
            print("-", lista)
            self.trazar(lista)
            x += 125
        
        for i in range(len(str(num))):
            val.insert(0, num % 10)
            num = num//10
            a = math.pi/180
        
        for i in val:
            if i == 0:
                lista = []
                c = 180
                r = 45
                
                while c >= 0:
                    x1 = (x + r) + r * math.cos(c*a)
                    y1 = (y + r) + r * math.sin(c*a) * -1
                    lista.append([int(x1),int(y1),2])
                    c -= 1
                    
                while c >= -180:
                    x1 = (x + r) + r * math.cos(c*a)
                    y1 = (y + r+60) + r * math.sin(c*a) * -1
                    lista.append([int(x1),int(y1),2])
                    c -= 1
                    
                lista.append([int(x),int(y+r),2])
                print(i, lista)
                self.trazar(lista)
                x += r*2
            #-----------------------------
                
            elif i == 1:
                lista = [[x, y+50, 2], [x+50, y, 2], [x+50, y+150, 2]]
                print(i, lista)
                self.trazar(lista)
                x += 50
            #-----------------------------
                
            elif i == 2:
                
                lista = []
                c = 180
                r = 45
                
                while c > -53:
                    x1 = (x + r) + r * math.cos(c*a)
                    y1 = (y + r) + r * math.sin(c*a) * -1
                    lista.append([int(x1),int(y1),2])
                    c -= 1
                    
                lista.append([x, y+150, 2])
                lista.append([x+r*2, y+150, 2])
                print(i, lista)
                self.trazar(lista)
                x += 90
            #-----------------------------
                
            elif i == 3:
                lista = []
                c = 168
                r = 40
                
                while c >= -90:
                    x1 = (x + r) + r * math.cos(c*a)
                    y1 = (y + r) + r * math.sin(c*a) * -1
                    lista.append([int(x1),int(y1),2])
                    c -= 1
                
                c = 90
                while c >= -180:
                    x1 = (x + r) + r * math.cos(c*a)
                    y1 = (y + r+70) + r * math.sin(c*a) * -1
                    lista.append([int(x1),int(y1),2])
                    c -= 1
                    
                print(i, lista)
                self.trazar(lista)
                x += int(r*15/8)
            #-----------------------------
                
            elif i == 4:
                lista = [[x, y, 2], [x, y+75, 2], [x+75, y+75, 2], [x+75, y, 1], [x+75, y+150, 2]]
                print(i, lista)
                self.trazar(lista)
                x += 75
            #-----------------------------
                
            elif i == 5:
                lista = [[x+80, y, 2], [x, y, 2], [x, y+78, 2]]
                
                c = 143
                r = 45
                
                while c >= -143:
                    x1 = (x + r) + r * math.cos(c*a)
                    y1 = (y + r+60) + r * math.sin(c*a) * -1
                    lista.append([int(x1),int(y1),2])
                    c -= 1
                    
                print(i, lista)
                self.trazar(lista)
                x += 80
            #-----------------------------
                
            elif i == 6:
                lista = []
                c = 180
                r = 45
                
                while c >= -180:
                    x1 = (x + r) + r * math.cos(c*a)
                    y1 = (y + r+60) + r * math.sin(c*a) * -1
                    lista.append([int(x1),int(y1),2])
                    c -= 1
                
                while c >= -320:
                    x1 = (x + r) + r * math.cos(c*a)
                    y1 = (y + r) + r * math.sin(c*a) * -1
                    lista.append([int(x1),int(y1),2])
                    c -= 1
                    
                print(i, lista)
                self.trazar(lista)
                x += r*2
            #-----------------------------
                
            elif i == 7:
                lista = [[x, y, 2], [x+75, y, 2], [x+25, y+150, 2]]
                
                print(i, lista)
                self.trazar(lista)
                x += 75
            #-----------------------------
                
            elif i == 8:
                lista = []
                c = 241
                r = 40
                
                while c >= -61:
                    x1 = (x + r) + r * math.cos(c*a)
                    y1 = (y + r) + r * math.sin(c*a) * -1
                    lista.append([int(x1),int(y1),2])
                    c -= 1
                    
                c = 61
                while c >= -299:
                    x1 = (x + r) + r * math.cos(c*a)
                    y1 = (y + r+70) + r * math.sin(c*a) * -1
                    lista.append([int(x1),int(y1),2])
                    c -= 1
                    
                print(i, lista)
                self.trazar(lista)
                x += r*2
            #-----------------------------
                
            elif i == 9:
                lista = []
                c = 360
                r = 45
                
                while c >= 0:
                    x1 = (x + r) + r * math.cos(c*a)
                    y1 = (y + r) + r * math.sin(c*a) * -1
                    lista.append([int(x1),int(y1),2])
                    c -= 1
                
                while c >= -127:
                    x1 = (x + r) + r * math.cos(c*a)
                    y1 = (y + r+60) + r * math.sin(c*a) * -1
                    lista.append([int(x1),int(y1),2])
                    c -= 1
                    
                print(i, lista)
                self.trazar(lista)
                x += r*2
            #-----------------------------
        
            x += 50
        #-----------------------------
            
    def espacio_numero(self, num):
        res = 0
        num = int(num)
        print(num)
        
        sig = self.signo(num)
        num = abs(num)
        
        if sig == -1:
            res += 125
            
        for i in range(len(str(num))):
            if not i == 0:
                res += 50
                
            val = num % 10
            num = num//10
            
            if val == 0:
                res += 90
                
            elif val == 1:
                res += 50
                
            elif val == 2:
                res += 90
                
            elif val == 3:
                res += int(40*15/8)
                
            elif val == 4:
                res += 75
                
            elif val == 5:
                res += 80
                
            elif val == 6:
                res += 90
                
            elif val == 7:
                res += 75
                
            elif val == 8:
                res += 80
                
            elif val == 9:
                res += 90
        
        res += 50
        
        return res
        
    def corazon(self, x, y, w, h):
        lista = []
        i = x
                   
        while i < w+x:
            x1 = i
            y1 = int((((2*((i-x)/w)**(2/3))+(-4*((i-x)/w)**2+4)**(1/2))/2)*-1*h+y)
            lista.append([x1, y1, 2])
            i += 1

        while i > x:
            x1 = i
            y1 = int((((2*((i-x)/w)**(2/3))-(-4*((i-x)/w)**2+4)**(1/2))/2)*-1*h+y)
            lista.append([x1, y1, 2])
            i -= 1

        i = len(lista)-1
        lista2 = []
        while i >= 0:
            lista2.append([int(x*2 - lista[i][0]), lista[i][1], lista[i][2]])
            i -= 1
        
        lista += lista2

        return lista

    def carta(self, x, y):
        
        try:
            archivo = open("trazado.txt", "w")
            lista = [[x, y, 2], [x+900, y, 2], [x+900, y+1400, 2], [x, y+1400, 2], [x, y, 2], [x+50, y+200, 1], [x+125, y+50, 2], [x+200, y+200, 2], [x+160, y+120, 1], [x+90, y+120, 2], [x+125, y+320, 1], [x+85, y+400, 2], [x+165, y+400, 2], [x+125, y+320, 2]]
            
            for i in lista:
                archivo.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + '\n')
                
            lista = []
            lista = self.corazon(x+125, y+260, 80, -60)
            
            for i in lista:
                archivo.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + '\n')
            
            lista = []
            lista = [[x+450, y+800, 1], [x+380, y+950, 2], [x+520, y+950, 2], [x+450, y+800, 2]]
            
            for i in lista:
                archivo.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + '\n')
            
            lista = []
            lista = self.corazon(x+450, y+620, 240, -180)
            
            for i in lista:
                archivo.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + '\n')
            
            lista = []
            lista = [[x+850, y+1200, 1], [x+775, y+1350, 2], [x+700, y+1200, 2], [x+740, y+1280, 1], [x+810, y+1280, 2], [x+775, y+1080, 1], [x+735, y+1000, 2], [x+815, y+1000, 2], [x+775, y+1080, 2]]
            
            for i in lista:
                archivo.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + '\n')
            
            lista = []
            lista = self.corazon(x+775, y+1140, 80, 60)
            
            for i in lista:
                archivo.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]) + '\n')
            
            archivo.close()
            
        except:
            print("No se pudo sobrescribir el archivo")
        
        self.trazar_archivo()
        
        self.inicio()

    def dibujar_grafica(self, a, b, c, d, x1, x2):
        
        ancho_pantalla = 2650
        alto_pantalla = 2150
        
        dx = x2 - x1
        pdx = dx / ancho_pantalla
        
        aux = a*x1**3 + b*x1**2 + c*x1 + d
        direccion = 0
        inflex = []
        n = 1
        while n <= ancho_pantalla:
            xn = x1 + n * pdx
            y = a*xn**3 + b*xn**2 + c*xn + d
            
            if direccion == 0:
                direccion = self.signo(aux - y)
            elif not direccion == self.signo(aux - y):
                direccion = self.signo(aux - y)
                inflex.append(xn)
                
            aux = y
            n+=1
        
        print(inflex)
        
        ymax = 0
        ymin = ymax
        
        if inflex == []:
            ymin = x1
            ymax = x2
        elif len(inflex) == 1:
            ymax = a*inflex[0]**3 + b*inflex[0]**2 + c*inflex[0] + d
            ymin = ymax - 0.5*dx
        else:
            ymax = a*inflex[0]**3 + b*inflex[0]**2 + c*inflex[0] + d
            ymin = ymax
            for i in inflex:
                y = a*i**3 + b*i**2 + c*i + d
                if y > ymax:
                    ymax = y
                if y < ymin:
                    ymin = y
            
        print("ymin:", ymin, "ymax:", ymax)
        
        dy = ymax - ymin
        print("dx:", dx, "dy:", dy)
        ymax /= 0.7
        ymin /= 0.7
        
        dy = ymax - ymin
        
        print("dx:", dx, "dy:", dy)
        
        offSetX = x1
        offSetY = ymin
        
        pdy = dy / alto_pantalla
        
        print("offSetY:", offSetY, "pdy:", pdy)
        
        try:
            archivo = open("trazado.txt", "w")
            
            ejex = int(alto_pantalla - (0 - offSetY)/pdy)
            
            if ejex > 20 and ejex < alto_pantalla - 20:
                archivo.write(str(0) + "," + str(ejex) + "," + str(1) + '\n')
                archivo.write(str(ancho_pantalla) + "," + str(ejex) + "," + str(2) + '\n')
            
            ejey = int((0 - offSetX)/pdx)
            
            if ejey > 20 and ejey < alto_pantalla - 20:
                archivo.write(str(ejey) + "," + str(0) + "," + str(1) + '\n')
                archivo.write(str(ejey) + "," + str(alto_pantalla) + "," + str(2) + '\n')
                
            primero = True
            j = 0
            while j <= ancho_pantalla:
                xn = x1 + j * pdx
                y = a*xn**3 + b*xn**2 + c*xn + d
                if int(alto_pantalla - (y - offSetY)/pdy) >= 10 and int(alto_pantalla - (y - offSetY)/pdy) <= alto_pantalla -10:
                    if primero:
                        archivo.write(str(int(j)) + "," + str(int(alto_pantalla - (y - offSetY)/pdy)) + "," + str(1) + '\n')
                        primero = False
                    else:
                        archivo.write(str(int(j)) + "," + str(int(alto_pantalla - (y - offSetY)/pdy)) + "," + str(2) + '\n')
                
                j += 1
                
            archivo.close()
            
        except:
            print("No se pudo sobrescribir el archivo")
        
        #self.trazar_archivo()
         
        if x1 >= 0:
            if ymin >= 0:
                self.dibujar_numero(x1, 200, alto_pantalla - 200)
                self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2), alto_pantalla - 200)
                self.dibujar_numero(ymin, 50, alto_pantalla - 400)
                self.dibujar_numero(ymax, 50, 50)
            elif ymax <= 0:
                self.dibujar_numero(x1, 200, 50)
                self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2), 50)
                self.dibujar_numero(ymin, 50, alto_pantalla - 200)
                self.dibujar_numero(ymax, 250, 50)
            else:
                if int(alto_pantalla - (0 - offSetY)/pdy) >= alto_pantalla/2:
                    self.dibujar_numero(x1, 50, int(alto_pantalla - (0 - offSetY)/pdy) + 50)
                    self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2), int(alto_pantalla - (0 - offSetY)/pdy) + 50)
                else:
                    self.dibujar_numero(x1, 50, int(alto_pantalla - (0 - offSetY)/pdy) - 200)
                    self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2), int(alto_pantalla - (0 - offSetY)/pdy) - 200)
                    
                self.dibujar_numero(ymin, 50, alto_pantalla - 200)
                self.dibujar_numero(ymax, 50, 50)
        
        elif x2 <= 0:
            if ymin >= 0:
                self.dibujar_numero(x1, 50, alto_pantalla - 200)
                self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2) - 150, alto_pantalla - 200)
                self.dibujar_numero(ymin, ancho_pantalla - self.espacio_numero(ymin), alto_pantalla - 400)
                self.dibujar_numero(ymax, ancho_pantalla - self.espacio_numero(ymax), 50)
            elif ymax <= 0:
                self.dibujar_numero(x1, 50, 50)
                self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2) - 150, 50)
                self.dibujar_numero(ymin, ancho_pantalla - self.espacio_numero(ymin), alto_pantalla - 400)
                self.dibujar_numero(ymax, ancho_pantalla - self.espacio_numero(ymax), 50)
            else:
                if int(alto_pantalla - (0 - offSetY)/pdy) >= alto_pantalla/2:
                    self.dibujar_numero(x1, 50, int(alto_pantalla - (0 - offSetY)/pdy) + 50)
                    self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2), int(alto_pantalla - (0 - offSetY)/pdy) + 50)
                else:
                    self.dibujar_numero(x1, 50, int(alto_pantalla - (0 - offSetY)/pdy) - 200)
                    self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2), int(alto_pantalla - (0 - offSetY)/pdy) - 200)
                
                self.dibujar_numero(ymin, ancho_pantalla - self.espacio_numero(ymin), alto_pantalla - 200)
                self.dibujar_numero(ymax, ancho_pantalla - self.espacio_numero(ymax), 50)
                
        else:
            if ymin >= 0:
                self.dibujar_numero(x1, 50, alto_pantalla - 200)
                self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2), alto_pantalla - 200)
                
                if int((0 - offSetX)/pdx) >= ancho_pantalla/2:
                    self.dibujar_numero(ymin, int((0 - offSetX)/pdx) - self.espacio_numero(ymin), alto_pantalla - 200)
                    self.dibujar_numero(ymax, int((0 - offSetX)/pdx) - self.espacio_numero(ymax), 50)
                else:
                    self.dibujar_numero(ymin, int((0 - offSetX)/pdx) + 50, alto_pantalla - 200)
                    self.dibujar_numero(ymax, int((0 - offSetX)/pdx) + 50, 50)
                    
            elif ymax <= 0:
                self.dibujar_numero(x1, 50, alto_pantalla - 200)
                self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2), alto_pantalla - 200)
                
                if int((0 - offSetX)/pdx) >= ancho_pantalla/2:
                    self.dibujar_numero(ymin, int((0 - offSetX)/pdx) - self.espacio_numero(ymin), alto_pantalla - 200)
                    self.dibujar_numero(ymax, int((0 - offSetX)/pdx) - self.espacio_numero(ymax), 50)
                else:
                    self.dibujar_numero(ymin, int((0 - offSetX)/pdx) + 50, alto_pantalla - 200)
                    self.dibujar_numero(ymax, int((0 - offSetX)/pdx) + 50, 50)
            else:
                if int((0 - offSetX)/pdx) >= ancho_pantalla/2:
                    self.dibujar_numero(ymin, int((0 - offSetX)/pdx) - self.espacio_numero(ymin), alto_pantalla - 200)
                    self.dibujar_numero(ymax, int((0 - offSetX)/pdx) - self.espacio_numero(ymax), 50)
                    
                    if int(alto_pantalla - (0 - offSetY)/pdy) >= alto_pantalla/2:
                        self.dibujar_numero(x1, 50, int(alto_pantalla - (0 - offSetY)/pdy) + 50)
                        self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2), int(alto_pantalla - (0 - offSetY)/pdy) + 50)
                    else:
                        self.dibujar_numero(x1, 50, int(alto_pantalla - (0 - offSetY)/pdy) - 200)
                        self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2), int(alto_pantalla - (0 - offSetY)/pdy) - 200) 
                else:
                    self.dibujar_numero(ymin, int((0 - offSetX)/pdx) + 50, alto_pantalla - 200)
                    self.dibujar_numero(ymax, int((0 - offSetX)/pdx) + 50, 50)
                    
                    if int(alto_pantalla - (0 - offSetY)/pdy) >= alto_pantalla/2:
                        self.dibujar_numero(x1, 50, int(alto_pantalla - (0 - offSetY)/pdy) + 50)
                        self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2), int(alto_pantalla - (0 - offSetY)/pdy) + 50)
                    else:
                        self.dibujar_numero(x1, 50, int(alto_pantalla - (0 - offSetY)/pdy) - 200)
                        self.dibujar_numero(x2, ancho_pantalla - self.espacio_numero(x2), int(alto_pantalla - (0 - offSetY)/pdy) - 200)
            
        self.inicio()

    def circulo(self, offx, offy, r, lista):
        a = math.pi/180
        for c in range(361):
            x = offx + r * math.cos(c*a)
            y = offy + r * math.sin(c*a)
            if int(c / 20) % 2 == 0:
                z = 2
            else:
                z = 1
            lista.append([int(x),int(y),int(z)])
    #----------------------------------------------------------------
            
Imp = Impresora()

#dibujar_grafica(-0.1, 0.2, 4.5, -3.3, -10, 10)

#lista=[]
#Imp.circulo(1300,1800,150,lista)
#print(lista)

#lista = Imp.corazon(200, 200, 80, 60)
#print(lista)

#Imp.dibujar_numero(0, 100, 100)
"""
cont = 1
while cont > 0:
    Imp.ejeYmm(2150)
    Imp.inicio()
    cont -= 1"""