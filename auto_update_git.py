import os
import datetime
import git
import subprocess
import time

python_bot_subprocess = None

def kill_bot():
  global python_bot_subprocess
  if python_bot_subprocess is not None:
    python_bot_subprocess.kill()

def start_bot():
  global python_bot_subprocess
  python_bot_subprocess = subprocess.Popen(["python3", "python_bot.py"], cwd=os.getcwd())
  time.sleep(5)
  print("Python bot id: " + str(python_bot_subprocess.pid))

def check_for_git_update():
  repo = git.Repo(os.getcwd())
  currentBranch = repo.head.reference
  for remote in repo.remotes:
      remote.fetch()
  commits_behind = repo.iter_commits('master..origin/master')
  count = sum(1 for c in commits_behind)
  if(count > 0):
    kill_bot()
    repo.remotes.origin.pull()
    print("Updated git repo to " + repo.head.reference.commit.hexsha + " @ " + str(datetime.datetime.now()))
    start_bot()

def main():
  start_bot()
  while(1):
    check_for_git_update()
    time.sleep(60)

main()