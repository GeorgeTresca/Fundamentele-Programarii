from domain.entities import film,client
from domain.validate import film_validator,client_validator
from repository.firma_repository import film_repository,client_repository,ClientFileRepo, FilmFileRepo
from ui.console import Console
from exceptions import ClientNotFoundException
import random
import string




class firma_service:

    def __init__(self, repo_film,repo_client, val_film,val_client):
        """
        Initializeaza service
        :param repo_film: obiect de tip film_repository care ne ajuta sa gestionam multimea de filme
        :type repo_film:
        :param repo_client: obiect de tip client_repository care ne ajuta sa gestionam multimea de seriale
        :type repo_client:
        :param val_film: validator pentru verificarea filmelor
        :type val_film: film_validator
        :param val_client: validator pentru verificarea clientilor
        :type val_client: client_validator_validator
        """
        self.rep_filme = repo_film
        self.rep_clienti=repo_client
        self.val_film= val_film
        self.val_client=val_client

    def add_film(self,id_f,titlu,descriere,gen,nr_inchirieri):
        """
        Adauga film
        :param id_f:ID-ul filmului
        :type id_f:int
        :param titlu: titlul serialului
        :type titlu:str
        :param descriere: descrierea filmului
        :type descriere:str
        :param gen:genul filmului
        :type gen:str
        :param nr_inchirieri:numarul de ori de care a fost inchiriat filmul
        :type nr_inchirieri
        :return: obiectul de tip film creat
        :rtype:-; filmul s-a adaugat in lista
        :raises: ValidationException daca filmul are date invalide
        """
        s = film(id_f,titlu,descriere,gen,nr_inchirieri)
        lista_filme = self.rep_filme.get_all_filme()
        for f in lista_filme:
            if s==f:
                raise ValueError("Filml deja exista")
        self.val_film.validate_film(s)
        self.rep_filme.store_film(s)
        return s

    def add_client(self,id_c,nume,cnp,nr_filme_inchiriate):
        """
        Adauga client
        :param id_c:ID-ul clientului
        :type id_c:int
        :param nume: numele clientului
        :type nume:str
        :param cnp: cnp client
        :type cnp:int
        :param nr_filme_inchiriate:numarul de filme inchiriate
        :type nr_filme_inchiriate:int
        :return: obiectul de tip client creat
        :rtype:-; clientul s-a adaugat in lista
        :raises: ValueError daca clientul are date invalide
        """
        c = {'ID': id_c, 'Nume': nume, 'CNP': cnp, 'Nr. filme inchiriate': nr_filme_inchiriate}
        s = client(c)
        lista_clienti = self.rep_clienti.get_all_clienti()
        for c in lista_clienti:
            if c == s:
                raise ValueError("Clientul deja exista")
        self.val_client.validate_client(s)
        self.rep_clienti.store_client(s)
        return s


    def get_all_filme(self):
        """
        Returneaza o lista cu toate filmele disponibile
        :return: lista de filme disponibile
        :rtype: list of objects de tip film
        """
        return self.rep_filme.get_all_filme()


    def get_all_clienti(self):
        """
        Returneaza o lista cu toti clientii disponibili
        :return: lista de clienti disponibil
        :rtype: list of objects de tip client
        """
        return self.rep_clienti.get_all_clienti()

    def _cauta_f(self,titlu):
        """

        :param titlu: titlul filmului pe care il cautam
        :type: str
        :return: filmul pe care il cautam sau un mesaj daca nu exista
        """
        lista_filme=self.rep_filme.get_all_filme()
        ok=0

        for film in lista_filme:
            if film.get_titlu()==titlu:
                found=film
                ok=1
        if ok==1:
            return found
        else:
            return "Nu exista filmul cautat"

    def _cauta_c(self,nume):
        """

        :param nume: titlul clientului pe care il cautam
        :type: str
        :return: clientul pe care il cautam sau un mesaj daca nu exista
        """
        lista_clienti=self.rep_clienti.get_all_clienti()
        ok=0
        for client in lista_clienti:
            if client.get_nume()==nume:
                found=client
                ok=1
        if ok==1:
            return found
        else:
            return "Nu exista clientul cautat"

    def _mod_film(self,titlu,new_title,descriere,gen):

        """
        :param titlu: titlul filmului pe care dorim sa il modificam
        :type titlu: str
        :param descriere:noua descriere a filmului
        :param new_title:noul titlu al filmului
        :type new_title: str
        :type: str
        :param gen: noul gen al filmului
        :type: str
        :return: modifica valorile filmului daca acesta exista(FilmNotFoundException altfel)
        """
        lista_filme=self.rep_filme.get_all_filme()
        id=film.get_num_objects()+1
        f=film(id,new_title,descriere,gen,0)
        ok=0
        self.val_film.validate_film(f)
        try:
            self.rep_filme.update(titlu,f)
            return "Filmul a fost modificat cu succes"
        except ValueError:
            film.num_instances -= 1

    def _mod_client(self,cnp,nume,new_cnp):
        """

        :param nume: numele clientului cautat
        :type nume: str
        :param cnp:noul cnp al clientului cautat
        :type cnp:int
        :return: modifica valorile clientului daca acesta exista(ClientNotFoundException altfel)
        """
        lista_clienti=self.rep_clienti.get_all_clienti()
        id=client.get_num_objects()
        s = {'ID': id, 'Nume': nume, 'CNP': new_cnp, 'Nr. filme inchiriate': 0}
        c = client(s)
        self.val_client.validate_client(c)
        ok=0
        try:
            self.rep_clienti.update(cnp,c)
            return "Clientul a fost modificat cu succes"
        except ValueError:
            client.num_instances -= 1

    def inchiriere(self,nume,titlu):
        """
        Inchiriaza un film unui client
        :param nume: numele clientului care inchiriaza
        :type nume: str
        :param titlu: titlul filmului care se inchiriaza
        :type titlu: str
        :return:
        """
        ok1=0
        ok2=0
        lista_filme = self.rep_filme.get_all_filme()
        lista_clienti = self.rep_clienti.get_all_clienti()
        for f in lista_filme:
            if f.get_titlu()==titlu:
                ok1=1
        for c in lista_clienti:
            if c.get_nume()==nume:
                ok2=1
        if ok1==1 and ok2==1:
            self.rep_clienti.inchiriere(nume)
            self.rep_filme.inchiriere(titlu)
            return "Filmul a fost inchiriat cu succes"

        else:
            return "Filmul/clientul nu exista"

    def returnare(self,nume,titlu):
        """

         Returneaza un film
        :param nume: numele clientului care returneaza
        :type nume: str
        :param titlu: titlul filmului care se returneaza
        :type titlu: str
        :return:
        """
        ok1=0
        ok2=0
        lista_filme = self.rep_filme.get_all_filme()
        lista_clienti = self.rep_clienti.get_all_clienti()
        for f in lista_filme:
            if f.get_titlu()==titlu and f.get_nr_inchirieri()>0:
                ok1=1
        for c in lista_clienti:
            if c.get_nume()==nume and c.get_nr_f()>0:
                ok2=1
        if ok1==1 and ok2==1:
            self.rep_clienti.returnare(nume)
            self.rep_filme.returnare(titlu)
            return "Filmul a fost returnat cu succes"

        else:
            return "Filmul/clientul nu exista sau filmul nu a fost inchiriat de acel client"

    def _stergere_film(self,titlu):
        """

        :param titlu: titlul filmului care trebuie sters
        :type titlu:str
        :return: Sterge din lista filmul citit de la tastatura
        """

        self.rep_filme.delete(titlu)

    def _stergere_client(self,cnp):
        """

        :param cnp: cnp-ul clientului care trebuie sters
        :return: Sterge din lista filmul citit de la tastatura
        """
        if len(str(cnp)) == 13:
            self.rep_clienti.delete(cnp)
            return "Clientul a fost sters"

        else:
            raise ValueError("CNP-ul trebuie sa aiba 13 cifre valide")


    def random_filme(self,x):
        for i in range(0,x):
            litere = string.ascii_lowercase
            nume_film = ''.join(random.choice(litere) for i in range(7))
            descriere_film = ''.join(random.choice(litere) for i in range(5))
            gen_film=''.join(random.choice(litere) for i in range(5))
            f=film(film.get_num_objects(),nume_film,descriere_film,gen_film,0)
            self.rep_filme.store_film(f)
        return "Filmele au fost generate"

    def clienti_nume(self):
        " :return: Afiseaza clientii ordonati crescator dupa nume"
        lst_clienti=self.get_all_clienti()
        l=[]
        for c in lst_clienti:
            if c.get_nr_f()>0:
                l.append(c)
        if l==[]:
            raise ValueError("Nu exista clienti cu filme inchiriate!")
        else:
            l = sorted(l, key=lambda i: i['Nume'])
            for c in l:
                print(c)

    def clienti_nr_filme(self):
        """

        :return: Afiseaza clientii ordonati descrescator dupa numarul de filme inchiriate
        """
        lst_clienti=self.get_all_clienti()
        l=[]
        for c in lst_clienti:
            if c.get_nr_f()>0:
                l.append(c)
        if l==[]:
            raise ValueError("Nu exista clienti cu filme inchiriate!")
        else:
            l = sorted(l, key=lambda i: i['Nr. filme inchiriate'], reverse=True)
            for c in l:
                print(c)


    def clienti_nr_filme_comb(self):
        """

            :return: Afiseaza clientii ordonati descrescator dupa numarul de filme inchiriate,in caz de egalitate dupa id
            """
        lst_clienti = self.get_all_clienti()
        l = []
        for c in lst_clienti:
            if c.get_nr_f() > 0:
                l.append(c)
        if l == []:
            raise ValueError("Nu exista clienti cu filme inchiriate!")
        else:

            self.mergeSort(l,key=lambda i: (i.get_nr_f(),i.get_id_c()),cmp=self.comparator)
            l.reverse()
            for c in l:
                print(c)

    def comparator(self,client1, client2, key):
        return key(client1) <= key(client2)

    def comparator2(self,client1, client2, key):
        return key(client1) < key(client2)

    def clienti_nr_filme_merge(self):
        """

        :return: Afiseaza clientii ordonati descrescator dupa numarul de filme inchiriate
        """
        lst_clienti=self.get_all_clienti()
        l=[]
        for c in lst_clienti:
            if c.get_nr_f()>0:
                l.append(c)
        if l==[]:
            raise ValueError("Nu exista clienti cu filme inchiriate!")
        else:
            self.mergeSort(l,key=lambda i: i.get_nr_f(),cmp=self.comparator)
            l.reverse()
            for c in l:
                print(c)


    def mergeSort(self,lst,key,cmp):
        """

        :return: lista sortata cu merge sort
        """
        if len(lst) > 1:
            mid = len(lst) // 2
            left = lst[:mid]
            right = lst[mid:]

            self.mergeSort(left,key,cmp)
            self.mergeSort(right,key,cmp)

            i = 0
            j = 0

            k = 0

            while i < len(left) and j < len(right):
                if cmp(left[i],right[j],key):
                    lst[k] = left[i]
                    i += 1
                else:
                    lst[k] = right[j]
                    j += 1
                k += 1

            while i < len(left):
                lst[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                lst[k] = right[j]
                j += 1
                k += 1

        return lst


    def clienti_nr_filme_bingo(self):
        """

                :return: clientii ordonati descrescator dupa numarul de filme inchiriate
                """
        lst_clienti = self.get_all_clienti()
        l = []
        for c in lst_clienti:
            if c.get_nr_f() > 0:
                l.append(c)
        if l == []:
            raise ValueError("Nu exista clienti cu filme inchiriate!")
        else:
            self.BingoSort(l,key=lambda i: i.get_nr_f(),cmp=self.comparator2)
            for c in l:
                print(c)

    def BingoSort(self,lst,key,cmp):
        """

        :param lst: lista pe care dorim sa o sortam
        :return: lista sortata cu bingosort
        """

        bingo = lst[0]
        nextBingo = lst[0]
        mx=0
        mn=999
        for c in lst:
            if c.get_nr_f()>mx:
                mx1=c.get_nr_f()
                mx2=c
            if c.get_nr_f()<mn:
                mn=c.get_nr_f()
                mn2=c
        bingo=mn2
        nextBingo=mx2
        largestEle = nextBingo
        nextElePos = 0
        while cmp(bingo,nextBingo,key):
            startPos = nextElePos
            for i in range (startPos,len(lst)):
                if lst[i] == bingo:
                    lst[i], lst[nextElePos]=lst[nextElePos],lst[i]
                    nextElePos = nextElePos + 1
                elif cmp(lst[i],nextBingo,key):

                    nextBingo = lst[i]
            bingo = nextBingo
            nextBingo = largestEle

        return lst

    def cele_mai_inchiriate(self):
        """

        :return: Afiseaza filmele inchiriate de un numar maxim de ori
        """
        lst_filme=self.get_all_filme()
        l=[]
        mx=0
        for f in lst_filme:
            if f.get_nr_inchirieri()>mx:
                mx=f.get_nr_inchirieri()
        if mx==0:
            raise ValueError("NU exista filme inchiriate!")
        else:
            for f in lst_filme:
                if f.get_nr_inchirieri() == mx:
                    print(f)



    def cele_mai_inchiriate_rec(self,i,mx):
        """

        :param i: pozitia din lista
        :type i:int
        :param mx: numarul maxim de aparitii
        :type mx:int
        :return: printeaza elem inchiriate de nr max de ori sau un mesaj
        """

        lst_filme=self.get_all_filme()
        if i<len(lst_filme):
            if lst_filme[i].get_nr_inchirieri() > mx:
                mx = lst_filme[i].get_nr_inchirieri()
            if i < len(lst_filme):
                i=i+1
                self.cele_mai_inchiriate_rec(i, mx)
        elif mx==0:
            raise ValueError("NU exista filme inchiriate!")
        else:
            for f in lst_filme:
                if f.get_nr_inchirieri() == mx:
                    print(f)

    def cele_mai_inchiriate_30(self):
        """

        :return: Se afiseaza primii 30% clienti cu cele mai multe filme
        """
        lst_clienti=self.get_all_clienti()
        l=[]
        for c in lst_clienti:
            if c.get_nr_f()>0:
                l.append(c)
        if l==[]:
            raise ValueError("Nu exista clienti cu filme inchiriate!")
        else:
            l = sorted(l, key=lambda i: i['Nr. filme inchiriate'], reverse=True)
            lungime=int(0.3 * len(l))
            for i in range (0,lungime):
                print(l[i].get_nume_client())


    def filmele_neinchiriate(self):
        """

        :return: Se afiseaza filmele care nu au fost inchiriate
        """
        lst_filme=self.get_all_filme()
        l=[]
        for f in lst_filme:
            if f.get_nr_inchirieri()==0:
                l.append(f)
        if l==[]:
            raise ValueError("NU exista filme neinchiriate!")
        else:
            for f in l:
                    print(f)

    def filmele_neinchiriate_rec(self,i,l):
        """

        :param i:
        :return: filmele neinchiriate
        """
        lst_filme = self.get_all_filme()
        if i<len(lst_filme):
            if lst_filme[i].get_nr_inchirieri() ==0:
                l.append(lst_filme[i])
            if i < len(lst_filme):
                i=i+1
                self.filmele_neinchiriate_rec(i, l)
        elif l==[]:
            raise ValueError("NU exista filme neinchiriate!")
        else:
            for f in l:
                    print(f)

    def filmele_neinchiriate_fisier(self):
        """

        :return: Se afiseaza filmele care nu au fost inchiriate in fisier
        """
        lst_filme=self.get_all_filme()
        l=[]
        for f in lst_filme:
            if f.get_nr_inchirieri()==0:
                l.append(f)
        if l==[]:
            raise ValueError("NU exista filme neinchiriate!")
        else:
            self.rep_filme.raport(l)


def test_add_film():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    film1 = test_srv.add_film(1,"Lord of the Rings", "foarte bun", "Fantasy,Actiune",0)

    assert (len(test_srv.rep_filme.get_all_filme()) == 1)
    assert (film1.get_titlu()=='Lord of the Rings')
    assert (film1.get_gen()=="Fantasy,Actiune")
    assert (film1.get_id_f() == 1)



    try:
        film1 = test_srv.add_film(2,"Star Wars", "0", "abc",0)
        assert False
    except ValueError:
        assert True

def test_add_client():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    client1=test_srv.add_client(1, "Pop Vasile", 5123428064259, 0)

    assert (len(test_srv.rep_clienti.get_all_clienti()) == 1)
    assert (client1.get_nume()=='Pop Vasile')
    assert (client1.get_cnp()==5123428064259)
    assert (client1.get_id_c() == 1)



    try:
        client1 = test_srv.add_client(2,"Pop Vasile",12345 ,0)
        assert False
    except ValueError:
        assert True

def test_cauta_film():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    film1 = test_srv.add_film(1,"Lord of the Rings", "foarte bun", "Fantasy,Actiune",0)
    film2= test_srv.add_film(1,"The Nun", "ok", "Horror",0)

    assert (test_srv._cauta_f("Lord of the Rings")==film1)
    assert (test_srv._cauta_f("Godfather")=="Nu exista filmul cautat")

def test_cauta_client():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    client1 = test_srv.add_client(1, "Pop Vasile", 5123428064259, 0)
    client2= test_srv.add_client(1, "Pop Ion", 5123428123456, 0)

    assert (test_srv._cauta_c("Pop Ion")==client2)
    assert (test_srv._cauta_c("George")=="Nu exista clientul cautat")


def test_mod_film():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)
    film1 = test_srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
    assert (test_srv._mod_film("Lord of the Rings","Stapanul inelelor", "peste medie","Aventura") == "Filmul a fost modificat cu succes")
    #assert (test_srv._mod_film("Lord of the Rings","Stapanul inelelor", "peste medie", "Aventura") == "Filmul nu a fost gasit")
    try:
        test_srv._mod_film("Stapanul inelelor","Lord of the Rings", "xy", "z")
        assert False
    except ValueError:
        assert True

