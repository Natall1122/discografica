# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.models import AbstractModel

class Persona(AbstractModel):
    _name = 'discografica.persona'
    _description = 'discografica.persona'

    name = fields.Char()
    surname = fields.Char()
    birth_year = fields.Integer()
    age = fields.Integer(compute='get_age', store=True)
    contact = fields.Char()
    dni = fields.Char(string="DNI")

    @api.depends('birth_year')
    def _get_age(self):
        for persona in self:
            persona.age = fields.Datetime.now().year-persona.birth_year



class Cantants(models.Model, Persona):
    _name = 'discografica.cantants'
    _description = 'discografica.cantants'

    photo = fields.Image(max_width = 200, max_height=200)
    contracte = fields.Text()
    numAlbums = fields.Integer(compute='_compute_numAlbums', store=True)
    numPremis = fields.Integer()
    
    
    albums = fields.One2many('discografica.albums', 'cantant')
    representant = fields.Many2one('discografica.representants')
    events = fields.Many2many('discografica.events')

    @api.depends('albums')
    def _compute_numAlbums(self):
        for cantant in self:
            cantant.numAlbums = len(cantant.albums)
    
    @api.depends('birth_year')
    def _get_age(self):
        for cantant in self:
            cantant.age = fields.Datetime.now().year-cantant.birth_year


    
class Albums(models.Model):
    _name = 'discografica.albums'
    _description = 'discografica.description'

    title = fields.Char()
    date = fields.Date()
    description = fields.Text()
    portada = fields.Image(max_width = 200, max_height=200)
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.ref('base.EUR'))
    price = fields.Monetary(string="Preu", currency_field='currency_id')
    duracio_total = fields.Float(string="Duració total", compute='_compute_duracio_total', store=True)
    ventes = fields.Integer()
    moneyArreplegat = fields.Monetary(string="Diners arreplegats", currency_field='currency_id', compute='_compute_moneyArreplegat', store=True)
    numSongs = fields.Integer(compute='_compute_numSongs', store=True)
    cantant = fields.Many2one('discografica.cantants')
    song = fields.One2many('discografica.songs', 'album')
    

    @api.depends('song.duration_minutes')
    def _compute_duracio_total(self):
        for album in self:
            album.duracio_total = sum(album.song.mapped('duration_minutes'))
            album.duracio_total = "%d:%02d min" % (int(album.duracio_total), int((album.duracio_total - int(album.duracio_total)) * 60))

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

    title = fields.Char()
    duration_minutes = fields.Float(string="Duració (minuts)", help="Duració de la cançó en minuts")
    duration_display = fields.Char(string="Duració", compute='_compute_duration_display', store=True)
    writers = fields.Text()

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

    photo = fields.Image(max_width = 200, max_height=200)
    cantant = fields.One2many('discografica.cantants', "representant")

    @api.depends('birth_year')
    def _get_age(self):
        for representant in self:
            representant.age = fields.Datetime.now().year-representant.birth_year


class Events(models.Model):
    _name = 'discografica.events'
    _description = 'discografica.events'

    name = fields.Char()
    date = fields.Date()
    description = fields.Text()
    priceTicket = fields.Monetary(string="Preu entrada", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.ref('base.EUR'))
    assistents = fields.Integer()
    location = fields.Char()
    moneyArreplegat = fields.Monetary(string="Diners arreplegats", currency_field='currency_id', compute='_compute_moneyArreplegat', store=True)
    type = fields.Selection([('concert', 'Concert'), ('festival', 'Festival'), ('gira', 'Gira'), ('firma discos','Firma discos'), ('altres', 'Altres')], string="Tipus d'event", default='altres')

    cantants = fields.Many2many('discografica.cantants')

    @api.depends('assistents', 'priceTicket')
    def _compute_moneyArreplegat(self):
        for event in self:
            event.moneyArreplegat = event.assistents * event.priceTicket


