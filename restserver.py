
import tornado.escape
import tornado.web
import subprocess
from os.path import expanduser

from codes import LogicErrorCode

#MainHandler for application
class MainHandler(tornado.web.RequestHandler):

    def initialize(self):
        self._logic_funcs = {}
        self._init_logic_funcs()

    #set all real functions in dict of commands by rest name
    def _init_logic_funcs(self):
        result_dict = {}
        result_dict["load_mem"] = MainHandler.load_mem
        result_dict["clear_mem"] = MainHandler.clear_mem
        result_dict["load_cpu"] = MainHandler.load_cpu
        self._logic_funcs = result_dict

    # GET request handler
    def get(self):
        #send main application page
        self.render("index.html")
        return

    # POST request handler
    def post(self):
        request_body = tornado.escape.json_decode(self.request.body)
        response_body = self.process_rest(request_body)
        self.write(response_body)
        return

    # main REST process function
    def process_rest(self, request):

        # initial requests
        command = request.get("command")
        in_args = request.get("args")

        #call command
        try:
            func = self._logic_funcs[command]
        except KeyError:
            err, out_args = LogicErrorCode.INVALID_COMMAND, {}
        else:
            err, out_args = func(in_args)

        # obtain message for error and return result json
        error_message = LogicErrorCode.error_eng_message[err]
        response = {"command": command, "args": out_args,
                    "error_code": err, "error": error_message}
        return response

    # REAL COMMANDS
    # function of loading RAM memory
    def load_mem(args):
        if not isinstance(args, dict):
            raise TypeError("Invalid call add_node in class MainHandler: type of operand 'args' is not dict")

        # obtain command arguments from request: size and kilo/mega/giga modifier
        err = LogicErrorCode.NO_ERROR
        try:
            size = args["size"]
            modifier = args["modifier"]
            
            # check correctness of args
            if not(isinstance(size, int) and isinstance(modifier, str)
                    and (modifier in set(['k', 'm', 'g', 'K', 'M', 'G']) )):
                return (LogicErrorCode.INVALID_ARG, None)

        except (KeyError):
            return (LogicErrorCode.MISS_ARG, None)

        # calculate required memory in kilobytes
        kbyte_size = 0
        if (modifier == 'k') or (modifier == 'K'):
            kbyte_size = size
        elif (modifier == 'm') or (modifier == 'M'):
            kbyte_size = size*1024
        elif (modifier == 'g') or (modifier == 'G'):
            kbyte_size = size*1024*1024
        else:
            return (LogicErrorCode.INVALID_ARG, None)

        # create file in TMPFS directory using 'dd' utility
        count_str = "count="
        count_str += str(kbyte_size)
        subprocess.Popen(["dd", "if=/dev/zero", "of=/tmp/load/load1.bin",
                            "bs=1024", count_str])

        # write size of stored file in kb
        with open('/var/tmp/memsize.txt', 'w+', encoding='utf-8') as f:
            print(str(kbyte_size), file=f)

        return (LogicErrorCode.NO_ERROR, None)

    # function of cleaning loaded memory
    def clear_mem(args):
        if not isinstance(args, dict):
            raise TypeError("Invalid call clear_mem in class MainHandler: type of operand 'args' is not dict")

        # remove stored in TMPFS file
        subprocess.Popen(["rm", "/tmp/load/load1.bin"])

        # write zero as size of stored file
        with open('/var/tmp/memsize.txt', 'w+', encoding='utf-8') as f:
            print("0", file=f)

        return (LogicErrorCode.NO_ERROR, None)

    # function of loading CPU
    def load_cpu(args):
        if not isinstance(args, dict):
            raise TypeError("Invalid call load_cpu in class MainHandler: type of operand 'args' is not dict")

        # obtain command arguments from request:
        # percentage of CPU loading, num of CPU loading and time of loading process
        err = LogicErrorCode.NO_ERROR
        try:
            percentage = args["percentage"]
            time = args["time"]
            cpu_number = args["cpu_number"]

            # check correctness of args
            if not(isinstance(percentage, float) and isinstance(time, int) and isinstance(cpu_number, int) and
                    (cpu_number >= 0) and (time > 0) and (percentage > 0.0) and (percentage <= 1.0) ):
                return (LogicErrorCode.INVALID_ARG, None)

        except (KeyError):
            return (LogicErrorCode.MISS_ARG, None)

        #call CPU loader from home directory
        home = expanduser("~")
        home += "/CPULoadGenerator/"
        subprocess.Popen(["python3", "CPULoadGenerator.py",
                            "-l", str(percentage),
                            "-d", str(time),
                            "-c", str(cpu_number)], cwd=home)

        return (LogicErrorCode.NO_ERROR, None)
