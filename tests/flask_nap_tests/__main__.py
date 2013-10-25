# -*- coding: utf-8 -*-

from sa_nap import SAModel

from tests.flask_nap_tests.fixtures import app
from tests.fixtures import fixture_loader, Stores, Products, Users, StoreMemberships

from tests.helpers import engine

SAModel.metadata.create_all(engine)

fixture_loader.data(Stores, Users, Products, StoreMemberships).setup()
app.run(host='0.0.0.0', use_reloader=False)
