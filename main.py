import sys, time
import os


def main():
    os.system('python binance.py')
    #os.system('cp binance.csv ~/Desktop/')


if __name__ == '__main__':
    try:
        delay = sys.argv[1].strip() # in seconds
    except:
        delay = ""

    try:
        restart = sys.argv[2].strip()
    except:
        restart = ''

    if restart == '1':
        try:
            os.remove('binance.csv')
        except Exception:
            pass
    
    main()

    for _ in range(50):
        if delay:
            delay = int(delay)
        else:
            delay = 60    

        time.sleep(delay)
        main()

