import json
import os

from flask import Blueprint
from flask_testing import TestCase

from app import manager

manager.app.tests_blueprint = Blueprint("tests", __name__)
manager.load_views(manager.app.tests_blueprint, "pysite/views/tests")
manager.app.register_blueprint(manager.app.tests_blueprint)
app = manager.app


class SiteTest(TestCase):
    """ extend TestCase with flask app instantiation """
    def create_app(self):
        """ add flask app configuration settings """
        server_name = 'pytest.local'
        app.config['TESTING'] = True
        app.config['LIVESERVER_TIMEOUT'] = 10
        app.config['SERVER_NAME'] = server_name
        app.config['API_SUBDOMAIN'] = f'http://api.{server_name}'
        app.config['STAFF_SUBDOMAIN'] = f'http://staff.{server_name}'
        app.allow_subdomain_redirects = True
        return app


class BaseEndpoints(SiteTest):
    """ test cases for the base endpoints """
    def test_index(self):
        """ Check the root path reponds with 200 OK """
        response = self.client.get('/', 'http://pytest.local')
        self.assertEqual(response.status_code, 200)

    def test_info_help(self):
        """ Check the info help path responds with 200 OK """
        response = self.client.get('/info/help')
        self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        """ Check paths without handlers returns 404 Not Found """
        response = self.client.get('/nonexistentpath')
        self.assertEqual(response.status_code, 404)

    def test_error(self):
        """ Check the /error/XYZ page """
        response = self.client.get('/error/418')
        self.assertEqual(response.status_code, 418)

    def test_invite(self):
        """ Check invite redirects """
        response = self.client.get('/invite')
        self.assertEqual(response.status_code, 302)

    def test_ws_test(self):
        """ check ws_test responds """
        response = self.client.get('/ws_test')
        self.assertEqual(response.status_code, 200)

    def test_datadog_redirect(self):
        """ Check datadog path redirects """
        response = self.client.get('/datadog')
        self.assertEqual(response.status_code, 302)

    def test_500_easter_egg(self):
        """Check the status of the /500 page"""
        response = self.client.get("/500")
        self.assertEqual(response.status_code, 500)


