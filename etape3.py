from tkinter import *
from random import randint
import time


class Menus(): #controleur
    "Demande la resolution pour lancer le modele"
    def __init__(self ):
        self.tk=Tk()
        self.fen=Frame(self.tk)
        self.fen.pack(fill= BOTH, expand = True)
        self.bou = Button(self.fen, text="SNAKE V2 POOOOOOOOOOOOOOOOOO(programmation orienté objet Oo)",
                           background="black", fg="white", width=150, height=5,font="Courier", command=self.credit)
        self.bou.pack(side=TOP, expand=True, fill=BOTH)
        self.bou1 = Button(self.fen, text='Resolution 800x600', background = "red", fg = "white", width=50, height=5, font="Courier", command=self.resolution1)
        self.bou1.pack(side=TOP, expand=True, fill=BOTH)
        self.bou2 = Button(self.fen, text='Resolution 1000x800', background = "blue", fg = "white",width=50, height=5, font="Courier", command=self.resolution2)
        self.bou2.pack(side=TOP, expand=True, fill=BOTH)
        self.bou3 = Button(self.fen, text='Resolution 1200x1000', background = "green", fg = "white",width=50, height=5, font="Courier", command=self.resolution3)
        self.bou3.pack(side=TOP, expand=True, fill=BOTH)
        self.tk.mainloop()

    def resolution1(self):
        jeux=Interface_graphique(800, 600, Moteur_serpent)

    def resolution2(self):
        jeux=Interface_graphique(1000, 800, Moteur_serpent)


    def resolution3(self):
        jeux=Interface_graphique(1200,1000, Moteur_serpent)

    def credit(self):
        Credit()

class Credit:
    def __init__(self):
        self.fen = Tk()
        self.can=Canvas(self.fen, bg='dark grey', height=400, width=400)
        self.can.pack()
        presentation="GotLuB tous droits reservés ©"
        self.can.create_text(200,200,text=presentation,font="Courier")
        self.fen.mainloop()



class Moteur_serpent:  # controleur
    """parti centrale du programme avec la boucle 'jouer',creer les conditions, lie les objets et leurs interactions
     avec comme paramètres d'entrée la resolutions le canevas et la fenettre de jeux"""

    def __init__(self, x, y, can1, fen):
        self.K = 50
        self.x, self.y, self.can1, self.fen = x, y, can1, fen
        self.commandes = Commandes(self.fen)
        self.vitesse = 50
        self.boucle = 0                                                                                                  # notre timer , temps=boucle*(parametre[0] de self.fen.after en ms
        self.serpent = Serpent(can1=self.can1)
        self.bonbons = BonBons(self.can1, self.x, self.y)
        self.fen.bind("<Control-Z>", self.recommencer)
        self.fen.bind("<Control-P>",self.tchekVitesse)
        self.en_attente()
        self.couleur=["red","orange","green"]

    def tchekVitesse(self, event):
        self.vitesse=100-int(self.commandes.tchek_vitesse())*10

    def recommencer(self, event=None):
        try:
            self.can1.delete('all')

        except:
            pass
        self.boucle = 0
        self.serpent.reset()
        self.bonbons.reset()
        self.commandes.reset()

    def en_attente(self):
        self.mouvement = self.commandes.tchek_move()
        if self.mouvement:
        #    for k in range(6):
        #        if k%2==0:
        #            self.rec = self.can1.create_rectangle(0, 0, self.x, self.y, fill='red')
        #            time.sleep(0.5)
        #        if k%2==1:
        #            self.can1.delete(self.rec)
        #            time.sleep(0.5)

            self.fen.after(300, self.jouer)
        else:
            self.fen.after(150, self.en_attente)

    def jouer(self):
        self.mouvement = self.commandes.tchek_move()
        if self.mouvement:
            self.serpent.sens = self.commandes.tchek_sens()
            self.condition()
            self.serpent.deplacement()
            self.boucle += 1

            if self.boucle % 50 == 0:
                self.bonbons.des_bonbons()
        if int(self.boucle)%5==0:
            self.commandes.affichage_points(int(self.boucle),int(self.serpent.longeur))
        self.fen.after(self.vitesse, self.jouer)

    def condition(self):
        memoire=''
        if self.serpent.tete[0] + self.K > self.x \
                or self.serpent.tete[0] < 0 \
                or self.serpent.tete[1] + self.K > self.y \
                or self.serpent.tete[1] < 0 \
                or self.serpent.tete in self.serpent.coordonnes[1:len(self.serpent.coordonnes)]:  #si la tete du serpent est en dehors du cadre , ou dans son propre corps
            self.game_over()
        if len(self.bonbons.bonbons)>0:
            for nb,serp in enumerate(self.bonbons.bonbons):                                       #si le serpent croise un bonbon
                try:
                    serp1 = [int(self.can1.coords(serp)[0]), int(self.can1.coords(serp)[1])]      #convertion des cordonnes du carré en celuis du point supérieure gauche en entier
                except:                                                                           #parfois les bonbons disparaisent , la vie c'est le moment present
                    serp1 = 0
                if serp1 == self.serpent.tete:
                    self.serpent.grandir()
                    memoire = nb
        if memoire != "":
            self.can1.delete(self.bonbons.bonbons[memoire])                                       #supresion a l'extérieure de la boucle pour ne pas génerer d'erreure,
                                                                                                  #la boucle est actualisé a chaque deplacement de la taille d'un bonbon le serpant ne peut en manger deux en une fois

    def game_over(self):
        self.commandes.stop()
        self.commandes.fen.title("Game over")
        time.sleep(1)
        self.rec = self.can1.create_rectangle(0, 0, self.x, self.y, fill='red')
        self.commandes.fen.title("Game over")


