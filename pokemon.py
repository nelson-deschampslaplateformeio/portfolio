class Pokemon:
    def __init__(self, nom, type_list, pv, attaque, defense, niveau=1, evolution=None):
        self.nom = nom
        self.type = type_list  
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.niveau = niveau
        self.evolution = evolution

    def evoluer(self, nouvelle_forme):
        """Fait évoluer le Pokémon vers une nouvelle forme."""
        self.nom = nouvelle_forme.nom
        self.pv = nouvelle_forme.pv
        self.attaque = nouvelle_forme.attaque
        self.defense = nouvelle_forme.defense
        self.type = nouvelle_forme.type
        self.niveau += 1