class ApiEndpoints(SiteTest):
    """ test cases for the api subdomain """
    def test_api_unknown_route(self):
        """ Check api unknown route """
        response = self.client.get('/', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.json, {'error_code': 0, 'error_message': 'Unknown API route'})
        self.assertEqual(response.status_code, 404)

    def test_api_healthcheck(self):
        """ Check healthcheck url responds """
        response = self.client.get('/healthcheck', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.json, {'status': 'ok'})
        self.assertEqual(response.status_code, 200)

    def test_api_tag(self):
        """ Check tag api """
        os.environ['BOT_API_KEY'] = 'abcdefg'
        headers = {'X-API-Key': 'abcdefg', 'Content-Type': 'application/json'}
        good_data = json.dumps({
            'tag_name': 'testing',
            'tag_content': 'testing',
            'tag_category': 'testing'})

        bad_data = json.dumps({
            'not_a_valid_key': 'testing',
            'tag_content': 'testing',
            'tag_category': 'testing'})

        response = self.client.get('/tag', app.config['API_SUBDOMAIN'])
        self.assertEqual(response.status_code, 401)

        response = self.client.get('/tag', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/tag', app.config['API_SUBDOMAIN'], headers=headers, data=bad_data)
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/tag', app.config['API_SUBDOMAIN'], headers=headers, data=good_data)
        self.assertEqual(response.json, {'success': True})

        response = self.client.get('/tag', app.config['API_SUBDOMAIN'], headers=headers, data=good_data)
        self.assertEqual(response.json, [{'tag_name': 'testing'}])
        self.assertEqual(response.status_code, 200)

    def test_api_user(self):
        """ Check insert user """
        os.environ['BOT_API_KEY'] = 'abcdefg'
        headers = {'X-API-Key': 'abcdefg', 'Content-Type': 'application/json'}
        bad_data = json.dumps({'user_id': 1234, 'role': 5678})
        good_data = json.dumps([{'user_id': 1234, 'role': 5678}])

        response = self.client.get('/user', app.config['API_SUBDOMAIN'], headers=headers)
        self.assertEqual(response.status_code, 405)

        response = self.client.post('/user', app.config['API_SUBDOMAIN'], headers=headers, data=bad_data)
        self.assertEqual(response.json, {'error_code': 3, 'error_message': 'Incorrect parameters provided'})

        response = self.client.post('/user', app.config['API_SUBDOMAIN'], headers=headers, data=good_data)
        self.assertEqual(True, "inserted" in response.json)

    def test_api_route_errors(self):
        """ Check api route errors """
        from pysite.base_route import APIView
        from pysite.constants import ErrorCodes

        av = APIView()
        av.error(ErrorCodes.unauthorized)
        av.error(ErrorCodes.bad_data_format)

    def test_not_found(self):
        """ Check paths without handlers returns 404 Not Found """
        response = self.client.get('/nonexistentpath')
        self.assertEqual(response.status_code, 404)


class StaffEndpoints(SiteTest):
    """ Test cases for staff subdomain """
    def test_staff_view(self):
        """ Check staff view renders """
        from pysite.views.staff.index import StaffView
        sv = StaffView()
        result = sv.get()
        self.assertEqual(result.startswith('<!DOCTYPE html>'), True)

        response = self.client.get('/', app.config['STAFF_SUBDOMAIN'])
        self.assertEqual(response.status_code, 200)


class Utilities(SiteTest):
    """ Test cases for internal utility code """
    def test_logging_runtime_error(self):
        """ Check that a wrong value for log level raises runtime error """
        os.environ['LOG_LEVEL'] = 'wrong value'
        try:
            import pysite.__init__  # noqa: F401
        except RuntimeError:
            return True
        finally:
            os.environ['LOG_LEVEL'] = 'info'
        raise Exception('Expected a failure due to wrong LOG_LEVEL attribute name')

    def test_error_view_runtime_error(self):
        """ Check that wrong values for error view setup raises runtime error """
        import pysite.base_route

        ev = pysite.base_route.ErrorView()
        try:
            ev.setup('sdf', 'sdfsdf')
        except RuntimeError:
            return True
        raise Exception('Expected runtime error on setup() when giving wrongful arguments')

    def test_websocket_callback(self):
        """ Check that websocket default callbacks work """
        import pysite.websockets

        class TestWS(pysite.websockets.WS):
            pass

        try:
            TestWS(None).on_message("test")
            return False
        except NotImplementedError:
            return True



class MixinTests(SiteTest):
    """ Test cases for mixins """
    def test_dbmixin_runtime_error(self):
        """ Check that wrong values for error view setup raises runtime error """
        from pysite.mixins import DBMixin

        dbm = DBMixin()
        try:
            dbm.setup('sdf', 'sdfsdf')
        except RuntimeError:
            return True
        raise Exception('Expected runtime error on setup() when giving wrongful arguments')

    def test_dbmixin_table_property(self):
        """ Check the table property returns correctly """
        from pysite.mixins import DBMixin

        try:
            dbm = DBMixin()
            dbm.table_name = 'Table'
            self.assertEquals(dbm.table, 'Table')
        except AttributeError:
            pass

    def test_handler_5xx(self):
        """ Check error view returns error message """
        from werkzeug.exceptions import InternalServerError
        from pysite.views.error_handlers import http_5xx

        error_view = http_5xx.Error500View()
        error_message = error_view.get(InternalServerError)
        self.assertEqual(error_message[1], 500)

    def test_route_view_runtime_error(self):
        """ Check that wrong values for route view setup raises runtime error """
        from pysite.base_route import RouteView

        rv = RouteView()
        try:
            rv.setup('sdf', 'sdfsdf')
        except RuntimeError:
            return True
        raise Exception('Expected runtime error on setup() when giving wrongful arguments')

    def test_route_manager(self):
        """ Check route manager """
        from pysite.route_manager import RouteManager
        os.environ['WEBPAGE_SECRET_KEY'] = 'super_secret'
        rm = RouteManager()
        self.assertEqual(rm.app.secret_key, 'super_secret')


class DecoratorTests(SiteTest):
    def test_decorator_api_json(self):
        """ Check the json validation decorator """
        from pysite.decorators import api_params
        from pysite.constants import ValidationTypes
        from schema import Schema

        SCHEMA = Schema([{"user_id": int, "role": int}])

        @api_params(schema=SCHEMA, validation_type=ValidationTypes.json)
        def try_json_type(data):
            return data

        try:
            try_json_type("not json")
        except Exception as error_message:
            self.assertEqual(type(error_message), AttributeError)

    def test_decorator_params(self):
        """ Check the params validation decorator """

        response = self.client.post('/testparams?test=params')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'test': 'params'}])


class DatabaseTests(SiteTest):
    """ Test cases for the database module """
    def test_table_actions(self):
        import string
        import secrets
        from pysite.database import RethinkDB

        alphabet = string.ascii_letters
        generated_table_name = ''.join(secrets.choice(alphabet) for i in range(8))

        rdb = RethinkDB()
        # Create table name and expect it to work
        result = rdb.create_table(generated_table_name)
        self.assertEquals(result, True)

        # Create the same table name and expect it to already exist
        result = rdb.create_table(generated_table_name)
        self.assertEquals(result, False)

        # Drop table and expect it to work
        result = rdb.drop_table(generated_table_name)
        self.assertEquals(result, True)

        # Drop the same table and expect it to already be gone
        result = rdb.drop_table(generated_table_name)
        self.assertEquals(result, False)

        # This is to get some more code coverage
        self.assertEquals(rdb.teardown_request('_'), None)


class TestWebsocketEcho(SiteTest):
    """ Test cases for the echo endpoint """
    def testEcho(self):
        """ Check rudimentary websockets handlers work """
        from geventwebsocket.websocket import WebSocket
        from pysite.views.ws.echo import EchoWebsocket
        ew = EchoWebsocket(WebSocket)
        ew.on_open()
        ew.on_message('message')
        ew.on_close()