def test_mod_client():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)
    client1 = test_srv.add_client(1, "Pop Vasile", 5123428064259, 0)
    assert(test_srv._mod_client(5123428064259,"Pop Ion",5902518390176)=="Clientul a fost modificat cu succes")
    #assert(test_srv._mod_client(5123428064259,"Pop Ion",5035678920108)==ClientNotFoundException())
    try:
        test_srv._mod_client(5902518390176,"AB", 5423577901)
        assert False
    except ValueError:
        assert True

def test_inchiriere():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    film1 = test_srv.add_film(1,"Lord of the Rings", "foarte bun", "Fantasy,Actiune",0)
    client1 = test_srv.add_client(1, "Pop Vasile", 5123428064259, 0)
    assert(test_srv.inchiriere("Pop Vasile","Lord of the Rings")=="Filmul a fost inchiriat cu succes")
    assert (test_srv.inchiriere("Pop Vasile","Star Wars")=="Filmul/clientul nu exista")

def test_returnare():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    test_srv.add_film(1,"Lord of the Rings", "foarte bun", "Fantasy,Actiune",0)
    test_srv.add_client(1, "Pop Vasile", 5123428064259, 0)
    test_srv.inchiriere("Pop Vasile", "Lord of the Rings")
    assert(test_srv.returnare("Pop Vasile","Lord of the Rings")=="Filmul a fost returnat cu succes")
    assert(test_srv.returnare("Pop Vasile","Lord of the Rings")=="Filmul/clientul nu exista sau filmul nu a fost inchiriat de acel client")

