import shutil
import os.path
import git
from subprocess import call
from subprocess import Popen, PIPE
import logging
import uuid
import schedule
import time

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

local_repository = '/home/rafael/sources/ops-remote-config/repos'

def need_clone(local_repository):
	return not os.path.exists(local_repository)

def clone_repo(remote_url, local_repository):	
	git.Repo.clone_from(remote_url, local_repository)

def copy_config(local_repository, config_dir):
	shutil.rmtree(config_dir)
	shutil.copytree(local_repository, config_dir)

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

def ops_remote_config(local_repository, remote_repository, 
	config_dir, post_change_command):	
	logging.debug('checking for remote changes')
	
	try:
		if(need_clone(local_repository)):
			logging.info('cloning new config repo: '+remote_repository)
			clone_repo(remote_repository, local_repository)
			copy_config(local_repository, config_dir)
			run_post_change(post_change_command)

		elif(need_pull(local_repository)):
			logging.info('remote changes found; fetching repository')
			pull(local_repository)
			copy_config(local_repository, config_dir)
			run_post_change(post_change_command)

	except Exception, e:
		logging.error('Fail to load new sensu server config')
		logging.exception(e)

def main(args):	
	repo_id = str(uuid.uuid4())
	local_repository = local_repository + '/' + repo_id

	ops_remote_config(local_repository, args.remote_repository,
		args.config_dir, args.post_change_command)

	schedule.every(args.interval).seconds.do(
		ops_remote_config, local_repository, args.remote_repository,
			args.config_dir, args.post_change_command)

	while True:
		schedule.run_pending()
		time.sleep(1)	