class Commandes(Frame):  # vu
    "controlles et messages a destination de l'utilisateur"

    def __init__(self, fen):
        Frame.__init__(self)
        self.fen = fen
        self.serpent_sens = [50, 0]
        self.move = False
        self.vitesse=5
        self.bou1 = Button(self.fen, text='Quitter',background = "red", fg = "white", width=30, font="Courier", command=fen.destroy)
        self.bou1.grid(row=3, column=2, padx=5, pady=5)
        self.bou2 = Button(self.fen, text='Démarrer/Pause',background = "green", fg = "white", width=30, font="Courier", command=self.mouvement)
        self.bou2.grid(row=4, column=2, padx=5, pady=5)
        self.bou3 = Button(self.fen, text='Recommencer', background = "blue", fg = "white", width=30, font="Courier", command=self.recommencer)
        self.bou3.grid(row=5, column=2, padx=5, pady=5)
        self.bou4 = Scale(self.fen, length=300, orient=HORIZONTAL, sliderlength=25, label='Vitesse', from_=0, to=10, tickinterval=1,
                          showvalue=1, troughcolor='grey50', font="Courier", command=self.setVitesse)
        self.bou4.grid(row=3, column=1, padx=5, pady=5, sticky=E)
        self.bou4.set(5)
        self.lab=Label(self.fen, text=' En attente de partie')
        self.lab.grid(row=5, column=5, padx=5, pady=5)
        self.lab.configure(font=("Courier", 16, "italic"))
        self.fen.bind("<Key-Left>", self.depleft)
        self.fen.bind("<Key-Right>", self.depright)
        self.fen.bind("<Key-Down>", self.depup)
        self.fen.bind("<Key-Up>", self.depdown)
        self.fen.title("Snake v2 -> Flèches directionnelles pour controler la bestiole")

    def depleft(self, event):
        self.serpent_sens = [-50, 0]

    def depright(self, event):
        self.serpent_sens = [50, 0]

    def depup(self, event):
        self.serpent_sens = [0, 50]

    def depdown(self, event):
        self.serpent_sens = [0, -50]

    def setVitesse(self, vitesse):
        self.vitesse = vitesse
        self.fen.event_generate('<Control-P>')

    def tchek_sens(self):
        return self.serpent_sens

    def tchek_move(self):
        return self.move

    def tchek_vitesse(self):
        return int(self.vitesse)

    def affichage_points(self, boucle, points):
        des_points = (boucle*(int(self.vitesse)))/100+points*50
        if 10-len(str(des_points)) >= 0 :
            espace=' '*(10-len(str(des_points)))
        else:
            espace=''
        self.lab.configure(text=f"Score : {des_points} {espace}")
        self.lab.configure(font=("Courier", 16, "italic"))

    def stop(self):
        self.move = False

    def mouvement(self):
        if not self.move:
            self.move = True
        else:
            self.move = False

    def recommencer(self):
        self.fen.event_generate("<Control-Z>")

    def reset(self):
        self.serpent_sens = [50, 0]
        self.fen.title("Snake v2 -> Flèches directionnelles pour controler la bestiole")