def test_stergere_film():
    repo_film = FilmFileRepo("data/filme.txt")
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    test_srv.add_film(1,"abcdefg", "foarte bun", "Fantasy,Actiune",0)
    test_srv._stergere_film("abcdefg")
    #assert (len(test_srv.get_all_filme())==1)
    assert(test_srv._cauta_f("abcdefg")=="Nu exista filmul cautat")

def test_stergere_client():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = ClientFileRepo("data/clienti.txt")
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    test_srv.add_client(1, "Pop Vasile", 5123428064259, 0)
    test_srv._stergere_client(5123428064259)
    #assert (len(test_srv.get_all_clienti())==2)
    assert(test_srv._cauta_c("Pop Vasile")=="Nu exista clientul cautat")

def test_clienti_nume():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    test_srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
    test_srv.add_film(2, "Star Wars", "bun", "Sf,Aventura", 0)
    test_srv.add_film(3, "IT", "mediu", "Horror", 0)
    test_srv.add_film(4, "Need for Speed", "peste medie", "Actiune,Aventura", 0)
    test_srv.add_film(5, "Titanic", "excelent", "Drama,Dragoste", 0)

    test_srv.add_client(1, "Pop Vasile", 5134789562308, 0)
    test_srv.add_client(2, "Pop Ion", 5348913623081, 0)
    test_srv.add_client(3, "Sabou Alexandra", 6134789586408, 0)
    test_srv.add_client(4, "George Tresca", 5134798736129, 0)

    test_srv.inchiriere("Pop Vasile", "Lord of the Rings")
    test_srv.inchiriere("Pop Vasile", "Star Wars")
    test_srv.inchiriere("George Tresca", "Star Wars")
    lst_clienti = test_srv.get_all_clienti()
    l = []
    for c in lst_clienti:
        if c.get_nr_f() > 0:
            l.append(c)

    l = sorted(l, key=lambda i: i['Nume'])
    assert(l[0].get_nume()=="George Tresca")
    assert(l[1].get_nume()=="Pop Vasile")

