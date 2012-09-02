# -*- coding: utf-8 -*-

import logging
from pyramid.view import view_config
from webhelpers import paginate


from anuket.models import DBSession
from begotemp.models.rock import Rock


log = logging.getLogger(__name__)


def includeme(config):

    config.add_route('rock_list', '/rock')
    config.add_route('rock_add', '/rock/add')


@view_config(route_name='rock_list', permission='admin',
             renderer='/rock/rock_list.mako')
def rock_list_view(request):

    _ = request.translate
    stats=None

    # construct the query
    rocks = DBSession.query(Rock)
    rocks = rocks.order_by(Rock.rock_number)
    # add a flash message for empty results
    if rocks.count() == 0:
        request.session.flash(_(u"There is no results!"), 'error')

    # paginate results
    page_url = paginate.PageURL_WebOb(request)
    rocks = paginate.Page(rocks,
                          page=int(request.params.get("page", 1)),
                          items_per_page=20,
                          url=page_url)

    return dict(rocks=rocks, stats=stats)


from begotemp.forms import RockForm

@view_config(route_name='rock_add', permission='admin',
             renderer='/rock/rock_add.mako')
def rock_add_view(request):

    _ = request.translate
    form = RockForm(request.POST)
    if request.method == 'POST' and form.validate():
        pass

    return dict(form=form)




#TODO change 'rock' to 'geo_rock' 'geo/rock' ?