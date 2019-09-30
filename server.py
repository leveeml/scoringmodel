import conf
import src
import json
import logging
import os
import pandas as pd
import tornado.ioloop
import tornado.web
from conf import Logger
from tornado.log import enable_pretty_logging

symdf = src.load_similarity_data()

def score(data):
    scores = pd.DataFrame(data)
    scores = src.calculate_scores(src.get_similarities(scores,symdf))
    scores["model"] = "similarity"
    scores["version"] = "1.0.0"
    return scores[["candidate_id", "job_id", "score", "model", "version"]]


class ScoreHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        self.set_header("Content-Type", "application/json")
        self.write(score(data).to_json(orient="records"))

class PingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("OK")

def make_app():
    return tornado.web.Application(
        [
            (r"/score/invocations", ScoreHandler),
            (r"/score/healthcheck", PingHandler),
        ]
    )

if __name__ == "__main__":
    try:
        app = make_app()
        app.listen(int(conf.PORT))
        enable_pretty_logging(logger=Logger)
        Logger.info("Listening on port %s", conf.PORT)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Exiting")
