class Terrain():
    T_names = ["flat", "hilly", "forest", "cave"]

    def __init__(self, name, p_false_neg):
        self.name = name
        self.p_false_neg = p_false_neg


    @classmethod
    def generate_flat(cls):
        return cls('flat', 0.1)

    @classmethod
    def generate_hilly(cls):
        return cls('hilly', 0.3)

    @classmethod
    def generate_forest(cls):
        return cls('forest', 0.7)

    @classmethod
    def generate_cave(cls):
        return cls('cave', 0.9)

    @classmethod
    def generate_from_index(cls, i):
        f = getattr(cls, "generate_"+cls.T_names[i])
        return f()


    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name