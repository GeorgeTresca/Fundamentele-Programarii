
class film:
    #obiecte de tip film
    num_instances=0
    def __init__(self,id_f,titlu,descriere,gen,nr_inchirieri):
        """
        Creeaza un nou film
        :param id_f: id-ul filmului
        :type id_f:int
        :param titlu: titlul filmului
        :type titlu: str
        :param descriere: descrierea filmului
        :type descriere: str
        :param gen: genul filmului
        :typer gen: str
        :param nr_inchirieri: numarul de ori de care a fopst inchiriat filmul
        :type nr_inchirieri: int
        """

        self.id_f=id_f
        self.titlu=titlu
        self.descriere=descriere
        self.gen=gen
        self.nr_inchirieri=nr_inchirieri
        film.num_instances+=1

    def get_id_f(self):
        return self.id_f

    def get_titlu(self):
        return self.titlu

    def get_descriere(self):
        return self.descriere

    def get_gen(self):
        return self.gen

    def get_nr_inchirieri(self):
        return self.nr_inchirieri

    def set_id_f(self,value):
        self.id_f=value

    def set_titlu(self,value):
        self.titlu=value

    def set_descriere(self,value):
        self.descriere=value

    def set_gen(self,value):
        self.gen=value

    def set_nr_inchirieri(self,value):
        self.nr_inchirieri=value

    def __eq__(self, other):
        """
        Verifica egalitatea intre serialul curent si serialul other
        :param other:
        :type other: film
        :return: True daca serialele sunt egale (au acelasi titlu, aceeasi descriere si acelasi gen), False altfel
        :rtype: bool
        """
        if self.titlu == other.get_titlu() :
            return True
        return False

    def __str__(self):
        return "ID:" + str(self.id_f)+ "; Titlu:" + self.titlu + '; Descriere:' + self.descriere + '; Gen:' + self.gen+ 'Nr. inchirieri:'+str(self.nr_inchirieri)

    @staticmethod
    def get_num_objects():
        return film.num_instances




class client():
    #obiecte de tip client
    num_instances=0

    def __init__(self, init=None):
        if init is not None:
            self.__dict__.update(init)
        client.num_instances+=1

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, valoare):
        self.__dict__[key] = valoare

    def get_id_c(self):
        return self.__dict__['ID']

    def get_nume(self):
        return self.__dict__['Nume']

    def get_cnp(self):
        return self.__dict__['CNP']

    def get_nr_f(self):
        return self.__dict__['Nr. filme inchiriate']


    def set_nume(self,nume):
        self.__dict__['Nume']=nume

    def set_id_c(self,id_c):
        self.__dict__['ID']=id_c

    def set_cnp(self,cnp):
        self.__dict__['CNP']=cnp

    def set_nr_filme_inchiriate(self,nr):
        self.__dict__['Nr. filme inchiriate']=nr

    def __eq__(self, other):
        """
        Verifica egalitatea intre clientul curent si clientul other
        :param other:
        :type other: client
        :return: True daca clientii sunt egali (au acelasi nume, si acelasi cnp), False altfel
        :rtype: bool
        """
        if self.get_cnp() == other.get_cnp():
            return True
        return False

    def __str__(self):
        return "ID:" + str(self.get_id_c())+ "; Nume:" + self.get_nume() + '; CNP:' + str(self.get_cnp()) + '; Nr. filme inchriate:' + str(self.get_nr_f())

    @staticmethod
    def get_num_objects():
        return client.num_instances

def test_create_film():
        film1 = film(film.get_num_objects()+1,"Lord of the Rings", "foarte bun", "Fantasy,Actiune",0)
        assert (film1.get_id_f()==1)
        assert (film1.get_titlu() == 'Lord of the Rings')
        assert (film1.get_descriere() == 'foarte bun')
        assert (film1.get_gen() == 'Fantasy,Actiune')
        assert (film1.get_nr_inchirieri()==0)

        film1.set_titlu('See')
        film1.set_descriere('bun')
        film1.set_gen('Drama')

        assert (film1.get_titlu() == 'See')
        assert (film1.get_descriere() == 'bun')
        assert (film1.get_gen() == 'Drama')

def test_create_client():
    s = {'ID': 1, 'Nume': "Pop Vasile", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
    c = client(s)
    assert(c.get_id_c()==1)
    assert(c.get_nume()=="Pop Vasile")
    assert(c.get_cnp()==5123428064259)
    assert(c.get_nr_f()==0)

    c.set_nume("Pop Ion")
    c.set_cnp(5123123456259)

    assert(c.get_nume()=="Pop Ion")
    assert(c.get_cnp()==5123123456259)


def test_equals_serial():
    film1 = film(1,"Lord of the Rings", "foarte bun", "Fantasy,Actiune",0)
    film2 = film(2,"Lord of the Rings", "foarte bun", "Fantasy,Actiune",0)

    assert (film1 == film2)

    film3 =film(1,"Stapanul inelelor", "foarte bun", "Fantasy,Actiune",0)
    assert (film1 != film3)

def test_equals_client():
    s1 = {'ID': 1, 'Nume': "Pop Vasile", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
    c1 = client(s1)
    s2={'ID': 1, 'Nume': "Pop Vasile", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
    c2 = client(s2)

    assert(c1==c2)

    s3 = {'ID': 1, 'Nume': "Pop Vasile", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
    c3 = client(s3)

    assert(c1!=c3)


test_create_film()
test_create_client()
test_equals_serial()
