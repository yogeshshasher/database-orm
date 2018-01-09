from time import time

from django.db import connection


class NumOfQueries(object):
    def __init__(self, label):
        self.label = label

    def __enter__(self):
        self.initial_query_count = len(connection.queries)

    def __exit__(self, *args):
        count = len(connection.queries) - self.initial_query_count
        total_time = reduce(lambda a, b: a + float(b['time']), connection.queries[-count:], 0.0)
        print "For {} {} queries hit".format(self.label, count)
        print "Total time taken {}".format(total_time)