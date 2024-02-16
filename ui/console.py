
from domain.entities import film,client


def print_menu():
    print(  'Iteratia 1\n\n'
            'GF-Generate filme\n'
            'GC-Generate clienti\n'
            '1-Print filme\n'
            '2-Print clienti\n'
            '3-Add film\n'
            '4-Add client\n'
            '5-Cautare film dupa nume\n'
            '6-Cautare client dupa nume\n\n'
            'Iteratia 2\n\n'
            '7-Modificare film\n'
            '8-Modificare client\n'
            '9-Inchiriere film\n'
            '10-Returnare film\n'
            '11-Stergere film\n'
            '12-Stergere client\n'
            '13-Clienti cu filme inchiriate dupa nume\n'
            '14-Clienti cu filme inchiriate dupa nr. filme\n'
            '15-Cele mai inchiriate filme\n'
            '16-Primii 30% clienti cu cele mai multe filme inchiriate\n'
            '17-Filmele neinchiriate\n'
            '18-Filmele neinchiriate fisier\n'
            '19-Cele mai inchiriate filme recursiv\n'
            '20-Filme neinchiriate recursiv\n'
            '21-Clienti ordonati descrescator dupa nr filme MergeSort\n'
            '22-Clienti ordonati descrescator dupa nr filme BingoSort\n'
            '23-Clienti ordonati descrescator dupa nr filme criterii comb\n'

                  )


