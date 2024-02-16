from domain.entities import film,client
from exceptions import ValidationException

class film_validator:
    def validate_film(self, film):
        """

        :param film: film
        :type film:film
        :return:
        """
        err = []
        if len(film.get_titlu()) < 2:
            err.append('Titlul filmului trebuie sa aiba minim 2 caractere.')
        if len(film.get_descriere())<2:
            err.append('Descrierea filmului trebuie sa aiba minim 2 caractere.')
        if len(film.get_gen())<5:
            err.append('Descrierea filmului trebuie sa aiba minim 5 caractere.')

        if len(err) > 0:
            #err_string = '\n'.join(err)
            #raise ValueError(err_string)
            raise ValidationException(err)

class client_validator:
    def validate_client(self, client):
        """

        :param client: client
        :type client:client
        :return:
        """
        err = []
        if len(client.get_nume()) < 5:
            err.append('Numele clientului trebuie sa aiba minim 5 caractere.')
        if len(str(client.get_cnp()))!=13:
            err.append('CNP-ul trebuie sa aiba 13 cifre valide!')


        if len(err) > 0:
            #err_string = '\n'.join(err)
            #raise ValueError(err_string)
            raise ValidationException(err)

def test_film_validator():
    test_validator = film_validator()
    film1 = film(1,"Lord of the Rings", "foarte bun", "Fantasy,Actiune",0)
    test_validator.validate_film(film1)
    film2 = film(1,"Lord of the Rings", "x", "Fantasy,Actiune",0)

    try:
        test_validator.validate_film(film2)
        assert False
    except ValueError:
        assert True

    film3 = film(1,"A", "foarte bun", "",0)
    try:
        test_validator.validate_film(film3)
        assert False
    except ValueError:
        assert True

def test_client_validator():
    test_validator = client_validator()
    s1 = {'ID': 1, 'Nume': "Pop Vasile", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
    c1 = client(s1)
    test_validator.validate_client(c1)
    s2 = {'ID': 2, 'Nume': "Pop Ion", 'CNP': 512364259, 'Nr. filme inchiriate': 0}
    c2=client(s2)

    try:
        test_validator.validate_client(c2)
        assert False
    except ValueError:
        assert True

    s3 = {'ID': 3, 'Nume': "A", 'CNP': 5123428064259, 'Nr. filme inchiriate': 0}
    c3 = client(s3)
    try:
        test_validator.validate_client(c3)
        assert False
    except ValueError:
        assert True

#test_film_validator()
#test_client_validator()