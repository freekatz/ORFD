from multiprocessing import Process
from subprocess import Popen, PIPE
import time

from response import run as run_response

def run():
	response_process = Process(target=run_response)
	response_process.start()

if __name__ == '__main__':
	run()