def test_client_nr_filme():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    test_srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
    test_srv.add_film(2, "Star Wars", "bun", "Sf,Aventura", 0)
    test_srv.add_film(3, "IT", "mediu", "Horror", 0)
    test_srv.add_film(4, "Need for Speed", "peste medie", "Actiune,Aventura", 0)
    test_srv.add_film(5, "Titanic", "excelent", "Drama,Dragoste", 0)

    test_srv.add_client(1, "Pop Vasile", 5134789562308, 0)
    test_srv.add_client(2, "Pop Ion", 5348913623081, 0)
    test_srv.add_client(3, "Sabou Alexandra", 6134789586408, 0)
    test_srv.add_client(4, "George Tresca", 5134798736129, 0)

    test_srv.inchiriere("Pop Vasile", "Lord of the Rings")
    test_srv.inchiriere("Pop Vasile", "Star Wars")
    test_srv.inchiriere("George Tresca", "Star Wars")
    lst_clienti = test_srv.get_all_clienti()
    l = []
    for c in lst_clienti:
        if c.get_nr_f() > 0:
            l.append(c)

    l = sorted(l, key=lambda i: i['Nr. filme inchiriate'],reverse=True)
    assert(l[0].get_nume()=="Pop Vasile")
    assert(l[1].get_nume()=="George Tresca")