class Interface_graphique:  # modele
    """initialise la fenetre et le canevas tkinter, """

    def __init__(self, x, y, objet):
        self.x, self.y = x, y
        self.fen = Tk()
        self.objet = objet
        self.can1 = Canvas(self.fen, bg='dark grey', height=self.y, width=self.x)
        self.can1.grid(column=1, columnspan=5 , padx=5, pady=5)
        objet(self.x, self.y, self.can1, self.fen)                                                                      # on lance l'objet qui est le jeux
        self.fen.mainloop()



class Serpent:  # model
    serpent = [0, 0]                                                                                                     # coordone du serpent  
    """ Un serpent a un sens une tete et une longeur qui est cartographiable, il est un object graphique lié au canvas"""

    def __init__(self, can1, sens=[0, 50], longeur=1, coordonnes=[[0, 0], [0, -50]]):
        self._K = 50                                                                                                     # une constante en self pour y acceder dans la classe, est-ce pep8?
        self.can1 = can1                                                                                                 # canvas ou le serpent se deplace
        self.sens = sens
        self.longeur = longeur
        self.coordonnes = coordonnes                                                                                    # serpent + serpent[-1] qui est une memoire
        self.tete = [0, 0]
        self.snake = [
            self.can1.create_rectangle(self.coordonnes[0][0], self.coordonnes[0][1], self.coordonnes[0][0] + self._K,
                                       self.coordonnes[0][1] + self._K, width=2, fill='grey1')]

    def grandir(self):
        "Petit serpent deviendra grand, concatenation d'un rectangle sur la memoire"
        self.longeur += 1
        couleur='grey'+str(self.longeur)
        self.snake.append(self.can1.create_rectangle(self.coordonnes[-1][-2], self.coordonnes[-1][-1],
                                                     self.coordonnes[-1][-2] + self._K,
                                                     self.coordonnes[-1][-1] + self._K, width=2,
                                                     fill=couleur))  # la derniere coordonne est toujours la memoire

    def deplacement(self):
        nouvelle_place = [self.coordonnes[0][0] + self.sens[0], self.coordonnes[0][1] + self.sens[1]]
        self.coordonnes.insert(0, nouvelle_place)
        if len(self.coordonnes) > self.longeur + 1:  # calcul de la memoire, par rapport a la taille du serpent
            del self.coordonnes[-1]  # on garde 1 en mémoire dans les coordonne
        self.tete = nouvelle_place
        Serpent.serpent = self.coordonnes[:self.longeur]  # juste le serpent sans ça memoire
        for segment in range(self.longeur):
            self.can1.coords(self.snake[segment], self.coordonnes[segment][0], self.coordonnes[segment][1],
                             self.coordonnes[segment][0] + self._K, self.coordonnes[segment][1] + self._K)

    def reset(self):
        self.longeur = 1
        self.coordonnes = [[0, 0], [0, -50]]
        self.tete = [0, 0]
        self.snake = [
            self.can1.create_rectangle(self.coordonnes[0][0], self.coordonnes[0][1], self.coordonnes[0][0] + self._K,
                                       self.coordonnes[0][1] + self._K, width=2, fill='grey1')]


class BonBons:  # model
    """Les bonbons çà va ça vient , gènère des coordonnée qui apparaissent et disparaissent """

    def __init__(self, can1, x, y):
        self.K = 50                                                                                                      # une constante en self pour y acceder dans la classe, est-ce pep8?
        self.can1 = can1                                                                                                 # canvas où sont placé les bonbons
        self.x, self.y = x, y  # la resolution
        self.bonbons = []
        self.coordonnes = []

    def des_bonbons(self):
        while len(self.bonbons) > 0:
            self.can1.delete(self.bonbons[-1])
            del self.bonbons[-1]
                                                                                                                        # on suprime a partir de la fin pour ne pas avoir d'erreure d'index
        self.coordonnes = []

        for k in range(4):
            coordonne = self.generateur()
            couleur=["brown", "medium violet red", "green", "DarkOrange1"][randint(0,3)]
            self.coordonnes.append(coordonne)
            self.bonbons.append(
                self.can1.create_oval(coordonne[0], coordonne[1], coordonne[0] + self.K, coordonne[1] + self.K, width=2,
                                      fill=couleur))


    def generateur(self):
        resolx = (self.x - self.K * 2) / self.K                                                                         #generateur de coordonne random
        resoly = (self.y - self.K * 2) / self.K
        while 1:
            x = randint(0, resolx) * self.K
            y = randint(0, resoly) * self.K
            self.coordo = [x, y]
            if self.coordo not in Serpent.serpent and self.coordo not in self.coordonnes:
                return self.coordo

    def reset(self):
        self.bonbons = []
        self.coordonnes = []



jeux=Menus()

"""GotLuB tous droits reservés ©"""

