import unittest

from domain.validate import film_validator, client_validator

from domain.entities import film,client
from exceptions import ValidationException


class TestCaseRatingDomain(unittest.TestCase):
    def setUp(self) -> None:
        self.film_validator = film_validator()
        self.client_validator=client_validator()

    def test_create_film(self):
        film1=film(1,"abcde","abcdef","abcdef",0)

        self.assertEqual(film1.get_id_f(), 1)
        self.assertEqual(film1.get_titlu(), 'abcde')
        self.assertEqual(film1.get_descriere(), 'abcdef')
        self.assertEqual(film1.get_gen(), 'abcdef')
        self.assertEqual(film1.get_nr_inchirieri(),0)

    def test_create_client(self):
        s1 = {'ID': 1, 'Nume': "Pop Vasile", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
        c1 = client(s1)
        self.assertEqual(c1.get_id_c(), 1)
        self.assertEqual(c1.get_nume(), 'Pop Vasile')
        self.assertEqual(c1.get_cnp(), 5123428064259)
        self.assertEqual(c1.get_nr_f(), 0)

    def test_equal(self):
        film1 = film(1, "abcde", "abcdef", "abcdef", 0)
        film2 = film(1, "abcde", "123456", "gvgjshh", 0)
        self.assertEqual(film1, film2)

        film3 = film(1, "wxyz", "123456", "gvgjshh", 0)
        self.assertNotEqual(film3, film2)
        s1 = {'ID': 1, 'Nume': "Pop Vasile", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
        c1 = client(s1)
        s2 = {'ID': 2, 'Nume': "Pop Ion", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
        c2 = client(s2)

        self.assertEqual(c1, c2)

        s3 = {'ID': 2, 'Nume': "Pop Ion", 'CNP': 5123467134099, 'Nr. filme inchiriate': 0}
        c3 = client(s3)
        self.assertNotEqual(c3, c2)

    def test_validator(self):
        film1=film(1,"abcde","abcdef","abcdef",0)
        s1 = {'ID': 1, 'Nume': "Pop Vasile", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
        c1 = client(s1)

        self.__validator = film_validator()
        self.__validator.validate_film(film1)

        film2=film(1,"abcde","a","a",0)
        self.assertRaises(ValidationException, self.__validator.validate_film, film2)