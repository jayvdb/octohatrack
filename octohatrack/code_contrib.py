#!/usr/bin/env python

from .api_helpers import *

"""
Given a repo name, get the "contributors" from the contribution counter
"""
def api_contributors(repo_name):
  contribs = api_walk("repos/%s/contributors" % repo_name)
  return [user_data(c) for c in contribs]

"""
Given a repo name, get all the contributors to all the PR/Issues
"""
def pri_contributors(repo_name):
  contribs = []

  for _type in ["pulls", "issues"]:
    _count= api_get("repos/%s/%s?state=all&page=1&per_page=1" % (repo_name, _type), "number")
    print(_count)

    for i in range(1, _count + 1):
      uri_stub = "/".join(["repos", repo_name, _type, str(i)])
      print(uri_stub)

      start = api_get(uri_stub, key=USER_LOGIN)
      if start:
        print(" - started by %s" % start)
        contribs.append(start)
      else:
        print(uri_stub + " invalid. NEXT")

        break

      users = api_walk(uri_stub + "/comments", key=USER_LOGIN)
      if users:
        print(" - commented on by: " + ",".join(users))
        contribs += users

  contribs = list(set(contribs))
  return [user_data(c) for c in contribs]

"""
from a user_name string, return a user_name/name dict
"""
def user_data(username):
  name = api_get("users/%s" % username, "name")
  return {"user_name": username, "name": name}