def test_cele_mai_inchiriate():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    test_srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
    test_srv.add_film(2, "Star Wars", "bun", "Sf,Aventura", 0)
    test_srv.add_film(3, "IT", "mediu", "Horror", 0)
    test_srv.add_film(4, "Need for Speed", "peste medie", "Actiune,Aventura", 0)
    test_srv.add_film(5, "Titanic", "excelent", "Drama,Dragoste", 0)

    test_srv.add_client(1, "Pop Vasile", 5134789562308, 0)
    test_srv.add_client(2, "Pop Ion", 5348913623081, 0)
    test_srv.add_client(3, "Sabou Alexandra", 6134789586408, 0)
    test_srv.add_client(4, "George Tresca", 5134798736129, 0)

    test_srv.inchiriere("Pop Vasile", "Lord of the Rings")
    test_srv.inchiriere("Pop Vasile", "Star Wars")
    test_srv.inchiriere("George Tresca", "Star Wars")

    lst_filme = test_srv.get_all_filme()
    l = []
    mx = 0
    for f in lst_filme:
        if f.get_nr_inchirieri() > mx:
            mx = f.get_nr_inchirieri()

    for f in lst_filme:
        if f.get_titlu()=="Star Wars":
            assert(f.get_nr_inchirieri() == mx)
        else:
            assert (f.get_nr_inchirieri() != mx)


