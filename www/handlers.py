"""
A collection of template handlers for a simple anonymouse web application.
"""
import json

import tornado.web

from www.anonymity import tor
from www.node import nodehandler


class IndexHandler(tornado.web.RequestHandler):
    """
    Template for Index handlers.
    """
    def get(self):
        self.write('hello world')

@nodehandler
class InfoHandler(tornado.web.RequestHandler):
    """
    Return a JSONObject containing all informations about the node.
    """

    def get(self):
        """
        Fetch the node information from the core in json form, then return it.
        """
        self.write(json.dumps(dict(
            name = self.node.name,
            title = self.node.title,
            description = self.node.description,
            type = self.node.type,
        )))

    def post(self):
        raise tornado.web.HTTPError(501)

    def delete(self):
        raise tornado.web.HTTPError(501)

@nodehandler
class StatsHandler(tornado.web.RequestHandler):
    """
    Display informations about the current tor status.
    """
    def get(self):
        return json.dumps(dict(
            tor_running = bool(torctl),
            hiddenservice_ip = torctl.hiddenip,
        ))

class TipHandler(tornado.web.RequestHandler):
    """
    If a specific submission is requested, return its content (GET)
    If a new submission is created, append it (POST)
    If some material is attached to a submission, map it (PUT)
    If a submission shall be removed, drop it from the database (DELETE)
    """
    def get(self, submission_id):
        pass

class TipStatisticsHandler(tornado.web.RequestHandler):
    """
    Retrive informations about a particular submission.
    """
    def get(self, submission_id):
        pass


class TipCommentsHandler(tornado.web.RequestHandler):
    """
    Retrive comments for a specific submission.
    """

    def get(self, submission_id, comment_id):
        print submission_id, comment_id
        # raise NotImplementedError

class TipMaterialHandler(tornado.web.RequestHandler):
    """
    """

