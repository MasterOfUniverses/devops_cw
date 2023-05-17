from tornado.testing import AsyncHTTPTestCase, gen_test, Application, Generator
import json
import append_paths
import main


print(append_paths.parent_path)


def response_body_parse(body: bytes) -> dict:
    res = json.loads(body.decode('utf8').replace("'", '"'))
    return res


def compare_with_max_num(test_num: int, norm_res: str) -> str:
    if test_num > main.namespace.max_prime_num:
        return ("please, enter number " +
                f"smaller then {main.namespace.max_prime_num}" +
                " or use force-mode /P/n (if you really" +
                " want to wait so long)")
    else:
        return norm_res


class Test_App(AsyncHTTPTestCase):
    def get_app(self) -> Application:
        main.app.listen(main.namespace.port, address=str(main.namespace.host))
        return main.app

    def test_fibonacchi(self) -> None:
        response = self.fetch('/f/0')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "#")
        response = self.fetch('/f/1')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "0")
        response = self.fetch('/f/2')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "1")
        response = self.fetch('/f/7')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "8")
        response = self.fetch('/f/10')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "34")
        response = self.fetch('/f/100')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "218922995834555169026")

    def test_prime(self) -> None:
        test_num = 0
        norm_res = "#"
        response = self.fetch(f'/p/{test_num}')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, compare_with_max_num(test_num, norm_res))
        test_num = 1
        norm_res = "2"
        response = self.fetch(f'/p/{test_num}')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, compare_with_max_num(test_num, norm_res))
        test_num = 10
        norm_res = "29"
        response = self.fetch(f'/p/{test_num}')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, compare_with_max_num(test_num, norm_res))
        test_num = 100
        norm_res = "541"
        response = self.fetch(f'/p/{test_num}')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, compare_with_max_num(test_num, norm_res))
        test_num = 10000
        norm_res = "104729"
        response = self.fetch(f'/p/{test_num}')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, compare_with_max_num(test_num, norm_res))

    def test_forse_Prime(self) -> None:
        response = self.fetch('/P/0')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "#")
        response = self.fetch('/P/1')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "2")
        response = self.fetch('/P/10')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "29")
        response = self.fetch('/P/100')
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "541")

    def test_start(self) -> None:
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        res = response_body_parse(response.body)
        self.assertEqual(str(res["hello"]),
                         ("please, write in address bar /f/n" +
                          " or /p/n to get n-th fibonacchi" +
                          " or prime number"))
        self.assertEqual(str(res["warning"]),
                         ("you can try to calculate n-th prime number" +
                          f" with n>={main.namespace.max_prime_num}" +
                          " but it is too long and if you really" +
                          " want to do it enter in address bar /P/n"""))

    @gen_test(timeout=360.0)
    def test_long_prime(self) -> Generator:
        response = yield self.http_client.fetch(self.get_url('/P/1000000000'),
                                                request_timeout=360.0)
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "22801763489")
        response = yield self.http_client.fetch(self.get_url('/P/1000000001'),
                                                request_timeout=360.0)
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "22801763513")
        test_num = 1000000000
        norm_res = "22801763489"
        response = yield self.http_client.fetch(self.get_url(f'/p/{test_num}'),
                                                request_timeout=360.0)
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, compare_with_max_num(test_num, norm_res))
        test_num = 1000000001
        norm_res = "22801763513"
        response = yield self.http_client.fetch(self.get_url(f'/p/{test_num}'),
                                                request_timeout=360.0)
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, compare_with_max_num(test_num, norm_res))
        response = yield self.http_client.fetch(self.get_url('/P/4000000000'),
                                                request_timeout=360.0)
        self.assertEqual(response.code, 200)
        res = str(response_body_parse(response.body)["num"])
        self.assertEqual(res, "97011687217")
