import shutil
import os.path
import git
from subprocess import call
from subprocess import Popen, PIPE
import logging
import uuid
import schedule
import time
import argparse

def parseArguments():
	parser = argparse.ArgumentParser()

	parser.add_argument('-r', '--remote-repository', 
		help='Git remote repository url', required=True)

	parser.add_argument('-e', '--remote-dir', 
		help='Directory where configuration is stored in remote repository (use for dir per environment)', required=True)

	parser.add_argument('-c', '--config-dir', 
		help='Local config directory path', required=True)

	parser.add_argument('-p', '--post-change-command', 
		help='Command to be executed after a configuration change')

	parser.add_argument('-i', '--interval', 
		help='Interval in secounds to verify for remote changes. Default 60',
		default=60, type=int)

	return parser.parse_args()

def need_clone(local_repository):
	return not os.path.exists(local_repository)

def clone_repo(remote_url, local_repository):	
	git.Repo.clone_from(remote_url, local_repository)

def copy_config(local_repository, remote_dir, config_dir):
	copy_repo_dir = local_repository + "/" +remote_dir
	if os.path.exists(config_dir):
		shutil.rmtree(config_dir)

	shutil.copytree(copy_repo_dir, config_dir)

def run_post_change(command):
	call(command, shell=True)

def need_pull(local_repository):
	repo = git.Repo(local_repository)
	git.remote.Remote(repo, 'origin').update()
	commits_behind = sum(1 for c in repo.iter_commits('master..origin/master'))
	if(commits_behind > 0):
		return True

	return False

def pull(local_repository):
	remote = git.remote.Remote(git.Repo(local_repository), 'origin')
	remote.pull()

def create_orc_dir():
	orc_dir = os.path.expanduser("~") + '/.orc'
	if not os.path.exists(orc_dir):
		os.makedirs(orc_dir)
	return orc_dir

def create_local_repository():
	repo_id = str(uuid.uuid4())
	return create_orc_dir() + '/' + repo_id

def ops_remote_config(local_repository, remote_repository, 
	remote_dir, config_dir, post_change_command):	
	
	logging.debug('checking for remote changes')
	try:
		if(need_clone(local_repository)):
			logging.info('cloning new config repo: '+remote_repository)
			clone_repo(remote_repository, local_repository)
			copy_config(local_repository, remote_dir, config_dir)
			run_post_change(post_change_command)

		elif(need_pull(local_repository)):
			logging.info('remote changes found; fetching repository')
			pull(local_repository)
			copy_config(local_repository, remote_dir, config_dir)
			run_post_change(post_change_command)

	except Exception, e:
		logging.error('Fail to load remote config')
		logging.exception(e)

def main():
	logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)	
	
	local_repository = create_local_repository()
	args = parseArguments()

	ops_remote_config(local_repository, args.remote_repository,
		args.remote_dir, args.config_dir, args.post_change_command)

	schedule.every(args.interval).seconds.do(
		ops_remote_config, local_repository, args.remote_repository, 
		args.remote_dir, args.config_dir, args.post_change_command)

	while True:
		schedule.run_pending()
		time.sleep(1)