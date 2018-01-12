from django.db import connection
from django.utils.decorators import ContextDecorator


class NumOfQueries(ContextDecorator):

    def __init__(self, *args, **kwargs):
        self.func_name = kwargs["label"] if kwargs else ""

    def __call__(self, *args, **kwargs):
        self.func_name = args[0].__name__ if args else self.func_name
        return super(NumOfQueries, self).__call__(*args, **kwargs)

    def __enter__(self):
        self.initial_query_count = len(connection.queries)
        return self

    def __exit__(self, *args):
        count = len(connection.queries) - self.initial_query_count
        total_time = reduce(lambda a, b: a + float(b['time']), connection.queries[-count:], 0.0)
        print "For {} {} queries hit".format(self.func_name, count)
        print "Total time taken {}".format(total_time)

        return False