def test_cele_mai_inchiriate_30():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    test_srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
    test_srv.add_film(2, "Star Wars", "bun", "Sf,Aventura", 0)
    test_srv.add_film(3, "IT", "mediu", "Horror", 0)
    test_srv.add_film(4, "Need for Speed", "peste medie", "Actiune,Aventura", 0)
    test_srv.add_film(5, "Titanic", "excelent", "Drama,Dragoste", 0)

    test_srv.add_client(1, "Pop Vasile", 5134789562308, 0)
    test_srv.add_client(2, "Pop Ion", 5348913623081, 0)
    test_srv.add_client(3, "Sabou Alexandra", 6134789586408, 0)
    test_srv.add_client(4, "George Tresca", 5134798736129, 0)

    test_srv.inchiriere("Pop Vasile", "Lord of the Rings")
    test_srv.inchiriere("Pop Vasile", "Star Wars")
    test_srv.inchiriere("George Tresca", "Star Wars")
    lst_clienti = test_srv.get_all_clienti()
    l = []
    for c in lst_clienti:
        if c.get_nr_f() > 0:
            l.append(c)

    l = sorted(l, key=lambda i: i['Nr. filme inchiriate'],reverse=True)
    lungime = int(0.3 * len(l))
    assert(lungime==0)


