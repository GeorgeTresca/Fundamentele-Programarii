import unittest
from domain.entities import client,film
from domain.validate import film_validator,client_validator
from repository.firma_repository import client_repository,film_repository
from exceptions import FilmNotFoundException,FilmExists,ClientExists,ClientNotFoundException,ValidationException
from service.firma_service import firma_service

class TestCaseShowService(unittest.TestCase):
    def setUp(self) -> None:
        repo_f = film_repository()
        repo_c=client_repository()
        validator_f = film_validator()
        validator_c=client_validator()
        self.srv = firma_service(repo_f,repo_c,validator_f,validator_c)

    def test_add_film(self):
        film1 = self.srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)

        self.assertEqual(len(self.srv.rep_filme.get_all_filme()),1)
        self.assertEqual (film1.get_titlu(), 'Lord of the Rings')
        self.assertEqual (film1.get_gen() , "Fantasy,Actiune")
        self.assertEqual (film1.get_id_f(), 1)
        self.assertRaises(ValidationException,self.srv.add_film,2, "Star Wars", "0", "abc", 0)

    def test_add_client(self):
        client1 = self.srv.add_client(1, "Pop Vasile", 5123428064259, 0)
        self.assertEqual (len(self.srv.rep_clienti.get_all_clienti()) , 1)
        self.assertEqual (client1.get_nume() ,'Pop Vasile')
        self.assertEqual (client1.get_cnp() , 5123428064259)
        self.assertEqual (client1.get_id_c() , 1)
        self.assertRaises(ValidationException,self.srv.add_client,2,"Pop Vasile",12345 ,0)

    def test_cauta_f(self):
        film1 = self.srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        film2 = self.srv.add_film(1, "The Nun", "ok", "Horror", 0)

        self.assertEqual (self.srv._cauta_f("Lord of the Rings") , film1)
        self.assertEqual (self.srv._cauta_f("Godfather") , "Nu exista filmul cautat")

    def test_cauta_c(self):
        client1 = self.srv.add_client(1, "Pop Vasile", 5123428064259, 0)
        client2 = self.srv.add_client(1, "Pop Ion", 5123428123456, 0)

        self.assertEqual (self.srv._cauta_c("Pop Ion") , client2)
        self.assertEqual (self.srv._cauta_c("George"), "Nu exista clientul cautat")

    def test_get_all_f(self):
        film1 = self.srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        film2 = self.srv.add_film(1, "The Nun", "ok", "Horror", 0)
        self.assertIsInstance(self.srv.get_all_filme(),list)
        self.assertEqual(len(self.srv.get_all_filme()),2)

    def test_get_all_c(self):
        client1 = self.srv.add_client(1, "Pop Vasile", 5123428064259, 0)
        client2 = self.srv.add_client(1, "Pop Ion", 5123428123456, 0)
        self.assertIsInstance(self.srv.get_all_clienti(), list)
        self.assertEqual(len(self.srv.get_all_clienti()), 2)

    def test_mod_f_black(self):
        film1 = self.srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        self.assertEqual(self.srv._mod_film("Lord of the Rings", "Stapanul inelelor", "peste medie",
                                            "Aventura"), "Filmul a fost modificat cu succes")
        self.assertRaises(FilmNotFoundException, self.srv._mod_film, "Lord of the Rings", "Stapanul inelelor",
                          "peste medie", "Aventura")

    def test_mod_f(self):
        film1 = self.srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        self.assertEqual (self.srv._mod_film("Lord of the Rings", "Stapanul inelelor", "peste medie",
                                   "Aventura") , "Filmul a fost modificat cu succes")
        self.assertRaises(FilmNotFoundException,self.srv._mod_film,"Lord of the Rings","Stapanul inelelor", "peste medie", "Aventura")
        self.assertRaises(ValidationException, self.srv._mod_film, "Stapanul inelelor","Lord of the Rings", "xy", "z")

    def test_mod_c(self):
        client1 = self.srv.add_client(1, "Pop Vasile", 5123428064259, 0)
        self.assertEqual(self.srv._mod_client(5123428064259,"Pop Ion",5902518390176), "Clientul a fost modificat cu succes")
        self.assertRaises(ClientNotFoundException, self.srv._mod_client, 5123428064259,"Pop Ion",5035678920108)
        self.assertRaises(ValidationException, self.srv._mod_client, 5902518390176,"AB", 5423577901)

    def test_inchiriere(self):
        film1 = self.srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        client1 = self.srv.add_client(1, "Pop Vasile", 5123428064259, 0)
        self.assertEqual (self.srv.inchiriere("Pop Vasile", "Lord of the Rings") , "Filmul a fost inchiriat cu succes")
        self.assertEqual (self.srv.inchiriere("Pop Vasile", "Star Wars") , "Filmul/clientul nu exista")

    def test_returnare(self):
        film1 = self.srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        client1 = self.srv.add_client(1, "Pop Vasile", 5123428064259, 0)
        self.srv.inchiriere("Pop Vasile", "Lord of the Rings")
        self.assertEqual (self.srv.returnare("Pop Vasile", "Lord of the Rings") , "Filmul a fost returnat cu succes")
        self.assertEqual (self.srv.returnare("Pop Vasile","Lord of the Rings") , "Filmul/clientul nu exista sau filmul nu a fost inchiriat de acel client")

    def test_stergere_f(self):
        self.srv.add_film(1, "abcdefg", "foarte bun", "Fantasy,Actiune", 0)
        self.srv._stergere_film("abcdefg")
        self.assertEqual (len(self.srv.get_all_filme()),0)
        self.assertEqual (self.srv._cauta_f("abcdefg") , "Nu exista filmul cautat")

    def test_stergere_c(self):
        self.srv.add_client(1, "Pop Vasile", 5123428064259, 0)
        self.srv._stergere_client(5123428064259)
        self.assertEqual (len(self.srv.get_all_clienti()),0)
        self.assertEqual (self.srv._cauta_c("Pop Vasile"), "Nu exista clientul cautat")

    def test_clienti_nume(self):
        self.srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        self.srv.add_film(2, "Star Wars", "bun", "Sf,Aventura", 0)
        self.srv.add_film(3, "IT", "mediu", "Horror", 0)
        self.srv.add_film(4, "Need for Speed", "peste medie", "Actiune,Aventura", 0)
        self.srv.add_film(5, "Titanic", "excelent", "Drama,Dragoste", 0)

        self.srv.add_client(1, "Pop Vasile", 5134789562308, 0)
        self.srv.add_client(2, "Pop Ion", 5348913623081, 0)
        self.srv.add_client(3, "Sabou Alexandra", 6134789586408, 0)
        self.srv.add_client(4, "George Tresca", 5134798736129, 0)

        self.srv.inchiriere("Pop Vasile", "Lord of the Rings")
        self.srv.inchiriere("Pop Vasile", "Star Wars")
        self.srv.inchiriere("George Tresca", "Star Wars")
        lst_clienti = self.srv.get_all_clienti()
        l = []
        for c in lst_clienti:
            if c.get_nr_f() > 0:
                l.append(c)

        l = sorted(l, key=lambda i: i['Nume'])
        self.assertEqual (l[0].get_nume() , "George Tresca")
        self.assertEqual (l[1].get_nume() , "Pop Vasile")

    def client_nr_filme(self):
        self.srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        self.srv.add_film(2, "Star Wars", "bun", "Sf,Aventura", 0)
        self.srv.add_film(3, "IT", "mediu", "Horror", 0)
        self.srv.add_film(4, "Need for Speed", "peste medie", "Actiune,Aventura", 0)
        self.srv.add_film(5, "Titanic", "excelent", "Drama,Dragoste", 0)

        self.srv.add_client(1, "Pop Vasile", 5134789562308, 0)
        self.srv.add_client(2, "Pop Ion", 5348913623081, 0)
        self.srv.add_client(3, "Sabou Alexandra", 6134789586408, 0)
        self.srv.add_client(4, "George Tresca", 5134798736129, 0)

        self.srv.inchiriere("Pop Vasile", "Lord of the Rings")
        self.srv.inchiriere("Pop Vasile", "Star Wars")
        self.srv.inchiriere("George Tresca", "Star Wars")
        lst_clienti = self.srv.get_all_clienti()
        l = []
        for c in lst_clienti:
            if c.get_nr_f() > 0:
                l.append(c)

        l = sorted(l, key=lambda i: i['Nr. filme inchiriate'], reverse=True)
        self.assertEqual (l[0].get_nume() , "Pop Vasile")
        self.assertEqual (l[1].get_nume() , "George Tresca")

    def test_cele_mai_inchiriate(self):
        self.srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        self.srv.add_film(2, "Star Wars", "bun", "Sf,Aventura", 0)
        self.srv.add_film(3, "IT", "mediu", "Horror", 0)
        self.srv.add_film(4, "Need for Speed", "peste medie", "Actiune,Aventura", 0)
        self.srv.add_film(5, "Titanic", "excelent", "Drama,Dragoste", 0)

        self.srv.add_client(1, "Pop Vasile", 5134789562308, 0)
        self.srv.add_client(2, "Pop Ion", 5348913623081, 0)
        self.srv.add_client(3, "Sabou Alexandra", 6134789586408, 0)
        self.srv.add_client(4, "George Tresca", 5134798736129, 0)

        self.srv.inchiriere("Pop Vasile", "Lord of the Rings")
        self.srv.inchiriere("Pop Vasile", "Star Wars")
        self.srv.inchiriere("George Tresca", "Star Wars")

        lst_filme = self.srv.get_all_filme()
        l = []
        mx = 0
        for f in lst_filme:
            if f.get_nr_inchirieri() > mx:
                mx = f.get_nr_inchirieri()

        for f in lst_filme:
            if f.get_titlu() == "Star Wars":
                self.assertEqual (f.get_nr_inchirieri() , mx)
            else:
                self.assertNotEqual (f.get_nr_inchirieri() , mx)

        self.srv.inchiriere("George Tresca", "Lord of the Rings")

        for f in lst_filme:
            if f.get_titlu() == "Star Wars" or f.get_titlu() == "Lord of the Rings":
                self.assertEqual (f.get_nr_inchirieri() , mx)
            else:
                self.assertNotEqual (f.get_nr_inchirieri() , mx)

    def test_cele_mai_inchiriate_30(self):
        self.srv.add_film(1, "Lord of the Rings", "foarte bun", "Fantasy,Actiune", 0)
        self.srv.add_film(2, "Star Wars", "bun", "Sf,Aventura", 0)
        self.srv.add_film(3, "IT", "mediu", "Horror", 0)
        self.srv.add_film(4, "Need for Speed", "peste medie", "Actiune,Aventura", 0)
        self.srv.add_film(5, "Titanic", "excelent", "Drama,Dragoste", 0)

        self.srv.add_client(1, "Pop Vasile", 5134789562308, 0)
        self.srv.add_client(2, "Pop Ion", 5348913623081, 0)
        self.srv.add_client(3, "Sabou Alexandra", 6134789586408, 0)
        self.srv.add_client(4, "George Tresca", 5134798736129, 0)

        self.srv.inchiriere("Pop Vasile", "Lord of the Rings")
        self.srv.inchiriere("Pop Vasile", "Star Wars")
        self.srv.inchiriere("George Tresca", "Star Wars")
        l = []
        lst_clienti = self.srv.get_all_clienti()
        for c in lst_clienti:
            if c.get_nr_f() > 0:
                l.append(c)

        l = sorted(l, key=lambda i: i['Nr. filme inchiriate'], reverse=True)
        lungime = int(0.3 * len(l))
        self.assertEqual (lungime , 0)