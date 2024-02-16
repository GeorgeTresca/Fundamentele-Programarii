from domain.entities import film,client
from domain.validate import film_validator,client_validator
from repository.firma_repository import film_repository,client_repository, ClientFileRepo, FilmFileRepo
from service.firma_service import firma_service
from ui.console import Console

#rep_film=FilmFileRepo("data/filme.txt")
rep_film = film_repository()
#rep_client=ClientFileRepo("data/clienti.txt")
rep_client=client_repository()
val_film = film_validator()
val_client=client_validator()
srv = firma_service(rep_film,rep_client, val_film,val_client)
ui=Console(srv)
ui.firma_ui()

