import threading

def run():
    for t in threading.enumerate():
        print(t)
        print(t.name)


if __name__ == '__main__':
    run()