from app import app
import sys
from app.functions import __init_db__, __run_db__, __drop_db__, __create_db__
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "run" or sys.argv[1] == "start" or sys.argv[1] == "go":
            __run_db__()
            app.run(debug=True)
        elif sys.argv[1] == "drop":
            __drop_db__()
            pass
        elif sys.argv[1] == "create":
            __create_db__()
            pass
        elif sys.argv[1] == "init":
            __drop_db__()
            __create_db__()
            __init_db__()
        else:
            app.run(debug=True)
    else:
        app.run(debug=True)

