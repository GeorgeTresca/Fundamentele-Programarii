from domain.entities import film,client
from exceptions import CorruptedFileException, FilmNotFoundException, ClientNotFoundException, FilmExists, ClientExists

class film_repository:
    """
        Clasa creata cu responsabilitatea de a gestiona
        multimea de filme
    """
    def __init__(self):
        self._filme = []
        #self.len=len(self._filme)

    def store_film(self, film):
        """
        Adauga un film in lista
        :param film: filmul care se adauga
        :type film: film
        :return: lista de filme care se modifica prin adaugarea serialului dat
        :rtype:
        """
        all_filme=self.get_all_filme()
        if film in all_filme:
            raise FilmExists()
        self._filme.append(film)

    def get_all_filme(self):
        """
        Returneaza o lista cu toate filmele existente
        """
        return self._filme

    def delete(self, titlu):
        """
        Sterge client dupa cnp
        :param titlu: titlul dat
        :type titlu: str
        :raises: FilmNotFoundException daca id-ul nu exista
        """

        index = -1
        all_filme = self.get_all_filme()
        i = 0
        for f in all_filme:
            if f.get_titlu() == titlu:
                index = i
                break
            i = i + 1
        if index == -1:
            raise FilmNotFoundException()

        deleted_show = self._filme[index]
        del self._filme[index]
        #Best case: filmul cu titlul dat se afla pe pozitia 0 si atunci vom avea complexitatea O(1)
        #Worst case: filmul nu se afla in lista iar atunci lista de filme se va parcurge in intregime, O(n)
        #Average case: filmul se afla in lista pe poz 0,1,2,n-1, atunci aven O(n)
        #Overall: O(n)

    def update(self,titlu,modified_film):
        index = -1
        all_filme = self.get_all_filme()
        i=0
        for f in all_filme:
            if f.get_titlu() == titlu:
                index = i
                break
            i=i+1
        if index == -1:
            raise FilmNotFoundException()
        all_filme[index]=modified_film
        return modified_film

    def inchiriere(self,titlu):
        lista_filme=self.get_all_filme()
        for f in lista_filme:
            if f.get_titlu() == titlu:
                f.set_nr_inchirieri(f.get_nr_inchirieri() + 1)

    def returnare(self,titlu):
        lista_filme = self.get_all_filme()
        for f in lista_filme:
            if f.get_titlu() == titlu:
                f.set_nr_inchirieri(f.get_nr_inchirieri() - 1)

