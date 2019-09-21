# Charset utf-8

class LogicErrorCode:
    NO_ERROR = 0
    MISS_ARG = 1
    INVALID_ARG = 2
    INVALID_COMMAND = 3

    error_eng_message = {}

    error_eng_message[NO_ERROR] = ""
    error_eng_message[MISS_ARG] = "Missing argument"
    error_eng_message[INVALID_ARG] = "Invalid argumnet or its type"
    error_eng_message[INVALID_COMMAND] = "Don't exist command with this name"
