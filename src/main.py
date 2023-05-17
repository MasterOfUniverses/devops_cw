from tornado.web import RequestHandler, Application
import sympy
import sys
import argparse
from ipaddress import ip_address as ip_type

parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host', type=ip_type, default='127.0.0.1')
parser.add_argument('-p', '--port', type=int, default=9999)
parser.add_argument('-mpn', '--max_prime_num', type=int, default=1000000000)
namespace = parser.parse_args(sys.argv[1:])


def fibonacchi_mod(pos: int) -> str:
    global namespace
    i = 1
    nums = [1, 1]
    while i < pos:
        i += 1
        nums = [nums[1], nums[0] + nums[1]]
    c = str(nums[0])
    if pos == 0:
        c = '0'
    elif pos == -1:
        c = '#'
    return c


def prime_mod(pos: int, force: int) -> str:
    global namespace
    if force == 0:
        if pos > namespace.max_prime_num:
            return ("please, enter number smaller then" +
                    f" {namespace.max_prime_num}" +
                    " or use force-mode /P/n" +
                    " (if you really want to wait so long)")
    if pos > 0:
        c = str(sympy.prime(pos))
    else:
        c = '#'
    return c


class MainHandler(RequestHandler):
    def get(self, data: str) -> None:
        global namespace
        data = str(data)
        mode = data[0]
        if mode == 'f':
            pos = data[2:]
            int_pos = int(pos) - 1
            result = fibonacchi_mod(int_pos)
            self.write({"num": result})
        elif mode == 'p':
            pos = data[2:]
            int_pos = int(pos)
            result = prime_mod(int_pos, 0)
            self.write({"num": result})
        elif mode == 'P':
            pos = data[2:]
            int_pos = int(pos)
            result = prime_mod(int_pos, 1)
            self.write({"num": result})
        else:
            self.write({"hello":
                        ("please, write in address bar /f/n" +
                         " or /p/n to get n-th fibonacchi" +
                         " or prime number"),
                        "warning":
                        ("you can try to calculate n-th" +
                         f" prime number with n>={namespace.max_prime_num}" +
                         " but it is too long and if you really" +
                         " want to do it enter in address bar /P/n")
                        })


app = Application([(r"/([f|p|P]/[0-9]+)?", MainHandler)])
