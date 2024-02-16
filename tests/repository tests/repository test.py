import unittest

from domain.entities import client,film
from exceptions import FilmExists,ClientExists, ClientNotFoundException, FilmNotFoundException
from repository.firma_repository import client_repository, ClientFileRepo, film_repository, FilmFileRepo


class TestCaseRepoInMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.client_repo_m = client_repository()
        self.film_repo_m = film_repository()
        self.__add_predefined()


    def __add_predefined(self):
        f1 = film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        f2 = film(2, "Star Wars", "bun", "Sf,Aventura", 0)
        f3 = film(3, "IT", "mediu", "Horror", 0)
        f4 = film(4, "Need for Speed", "peste medie", "Actiune,Aventura", 0)
        f5 = film(5, "Titanic", "excelent", "Drama,Dragoste", 0)

        self.film_repo_m.store_film(f1)
        self.film_repo_m.store_film(f2)
        self.film_repo_m.store_film(f3)
        self.film_repo_m.store_film(f4)
        self.film_repo_m.store_film(f5)

        s1 = {'ID': 1, 'Nume': "Pop Vasile", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
        c1 = client(s1)
        s2 = {'ID': 2, 'Nume': "Raul", 'CNP': 2789015064259, 'Nr. filme inchiriate': 0}
        c2 = client(s2)
        s3 = {'ID': 3, 'Nume': "Andrei", 'CNP': 5123428061234, 'Nr. filme inchiriate': 0}
        c3 = client(s3)
        s4 = {'ID': 4, 'Nume': "George", 'CNP': 5197210642590, 'Nr. filme inchiriate': 0}
        c4 = client(s4)

        self.client_repo_m.store_client(c1)
        self.client_repo_m.store_client(c2)
        self.client_repo_m.store_client(c3)
        self.client_repo_m.store_client(c4)


    def test_get_all(self):
        crt_films = self.film_repo_m.get_all_filme()
        self.assertIsInstance(crt_films, list)
        self.assertEqual(len(crt_films), 5)

        self.film_repo_m.delete("IT")
        self.film_repo_m.delete("Star Wars")

        crt_films = self.film_repo_m.get_all_filme()
        self.assertEqual(len(crt_films), 3)


        crt_clients = self.client_repo_m.get_all_clienti()
        self.assertIsInstance(crt_clients, list)

        self.assertEqual(len(crt_clients), 4)

        self.client_repo_m.delete(2789015064259)
        self.client_repo_m.delete(5123428061234)

        crt_clients = self.client_repo_m.get_all_clienti()
        self.assertEqual(len(crt_clients), 2)

    def test_store(self):
        initial_size_f = len(self.film_repo_m.get_all_filme())
        initial_size_c = len(self.client_repo_m.get_all_clienti())
        film1=film(1, "Lord", "foarte bun", "Fantasy,Actiune", 0)
        self.film_repo_m.store_film(film1)
        self.assertEqual(len(self.film_repo_m.get_all_filme()), initial_size_f + 1)
        self.assertRaises(FilmExists, self.film_repo_m.store_film, film1)
        s0 = {'ID': 1, 'Nume': "Ioana", 'CNP': 5123000004259, 'Nr. filme inchiriate': 0}
        client1 = client(s0)
        self.client_repo_m.store_client(client1)
        self.assertEqual(len(self.client_repo_m.get_all_clienti()), initial_size_c + 1)
        s00 = {'ID': 1, 'Nume': "Daria", 'CNP': 5123012004259, 'Nr. filme inchiriate': 0}
        client2 = client(s00)
        self.client_repo_m.store_client(client2)
        self.assertEqual(len(self.client_repo_m.get_all_clienti()), initial_size_c + 2)
        self.assertRaises(ClientExists, self.client_repo_m.store_client, client2)

    def test_delete(self):
        initial_size_f = len(self.film_repo_m.get_all_filme())
        initial_size_c = len(self.client_repo_m.get_all_clienti())
        self.film_repo_m.delete("Lord of the Rings")
        self.client_repo_m.delete(5123428064259)

        self.assertTrue(len(self.film_repo_m.get_all_filme()) == initial_size_f - 1)
        self.assertTrue(len(self.client_repo_m.get_all_clienti()) == initial_size_c - 1)

        self.assertRaises(FilmNotFoundException, self.film_repo_m.delete, "wxyz")
        self.assertRaises(ClientNotFoundException, self.client_repo_m.delete, 1000000000000)

    def test_update(self):
        film0=film(8,"ABCD","abcde","abcde",0)

        modified_film = self.film_repo_m.update('Titanic', film0)
        self.assertEqual(modified_film.get_titlu(), 'ABCD')
        self.assertEqual(modified_film.get_descriere(), "abcde")
        self.assertEqual(modified_film.get_gen(), "abcde")
        self.assertRaises(FilmNotFoundException, self.film_repo_m.update, '243545', film(20,"aaaaaa",'aaaaaaaa','aaaaaaa',0))

        s0 = {'ID': 1, 'Nume': "Stefan", 'CNP': 5123000994259, 'Nr. filme inchiriate': 0}
        client100 = client(s0)
        modified_client=self.client_repo_m.update(5197210642590,client100)
        self.assertEqual(modified_client.get_nume(),"Stefan")
        self.assertEqual(modified_client.get_cnp(), 5123000994259)
        s9={'ID': 1, 'Nume': "Raul", 'CNP': 8763000994259, 'Nr. filme inchiriate': 0}
        self.assertRaises(ClientNotFoundException, self.client_repo_m.update, 8989898989898,
                          client(s9))

    def test_inchiriere(self):
        film1 = film(1, "Lord", "foarte bun", "Fantasy,Actiune", 0)
        s0 = {'ID': 1, 'Nume': "Ioana", 'CNP': 5123000004259, 'Nr. filme inchiriate': 0}
        client1 = client(s0)
        self.client_repo_m.store_client(client1)
        self.film_repo_m.store_film(film1)
        self.film_repo_m.inchiriere("Lord")
        self.client_repo_m.inchiriere("Ioana")
        self.assertEqual(film1.get_nr_inchirieri(),1)
        self.assertEqual(client1.get_nr_f(),1)


class TestCaseRepoFile(unittest.TestCase):
    def setUp(self) -> None:
        self.client_repo = ClientFileRepo("client_repo_test.txt")
        self.film_repo = FilmFileRepo("film_repo_test.txt")


    def __add_predefined(self):
        f1 = film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        f2 = film(2, "Star Wars", "bun", "Sf,Aventura", 0)
        f3 = film(3, "IT", "mediu", "Horror", 0)
        f4 = film(4, "Need for Speed", "peste medie", "Actiune,Aventura", 0)
        f5 = film(5, "Titanic", "excelent", "Drama,Dragoste", 0)

        self.film_repo.store_film(f1)
        self.film_repo.store_film(f2)
        self.film_repo.store_film(f3)
        self.film_repo.store_film(f4)
        self.film_repo.store_film(f5)

        s1 = {'ID': 1, 'Nume': "Pop Vasile", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
        c1 = client(s1)
        s2 = {'ID': 2, 'Nume': "Raul", 'CNP': 2789015064259, 'Nr. filme inchiriate': 0}
        c2 = client(s2)
        s3 = {'ID': 3, 'Nume': "Andrei", 'CNP': 5123428061234, 'Nr. filme inchiriate': 0}
        c3 = client(s3)
        s4 = {'ID': 4, 'Nume': "George", 'CNP': 5197210642590, 'Nr. filme inchiriate': 0}
        c4 = client(s4)

        self.client_repo.store_client(c1)
        self.client_repo.store_client(c2)
        self.client_repo.store_client(c3)
        self.client_repo.store_client(c4)

    def test_get_all(self):
        self.__add_predefined()
        crt_films = self.film_repo.get_all_filme()
        self.assertIsInstance(crt_films, list)
        self.assertEqual(len(crt_films), 5)

        self.film_repo.delete("IT")
        self.film_repo.delete("Star Wars")

        crt_films = self.film_repo.get_all_filme()
        self.assertEqual(len(crt_films), 3)

        crt_clients = self.client_repo.get_all_clienti()
        self.assertIsInstance(crt_clients, list)

        self.assertEqual(len(crt_clients), 4)

        self.client_repo.delete(2789015064259)
        self.client_repo.delete(5123428061234)

        crt_clients = self.client_repo.get_all_clienti()
        self.assertEqual(len(crt_clients), 2)

        self.client_repo.delete_all()
        self.film_repo.delete_all()

    def test_store(self):
        self.__add_predefined()
        initial_size_f = len(self.film_repo.get_all_filme())
        initial_size_c = len(self.client_repo.get_all_clienti())
        film1 = film(1, "Lord", "foarte bun", "Fantasy,Actiune", 0)
        self.film_repo.store_film(film1)
        self.assertEqual(len(self.film_repo.get_all_filme()), initial_size_f + 1)
        self.assertRaises(FilmExists, self.film_repo.store_film, film1)
        s0 = {'ID': 1, 'Nume': "Ioana", 'CNP': 5123000004259, 'Nr. filme inchiriate': 0}
        client1 = client(s0)
        self.client_repo.store_client(client1)
        self.assertEqual(len(self.client_repo.get_all_clienti()), initial_size_c + 1)
        s00 = {'ID': 1, 'Nume': "Daria", 'CNP': 5123012004259, 'Nr. filme inchiriate': 0}
        client2 = client(s00)
        self.client_repo.store_client(client2)
        self.assertEqual(len(self.client_repo.get_all_clienti()), initial_size_c + 2)
        self.assertRaises(ClientExists, self.client_repo.store_client, client2)

        self.client_repo.delete_all()
        self.film_repo.delete_all()

    def test_delete(self):
        self.__add_predefined()
        initial_size_f = len(self.film_repo.get_all_filme())
        initial_size_c = len(self.client_repo.get_all_clienti())
        self.film_repo.delete("Lord of the Rings")
        self.client_repo.delete(5123428064259)

        self.assertTrue(len(self.film_repo.get_all_filme()) == initial_size_f - 1)
        self.assertTrue(len(self.client_repo.get_all_clienti()) == initial_size_c - 1)

        self.assertRaises(FilmNotFoundException, self.film_repo.delete, "wxyz")
        self.assertRaises(ClientNotFoundException, self.client_repo.delete, 1000000000000)

        self.client_repo.delete_all()
        self.film_repo.delete_all()

    def test_update(self):
        self.__add_predefined()
        film0 = film(8, "ABCD", "abcde", "abcde", 0)

        modified_film = self.film_repo.update('Titanic', film0)
        self.assertEqual(modified_film.get_titlu(), 'ABCD')
        self.assertEqual(modified_film.get_descriere(), "abcde")
        self.assertEqual(modified_film.get_gen(), "abcde")
        self.assertRaises(FilmNotFoundException, self.film_repo.update, '243545',
                          film(20, "aaaaaa", 'aaaaaaaa', 'aaaaaaa', 0))

        s0 = {'ID': 1, 'Nume': "Stefan", 'CNP': 5123000994259, 'Nr. filme inchiriate': 0}
        client100 = client(s0)
        modified_client = self.client_repo.update(5197210642590, client100)
        self.assertEqual(modified_client.get_nume(), "Stefan")
        self.assertEqual(modified_client.get_cnp(), 5123000994259)
        s9 = {'ID': 1, 'Nume': "Raul", 'CNP': 8763000994259, 'Nr. filme inchiriate': 0}
        self.assertRaises(ClientNotFoundException, self.client_repo.update, 8989898989898,
                          client(s9))

        self.client_repo.delete_all()
        self.film_repo.delete_all()

    def test_inchiriere(self):
        self.__add_predefined()
        film99 = film(1, "Lord", "foarte bun", "Fantasy,Actiune", 0)
        s0 = {'ID': 1, 'Nume': "Ioana", 'CNP': 5123000004259, 'Nr. filme inchiriate': 0}
        client1 = client(s0)
        self.client_repo.store_client(client1)
        self.film_repo.store_film(film99)
        self.film_repo.inchiriere("Lord")
        self.client_repo.inchiriere("Ioana")
        index = -1
        all_filme = self.film_repo.get_all_filme()
        i = 0
        for f in all_filme:
            if f.get_titlu() == "Lord":
                self.assertEqual(f.get_nr_inchirieri(), 1)
                break
            i = i + 1
        all_clients = self.client_repo.get_all_clienti()
        i = 0
        for c in all_clients:
            if c.get_cnp() == 5123000004259:
                self.assertEqual(c.get_nr_f(), 1)
                break
            i = i + 1

        self.client_repo.delete_all()
        self.film_repo.delete_all()