class FilmFileRepo:
    def __init__(self, filename):
        self.__filename = filename

    def __load_from_file(self):
        """
        Incarca datele din fisier
        :return: lista cu filmele din fisier
        :rtype: list of Films
        """

        try:
            f = open(self.__filename, 'r')
            # f = io.open(self.__filename, mode='r', encoding='utf-8')
        except IOError:
            raise CorruptedFileException()

        line = f.readline().strip()
        rez = []
        while line != "":
            attrs = line.split(";")
            f1=film(int(attrs[0]),attrs[1],attrs[2],attrs[3],int(attrs[4]))
            rez.append(f1)
            line = f.readline().strip()
        f.close()
        return rez

    def __save_to_file(self, film_list):
        """
        Salveaza in fisier clientii dati
        :param film_list: lista de filme
        :type film_list: list of Films
        :return: -
        :rtype: -
        """
        with open(self.__filename, 'w') as f:
            for film in film_list:
                film_string = str(film.get_id_f()) + ';' + film.get_titlu() + ';' + str(
                    film.get_descriere())+ ';' + str(film.get_gen())+ ';' +str(film.get_nr_inchirieri()) + '\n'
                f.write(film_string)

    def __save_to_file_raport(self, film_list):
        """
        Salveaza in fisier raportul dat
        :param film_list: lista de filme
        :type film_list: list of Films
        :return: -
        :rtype: -
        """
        with open("data/raport.txt", 'w') as f:
            for film in film_list:
                film_string = str(film.get_id_f()) + ';' + film.get_titlu() + ';' + str(
                    film.get_descriere())+ ';' + str(film.get_gen())+ ';' +str(film.get_nr_inchirieri()) + '\n'
                f.write(film_string)

    def raport(self,film_list):
        """
                Salveaza in fisier raportul dat
                :param film_list: lista de filme
                :type film_list: list of Films
                :return: -
                :rtype: -
                """
        self.__save_to_file_raport(film_list)

    def store_film(self, film):
        """
        Adauga film in lista
        :param film: clientul de adaugat
        :type film: film
        :return: -; lista de filme se modifica prin adaugarea filmului
        :rtype: -; filmul este adaugat
        :raises: DuplicateIDException daca exista deja filmul
        """
        all_filme = self.__load_from_file()
        if film in all_filme:
            raise FilmExists()
        all_filme.append(film)
        self.__save_to_file(all_filme)


    def get_all_filme(self):
        """
        Returneaza o lista cu toate filmele existente
        :rtype: list of objects de tip film
        """
        return self.__load_from_file()


    def delete(self, titlu):
        """
        Sterge film dupa titlu
        :param titlu: titlul dat
        :type titlu: str
        :raises: ClientNotFoundException daca titilul nu exista
        """

        index = -1
        all_filme = self.get_all_filme()
        i=0
        for f in all_filme:
            if f.get_titlu() == titlu:
                index = i
                break
            i=i+1
        if index == -1:
            raise FilmNotFoundException()

        deleted_film = all_filme.pop(index)
        self.__save_to_file(all_filme)

    def update(self,titlu,modified_film):
        index = -1
        all_filme = self.get_all_filme()
        i = 0
        for f in all_filme:
            if f.get_titlu() == titlu:
                index = i
                break
            i = i + 1
        if index == -1:
            raise FilmNotFoundException()
        all_filme[index] = modified_film

        self.__save_to_file(all_filme)
        return modified_film

    def inchiriere(self,titlu):
        lista_filme=self.get_all_filme()
        for f in lista_filme:
            if f.get_titlu() == titlu:
                f.set_nr_inchirieri(f.get_nr_inchirieri() + 1)

        self.__save_to_file(lista_filme)


    def returnare(self,titlu):
        lista_filme = self.get_all_filme()
        for f in lista_filme:
            if f.get_titlu() == titlu:
                f.set_nr_inchirieri(f.get_nr_inchirieri() - 1)

        self.__save_to_file(lista_filme)

    def delete_all(self):
        self.__save_to_file([])

class client_repository:
    """
        Clasa creata cu responsabilitatea de a gestiona
        multimea de clienti
    """
    def __init__(self):
        self._clienti = []

    def store_client(self, client):
        """
        Adauga un client in lista
        :param client: clientul care se adauga
        :type client: client
        :return: lista de clienti care se modifica prin adaugarea serialului dat
        :rtype:
        """
        all_clients=self.get_all_clienti()
        if client in all_clients:
            raise ClientExists()
        self._clienti.append(client)

    def get_all_clienti(self):
        """
        Returneaza o lista cu toti clientii existenti
        """
        return self._clienti

    def delete(self,cnp):
        """
        Sterge client dupa cnp
        :param cnp: cnp-ul dat
        :type cnp: int
        :raises: ClientNotFoundException daca id-ul nu exista
        """

        index = -1
        all_clients = self.get_all_clienti()
        i=0
        for c in all_clients:
            if c.get_cnp() == cnp:
                index = i
                break
            i=i+1
        if index == -1:
            raise ClientNotFoundException()

        deleted_show = self._clienti[index]
        del self._clienti[index]

    def update(self,cnp,modified_client):
        index = -1
        all_clients = self.get_all_clienti()
        i = 0
        for c in all_clients:
            if c.get_cnp() == cnp:
                index = i
                break
            i = i + 1
        if index == -1:
            raise ClientNotFoundException()
        all_clients[index]=modified_client
        return modified_client

    def inchiriere(self,nume):
        lista_clienti=self.get_all_clienti()
        for c in lista_clienti:
            if c.get_nume() == nume:
                c.set_nr_filme_inchiriate(c.get_nr_f() + 1)

    def returnare(self,nume):
        lista_clienti = self.get_all_clienti()
        for c in lista_clienti:
            if c.get_nume() == nume:
                c.set_nr_filme_inchiriate(c.get_nr_f() - 1)


