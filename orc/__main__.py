"""orc.__main__: executed when orc directory is called as script."""

import argparse
from .orc import main

main(parseArguments())


def parseArguments():
	parser = argparse.ArgumentParser()

	parser.add_argument('-r', '--remote-repository', 
		help='Git remote repository url', required=True)

	parser.add_argument('-c', '--config-dir', 
		help='Local config dir path', required=True)

	parser.add_argument('-p', '--post-change-command', 
		help='Command to be executed after a remote repository change',
		required=True)

	parser.add_argument('-i', '--interval', 
		help='Interval in secounds to verify for remote changes. Default 60',
		default=60, type=int)

	return parser.parse_args()