class Console:
    def __init__(self, srv):
        """
        Initializeaza consola
        :type srv: firma_service
        """
        self._srv = srv

    def generate_f(self):
        self._srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        self._srv.add_film(2, "Star Wars", "bun", "Sf,Aventura", 0)
        self._srv.add_film(3, "IT", "mediu", "Horror", 0)
        self._srv.add_film(4, "Need for Speed", "peste medie", "Actiune,Aventura", 0)
        self._srv.add_film(5, "Titanic", "excelent", "Drama,Dragoste", 0)

    def generate_c(self):
        self._srv.add_client(1,"Pop Vasile",5134789562308,0)
        self._srv.add_client(2, "Pop Ion", 5348913623081, 0)
        self._srv.add_client(3, "Sabou Alexandra", 6134789586408, 0)
        self._srv.add_client(4, "George Tresca", 5134798736129, 0)

    def _print_all_filme(self):
        """
        Afiseaza toate filmele disponibile
        """
        lst = self._srv.get_all_filme()
        if len(lst) == 0:
            print('Nu exista filme\n')
        else:
            print('Filmele sunt:\n')
            for f in lst:
                print(f)

    def _print_all_clientii(self):
        """
        Afiseaza toti clientii disponibili
        """
        lst = self._srv.get_all_clienti()
        if len(lst) == 0:
            print('Nu exista clienti\n')
        else:
            print('Clientii sunt:\n')
            for c in lst:
                print(c)

    def _add_film(self):
        """
        Adauga un film cu datele citite de la tastatura
        """
        titlu = input("Titlul filmului:")
        descriere=input("Descrierea filmului este:")
        gen=input("Genul filmului este:")

        try:
            id_film=film.get_num_objects()+1
            film_nou = self._srv.add_film(id_film,titlu,descriere, gen,0)
            print('Filmul ' + film_nou.get_titlu() + ' a fost adaugat cu succes\n')
        except ValueError as ve:
            print(str(ve))

    def _add_client(self):
        """
        Adauga un client cu datele citite de la tastatura
        """
        nume = input("Numele clientului:")
        try:
            cnp=int(input("CNP-ul clientului este:"))
        except ValueError:
            print("CNP-ul trebuie sa fie un numar intreg din 15 cifre!\n")
            return
        try:
            id_client=client.get_num_objects()+1
            client_nou = self._srv.add_client(id_client,nume,cnp,0)
            print('Clientul ' + client_nou.get_nume() + ' a fost adaugat cu succes\n')
        except ValueError as ve:
            print(str(ve))

    def _cauta_film(self):
        """
         Cauta un film cu titlul citit de la tastatura
         """
        titlu = input("Titlul filmului:")
        print(self._srv._cauta_f(titlu))

    def _cauta_client(self):
        """
         Cauta un film cu titlul citit de la tastatura
         """
        nume = input("Numele clientului:")
        print(self._srv._cauta_c(nume))

    def _mod_film(self):
        """

        Modifica valorile unui film cu titlul citit de la tastatura
        """
        titlu=input("titlul filmului cautat este:")
        new_title=input("titlul nou este:")
        descriere = input("noua descriere este:")
        gen = input("noul gen este:")
        try:
            print(self._srv._mod_film(titlu,new_title,descriere,gen))
        except ValueError as ve:
            print(str(ve))

    def _mod_client(self):
        """
        Modifica valorile unui client cu numele citit de la tastatura
        """

        try:
            cnp = int(input("cnp-ul clientului cautat este:"))
            nume = input("noul nume este:")
            new_cnp=int(input("noul CNP este:"))
            print(self._srv._mod_client(cnp,nume,new_cnp))
        except ValueError as ve:
            print(str(ve))

    def inchiriere(self):
        """
        Inchiriaza un film unui client
        """
        nume=input("numele clientului este:")
        titlu=input("titlul filmului inchiriat este:")
        print(self._srv.inchiriere(nume,titlu))

    def returnare(self):
        """
        returneaza un film

        """
        nume = input("numele clientului este:")
        titlu = input("titlul filmului inchiriat este")
        print(self._srv.returnare(nume, titlu))

    def _stergere_film(self):
        """
        Sterge din lista un film cu titlul citit de la tastatura
        """
        titlu=input("titlul este:")
        print(self._srv._stergere_film(titlu))

    def _stergere_client(self):
        """
        Sterge din lista de clienti un client cu cnp-ul citit de la tastatura
        """
        try:
            cnp = int(input("cnp-ul este:"))
            print(self._srv._stergere_client(cnp))
        except ValueError as ve:
            print(ve)

    def random_filme(self):
        """
        genereaza o lista de x filme random
        """
        try:
            x=int(input("numarul de filme este:"))
            print(self._srv.random_filme(x))

        except ValueError as ve:
            print(ve)

    def _clienti_nume(self):
        """
        Afiseaza clientii cu filme inchiriate dupa nume
        """
        try:

            self._srv.clienti_nume()

        except ValueError as ve:
            print(ve)

    def _clienti_nr_filme(self):
        """
        Afiseaza clientii cu filme inchiriate dupa nr filme inchiriate
        """
        try:

            self._srv.clienti_nr_filme()

        except ValueError as ve:
            print(ve)

    def clienti_nr_filme_merge(self):
        """
                Afiseaza clientii cu filme inchiriate dupa nr filme inchiriate mergesort
                """
        try:

            self._srv.clienti_nr_filme_merge()

        except ValueError as ve:
            print(ve)

    def clienti_nr_filme_bingo(self):
        """
                Afiseaza clientii cu filme inchiriate dupa nr filme inchiriate bingosort
                """
        try:

            self._srv.clienti_nr_filme_bingo()

        except ValueError as ve:
            print(ve)

    def clienti_nr_filme_comb(self):
        """
                      Afiseaza clientii cu filme inchiriate dupa nr filme inchiriate bingosort
                      """
        try:

            self._srv.clienti_nr_filme_comb()

        except ValueError as ve:
            print(ve)

    def _cele_mai_inchiriate(self):
        try:

            self._srv.cele_mai_inchiriate()

        except ValueError as ve:
            print(ve)

    def cele_mai_inchiriate_rec(self):
        try:
            self._srv.cele_mai_inchiriate_rec(0,0)
        except ValueError as ve:
            print(ve)

    def _cele_mai_inchiriate_30(self):
        try:

            self._srv.cele_mai_inchiriate_30()

        except ValueError as ve:
            print(ve)

    def _filmele_neinchiriate(self):
        try:

            self._srv.filmele_neinchiriate()

        except ValueError as ve:
            print(ve)

    def filme_neinchiriate_rec(self):
        try:
            l=[]
            self._srv.filmele_neinchiriate_rec(0,l)

        except ValueError as ve:
            print(ve)

    def _filme_neinchriate_fisier(self):
        try:

            self._srv.filmele_neinchiriate_fisier()

        except ValueError as ve:
            print(ve)


    def firma_ui(self):

        while True:
            print_menu()
            opt = input('Optiunea este:')
            if opt == '1':
                self._print_all_filme()

            elif opt=='2':
                self._print_all_clientii()

            elif opt=='3':
                self._add_film()

            elif opt=='4':
                self._add_client()

            elif opt=='5':
                self._cauta_film()

            elif opt=='6':
                self._cauta_client()

            elif opt=='7':
                self._mod_film()

            elif opt=='8':
                self._mod_client()

            elif opt=='9':
                self.inchiriere()

            elif opt=='10':
                self.returnare()

            elif opt=='11':
                self._stergere_film()

            elif opt=='12':
                self._stergere_client()

            elif opt=='GF':
                self.generate_f()

            elif opt=='GC':
                self.generate_c()

            elif opt=='RF':
                self.random_filme()

            elif opt=='13':
                self._clienti_nume()

            elif opt=='14':
                self._clienti_nr_filme()

            elif opt=='15':
                self._cele_mai_inchiriate()

            elif opt=='16':
                self._cele_mai_inchiriate_30()

            elif opt=='17':
                self._filmele_neinchiriate()

            elif opt=='18':
                self._filme_neinchriate_fisier()

            elif opt=='19':
                self.cele_mai_inchiriate_rec()

            elif opt=='20':
                self.filme_neinchiriate_rec()

            elif opt=='21':
                self.clienti_nr_filme_merge()

            elif opt=='22':
                self.clienti_nr_filme_bingo()

            elif opt=='23':
                self.clienti_nr_filme_comb()

            else:
                print('Comanda invalida')