class ClientFileRepo:
    def __init__(self, filename):
        self.__filename = filename

    def __load_from_file(self):
        """
        Incarca datele din fisier
        :return: lista cu clientii din fisier
        :rtype: list of Clients
        """

        try:
            f = open(self.__filename, 'r')
            # f = io.open(self.__filename, mode='r', encoding='utf-8')
        except IOError:
            raise CorruptedFileException()

        line = f.readline().strip()
        rez = []
        while line != "":
            attrs = line.split(";")
            s1 = {'ID': int(attrs[0]), 'Nume': attrs[1], 'CNP': int(attrs[2]), 'Nr. filme inchiriate': int(attrs[3])}
            c1 = client(s1)
            rez.append(c1)
            line = f.readline().strip()
        f.close()
        return rez

    def __save_to_file(self, client_list):
        """
        Salveaza in fisier clientii dati
        :param client_list: lista de clienti
        :type client_list: list of Clients
        :return: -
        :rtype: -
        """
        with open(self.__filename, 'w') as f:
            for client in client_list:
                client_string = str(client.get_id_c()) + ';' + client.get_nume() + ';' + str(
                    client.get_cnp())+ ';' + str(client.get_nr_f()) + '\n'
                f.write(client_string)

    def store_client(self, client):
        """
        Adauga client in lista
        :param client: clientul de adaugat
        :type client: Client
        :return: -; lista de clienti se modifica prin adaugarea clientului
        :rtype: -; clientul este adaugat
        :raises: DuplicateIDException daca exista deja clientul
        """
        all_clients = self.__load_from_file()
        if client in all_clients:
            raise ClientExists()
        all_clients.append(client)
        self.__save_to_file(all_clients)



    def get_all_clienti(self):
        """
        Returneaza o lista cu toti clientii existenti
        :rtype: list of objects de tip Client
        """
        return self.__load_from_file()


    def delete(self, cnp):
        """
        Sterge client dupa cnp
        :param cnp: cnp-ul dat
        :type cnp: int
        :raises: ClientNotFoundException daca id-ul nu exista
        """

        index = -1
        all_clients = self.get_all_clienti()
        i=0
        for c in all_clients:
            if c.get_cnp() == cnp:
                index = i
                break
            i=i+1
        if index == -1:
            raise ClientNotFoundException()

        deleted_client = all_clients.pop(index)
        self.__save_to_file(all_clients)


    def update(self, cnp, modified_client):
        """
        Modifica datele clientului cu id dat
        :return: clientul modificat
        :rtype: client
        :raises: ShowNotFoundException daca nu exista serial cu id dat
        """

        all_clients = self.__load_from_file()
        i = 0
        index=-1
        for c in all_clients:
            if c.get_cnp() == cnp:
                index = i
                break
            i = i + 1
        if index == -1:
            raise ClientNotFoundException()

        all_clients[index] = modified_client

        self.__save_to_file(all_clients)
        return modified_client

    def inchiriere(self,nume):
        lista_clienti=self.get_all_clienti()
        for c in lista_clienti:
            if c.get_nume() == nume:
                c.set_nr_filme_inchiriate(c.get_nr_f() + 1)
        self.__save_to_file(lista_clienti)

    def returnare(self,nume):
        lista_clienti = self.get_all_clienti()
        for c in lista_clienti:
            if c.get_nume() == nume:
                c.set_nr_filme_inchiriate(c.get_nr_f() - 1)
        self.__save_to_file(lista_clienti)

    def delete_all(self):
        self.__save_to_file([])


def test_store_f():
    x=film_repository()
    film1= film(1,"Lord of the Rings", "foarte bun", "Fantasy,Actiune",0)
    x.store_film(film1)
    filme=x.get_all_filme()
    assert (len(filme)==1)
    assert (filme[0]==film1)

def test_store_c():
    x=client_repository()
    s1 = {'ID': 1, 'Nume': "Pop Vasile", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
    c1 = client(s1)
    x.store_client(c1)
    clienti=x.get_all_clienti()
    assert (len(clienti)==1)
    assert (clienti[0]==c1)

test_store_f()
test_store_c()
