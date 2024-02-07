# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.models import AbstractModel

class Persona(AbstractModel):
    _name = 'discografica.persona'
    _description = 'discografica.persona'

    name = fields.Char(string="Nom", required=True)
    surname = fields.Char(string="Cognom", required=True)
    birth_year = fields.Integer(string="Any de naixement", required=True)
    age = fields.Integer(compute='_get_age', string="Edat", store=True)
    contact = fields.Char(string="Contacte")
    dni = fields.Char(string="DNI")
    photo = fields.Image(max_width = 200, max_height=200, string="Foto")

    @api.depends('birth_year')
    def _get_age(self):
        for persona in self:
            persona.age = fields.Datetime.now().year-persona.birth_year


class Cantants(models.Model, Persona):
    _name = 'discografica.cantants'
    _description = 'discografica.cantants'

    contracte = fields.Text(string="Contracte")
    numAlbums = fields.Integer(compute='_compute_numAlbums', store=True)
    numPremis = fields.Integer()
    
    
    albums = fields.One2many('discografica.albums', 'cantant')
    representant = fields.Many2one('discografica.representants')
    events = fields.Many2many('discografica.events')

    @api.depends('albums')
    def _compute_numAlbums(self):
        for cantant in self:
            cantant.numAlbums = len(cantant.albums)
    

    
class Albums(models.Model):
    _name = 'discografica.albums'
    _description = 'discografica.description'

    name = fields.Char(string="Títol", required=True)
    date = fields.Date(string="Data de publicació")
    description = fields.Text(string="Descripció")
    portada = fields.Image(max_width = 200, max_height=200)
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.ref('base.EUR'))
    price = fields.Monetary(string="Preu", currency_field='currency_id')
    duracio_total = fields.Char(string="Duració total", compute='_compute_duracio_total', store=True)
    ventes = fields.Integer(string="Ventes", default=0)
    moneyArreplegat = fields.Monetary(string="Diners arreplegats", currency_field='currency_id', compute='_compute_moneyArreplegat', store=True)
    numSongs = fields.Integer(compute='_compute_numSongs', string="Número Cançons", store=True)
    cantant = fields.Many2one('discografica.cantants')
    song = fields.One2many('discografica.songs', 'album', string="Cançons")
    
    @api.depends('song')
    def _compute_duracio_total(self):
        for album in self:
            album.duracio_total = sum(song.duration_minutes for song in album.song)

    @api.depends('ventes', 'price')
    def _compute_moneyArreplegat(self):
        for album in self:
            album.moneyArreplegat = album.ventes * album.price
    
    @api.depends('song')
    def _compute_numSongs(self):
        for album in self:
            album.numSongs = len(album.song)


class Cançons(models.Model):
    _name = 'discografica.songs'
    _description = 'discografica.songs'

    name = fields.Char(string="Títol", required=True)
    duration_minutes = fields.Float(string="Duració (minuts)", help="Duració de la cançó en minuts")
    duration_display = fields.Char(string="Duració", compute='_compute_duration_display', store=True)
    writers = fields.Text(string="Autors")
    lyrics = fields.Text(string="Lletres")
    partitura = fields.Image(max_width = 200, max_height=200, string="Partitura")


    album = fields.Many2one('discografica.albums')

    @api.depends('duration_minutes')
    def _compute_duration_display(self):
        for song in self:
            minutes = int(song.duration_minutes)
            seconds = int((song.duration_minutes - minutes) * 60)
            song.duration_display = "%d:%02d min" % (minutes, seconds)


class Representants(models.Model, Persona):
    _name = 'discografica.representants'
    _description = 'discografica.representants'

    cantant = fields.One2many('discografica.cantants', "representant")



class Events(models.Model):
    _name = 'discografica.events'
    _description = 'discografica.events'

    name = fields.Char(string="Nom", required=True)
    date = fields.Date(string="Data")
    description = fields.Text(string="Descripció")
    priceTicket = fields.Monetary(string="Preu entrada", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.ref('base.EUR'))
    assistents = fields.Integer()
    location = fields.Char(string="Ubicació")
    moneyArreplegat = fields.Monetary(string="Diners arreplegats", currency_field='currency_id', compute='_compute_moneyArreplegat', store=True)
    type = fields.Selection([('concert', 'Concert'), ('festival', 'Festival'), ('gira', 'Gira'), ('firma discos','Firma discos'), ('altres', 'Altres')], string="Tipus d'event", default='altres')

    cantants = fields.Many2many('discografica.cantants')

    @api.depends('assistents', 'priceTicket')
    def _compute_moneyArreplegat(self):
        for event in self:
            event.moneyArreplegat = event.assistents * event.priceTicket


