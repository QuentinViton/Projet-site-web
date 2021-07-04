from logging import Manager
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, url_for

from models import *

app = Flask(__name__)

bootstrap = Bootstrap(app)


#Page d'accueil affichant les artistes, les albums et les genres
@app.route('/')
@app.route('/accueil')
def page_accueil():
    query_artistes = Artists.select()
    query_albums = Albums.select()
    query_genres = Genres.select()

    return render_template('accueil.html', artistes=query_artistes, albums=query_albums, genres=query_genres)


#Page artiste affichant les infos relative à un artiste en particulier
#id_artiste représente l'id de l'artiste dans la base de données que l'on doit afficher
@app.route('/artiste/<id_artiste>')
def page_artiste(id_artiste):
    #select les infos à partir de id_artiste
    query_artiste = Artists.select().where(Artists.artist_id == id_artiste)
    
    query_albums = Albums.select().where(Albums.artist == id_artiste)



    return render_template('artiste.html', artiste=query_artiste[0], albums=query_albums )


#Page album affichant les infos relative à un album en particulier
#id_album représente l'id de l'album dans la base de données que l'on doit afficher
@app.route('/album/<id_album>')
def page_album(id_album):
    #select les infos à partir de id_album
    query_album = Albums.select().where(Albums.album_id == id_album)

    query_tracks = Tracks.select().where(Tracks.album == id_album)

    return render_template('album.html', album=query_album[0], tracks=query_tracks)


#Page genre affichant les infos relatives à un genre en particulier
#id_genre représente l'id du genre dans la base de données que l'on doit afficher
@app.route('/genre/<id_genre>')
def page_genre(id_genre):
    #select les infos à partir de id_genre
    query_genre = Genres.select().where(Genres.genre_id == id_genre)

    query_tracks = Tracks.select().where(Tracks.genre == id_genre)

    return render_template('genre.html', genre=query_genre[0], tracks=query_tracks)


#Page clients affichant les différents clients
@app.route('/clients')
def page_clients():
    #select les infos des clients
    query_clients = Customers.select()

    return render_template('clients.html', clients=query_clients)


#Page client affichant les infos relatives à un client en particulier
#id_client représente l'id du client dans la base de données que l'on doit afficher
@app.route('/client/<id_client>')
def page_client(id_client):
    #select les infos du client
    query_client = Customers.select().where(Customers.customer_id == id_client)

    query_commandes = Invoices.select().where(Invoices.customer == id_client)


    return render_template('client.html', client=query_client[0], commandes=query_commandes)


#Page commande affichant les infos relatives à une commande en particulier
#id_commande représente l'id du client dans la base de données que l'on doit afficher
@app.route('/commande/<id_commande>')
def page_commande(id_commande):
    #select les infos de la commande
    query_commande = Invoices.select().where(Invoices.invoice_id==id_commande).dicts()
    query_items=InvoiceItems.select(InvoiceItems.quantity, InvoiceItems.unit_price, Tracks.name).join(Tracks).where(InvoiceItems.invoice == id_commande).dicts()

    return render_template('commande.html', commande=query_commande[0], items=query_items)


#Page employes affichant la liste des employés
@app.route('/employes')
def page_employes():
    query_employes = Employees.select()
    
    return render_template('employes.html', employes=query_employes)

#Page employe affichant les infos relatives à un employé en particulier
#id_employe représente l'id de l'employé dans la base de données que l'on doit afficher
@app.route('/employe/<id_employe>')
def page_employe(id_employe):
    Managers=Employees.alias()
    query_employe = (Employees
                    .select(Employees.first_name, Employees.last_name, Employees.reports_to,
                     Managers.first_name.alias("manager_first_name"),
                     Managers.last_name.alias("manager_last_name") )
                     .where(Employees.employee_id==id_employe)
                     .join(Managers, JOIN.LEFT_OUTER, on=(Managers.employee_id==Employees.reports_to))).dicts()

    query_clients = Customers.select().where(Customers.support_rep==id_employe)



    return render_template('employe.html', employe=query_employe[0], clients=query_clients)


#Page nouvelle-commande permettant de créer une commande
#A FAIRE



if __name__ == "__main__":
    app.run(debug=True)