from unittest import TestCase

from aws_lambda_mess.framework.Route import Route, replace_with_regex


class TestRoute(TestCase):
    def test_replace_with_regex(self):
        self.assertEqual(
            "(/.*?)?/users/(?P<name>[a-zA-Z0-9\-_]*)/?",
            replace_with_regex("/users/<name>")
        )

        self.assertEqual(
            "(/.*?)?/users/(?P<name>[a-zA-Z0-9\-_]*)_(?P<surname>[a-zA-Z0-9\-_]*)/?",
            replace_with_regex("/users/<name>_<surname>")
        )

        self.assertEqual(
            "(/.*?)?/users/(?P<name>[a-zA-Z0-9\-_]*)/xxx/?",
            replace_with_regex("/users/<name>/xxx")
        )

        self.assertEqual(
            "(/.*?)?/users/(?P<name>[a-zA-Z0-9\-_]*)/xxx/(?P<surname>[a-zA-Z0-9\-_]*)/?",
            replace_with_regex("/users/<name>/xxx/<surname>")
        )

    def test_init(self):
        method_pattern = "GET"
        path_pattern = "/text"
        handler = lambda params, body: None

        route = Route(method_pattern, path_pattern, handler)

        self.assertEqual(route.method_pattern, method_pattern)
        self.assertEqual(route.path_pattern, replace_with_regex(path_pattern))
        self.assertEqual(route.handler, handler)

    def test_match(self):
        route = Route("GET", "/user/<name>", lambda params, body: None)
        self.assertEqual(
            (True, {"name": "johan"}),
            route.match("GET", "/api/user/johan")

        )
        self.assertEqual(
            (True, {"name": "johan"}),
            route.match("GET", "/user/johan/")
        )
        self.assertEqual(
            (False, None),
            route.match("GET", "/user/johan/xxxx")
        )
        self.assertEqual(
            (False, None),
            route.match("POST", "/user/johan")
        )

        route = Route("PUT", "/user/<name>/stuff/<xxx_zzz>", lambda params, body: None)
        self.assertEqual(
            route.match("PUT", "/user/johan/stuff/12345-77765"),
            (True, {"name": "johan", "xxx_zzz": "12345-77765"})
        )

    def test_run(self):
        def handler(params, body):
            self.assertEqual(body,"Hallo World")
            self.assertEqual(params,{"name": "johan", "xxx_zzz": "12345-77765"})

        route = Route("PUT", "/user/<name>/stuff/<xxx_zzz>", handler)
        match, params = route.match("PUT", "/user/johan/stuff/12345-77765")
        route.run(params, "Hallo World")
