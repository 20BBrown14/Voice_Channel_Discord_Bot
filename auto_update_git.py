import os
import datetime
import git
import subprocess
import time

global python_bot_pid

def kill_bot():
  global python_bot_pid
  if(python_bot_pid > 0):
    subProcess = subprocess.call(["kill", "-9", str(python_bot_pid)], cwd=os.getcwd())


def start_bot():
  global python_bot_pid
  subProcess = subprocess.Popen(["python3", "python_bot.py"], cwd=os.getcwd())
  time.sleep(5)
  python_bot_pid = subProcess.pid
  print("Python bot id: " + str(python_bot_pid))

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
  global python_bot_pid
  python_bot_pid = -1
  start_bot()
  while(1):
    check_for_git_update()
    time.sleep(60*30)

main()