def test_filme_neinchiriate():
    repo_film = film_repository()
    validator_film = film_validator()
    repo_client = client_repository()
    validator_client = client_validator()
    test_srv = firma_service(repo_film,repo_client,validator_film,validator_client)

    test_srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
    test_srv.add_film(2, "Star Wars", "bun", "Sf,Aventura", 0)
    test_srv.add_film(3, "IT", "mediu", "Horror", 0)
    test_srv.add_film(4, "Need for Speed", "peste medie", "Actiune,Aventura", 0)
    test_srv.add_film(5, "Titanic", "excelent", "Drama,Dragoste", 0)

    test_srv.add_client(1, "Pop Vasile", 5134789562308, 0)
    test_srv.add_client(2, "Pop Ion", 5348913623081, 0)
    test_srv.add_client(3, "Sabou Alexandra", 6134789586408, 0)
    test_srv.add_client(4, "George Tresca", 5134798736129, 0)

    test_srv.inchiriere("Pop Vasile", "Lord of the Rings")
    test_srv.inchiriere("Pop Vasile", "Star Wars")

    lst_filme = test_srv.get_all_filme()
    l = []
    for f in lst_filme:
        if f.get_nr_inchirieri() == 0:
            l.append(f)

    assert(len(l)==3)

    for f in l:
        assert(f.get_titlu()!="Star Wars" and f.get_titlu()!="Lord of the Rings")



#test_add_film()
#test_add_client()
#test_cauta_film()
#test_cauta_client()
#test_mod_film()
#test_mod_client()
#test_inchiriere()
#test_returnare()
#test_stergere_film()
#test_stergere_client()
#test_clienti_nume()
#test_client_nr_filme()
#test_cele_mai_inchiriate_30()
#test_filme_neinchiriate()