# coding:utf-8

import requests
import csv
import json
import sys
import getopt

TITLE = ["date", "username", "email", "project_id", "project_name", "git_path", "branch",
         "hash", "comment_message", "additions", "deletions", "total"]
TITLE2 = ["username", "email", "additions", "deletions", "total"]


"""
1、拿到所有projects
url = ${API_BASE_URL}/projects/

2、拿到单个project的全部分支
url = ${API_BASE_URL}/projects/211/repository/branches

3、拿到单个分支的全部commits
url = ${API_BASE_URL}/projects/211/repository/commits?ref_name=master

4、拿到单个commits的stats
url = ${API_BASE_URL}/projects/211/repository/commits/65508531dcc6c418541a524359adca6d0787de69
"""


def get_all_projects():
    all_commits = dict()
    page = 1
    while True:
        try:
            url = API_BASE_URL + "projects?per_page=100&page=" + str(page)
            page = page + 1

            resp = requests.get(url, headers=HEADERS).json()
            if len(resp) <= 0:
                return all_commits

            for it in resp:
                print(it["path_with_namespace"])
                project_commits = get_project_branch(it["id"], it["path_with_namespace"], it["web_url"])
                all_commits.update(project_commits)
        except Exception as e:
            print(e)
            return all_commits


def get_project_branch(pid, pname, path):
    project_commits = dict()
    try:
        url = API_BASE_URL + "projects/" + str(pid) + "/repository/branches"
        resp = requests.get(url, headers=HEADERS).json()

        for it in resp:
            print("\t\t==>" + it["name"])
            commits = get_branch_commit(pid, pname, path, it["name"])
            project_commits.update(commits)
    except Exception as e:
        print(e)
    return project_commits


def get_branch_commit(pid, pname, path, branch):
    branch_commits = dict()
    page = 1
    while True:
        try:
            url = API_BASE_URL + "projects/" + str(pid) + "/repository/commits?ref_name=" + branch
            if SINCE:
                url = url + "&since=" + SINCE
            if UNTIL:
                url = url + "&until=" + UNTIL
            url = url + "&per_page=100&page=" + str(page)
            page = page + 1

            resp = requests.get(url, headers=HEADERS).json()
            if len(resp) <= 0:
                return branch_commits

            for it in resp:
                comment_message = it["title"]
                if "merge" in comment_message.lower():
                    continue

                commit_stat = get_commit_stat(pid, it["id"])
                commit_stat["project_id"] = pid
                commit_stat["project_name"] = pname
                commit_stat["git_path"] = path
                commit_stat["branch"] = branch
                branch_commits[commit_stat["date"]] = commit_stat
        except Exception as e:
            print(e)
            return branch_commits


def get_commit_stat(pid, commit_hash):
    stat = dict()
    try:
        url = API_BASE_URL + "projects/" + str(pid) + "/repository/commits/" + commit_hash
        resp = requests.get(url, headers=HEADERS).json()
        stat["date"] = resp["created_at"]
        stat["username"] = resp["committer_name"]
        stat["email"] = resp["committer_email"]
        stat["hash"] = resp["id"]
        stat["comment_message"] = resp["title"]
        stat["additions"] = resp["stats"]["additions"]
        stat["deletions"] = resp["stats"]["deletions"]
        stat["total"] = resp["stats"]["total"]
        return stat
    except Exception as e:
        print(e)
        return stat


def write_to_cvs(all_commits):
    f = open("all_commits_%s_%s.csv" % (SINCE, UNTIL), "w")

    all_stats = dict()

    writer = csv.writer(f)
    writer.writerow(TITLE)
    for key in all_commits:
        commit = all_commits[key]
        fulfill_user_stats(all_stats, commit)
        row = []
        for it in TITLE:
            row.append(commit[it])
        writer.writerow(row)

    f.close()

    f = open("all_users_commits_%s_%s.csv" % (SINCE, UNTIL), "w")
    writer = csv.writer(f)
    writer.writerow(TITLE2)
    for key in all_stats:
        commit = all_stats[key]
        row = []
        for it in TITLE2:
            row.append(commit[it])
        writer.writerow(row)

    f.close()


def fulfill_user_stats(all_stats, commit):
    if commit["username"] in all_stats.keys():
        user_commit = all_stats[commit["username"]]
    else:
        user_commit = dict()
        user_commit["username"] = commit["username"]
        user_commit["email"] = commit["email"]
        user_commit["additions"] = 0
        user_commit["deletions"] = 0
        user_commit["total"] = 0
        all_stats[commit["username"]] = user_commit

    user_commit["additions"] += commit["additions"]
    user_commit["deletions"] += commit["deletions"]
    user_commit["total"] += commit["total"]


def init(argv):
    global API_BASE_URL, HEADERS, SINCE, UNTIL
    with open("gitlab_analysis_config.json", "r") as f:
        config = json.load(f)
        API_BASE_URL = config["api_base_url"]
        HEADERS = {
            "Private-Token": config["private_token"]
        }
        SINCE = config["since"]
        UNTIL = config["until"]

    try:
        opts, args = getopt.getopt(argv, "hs:u:", ["help", "since=", "until="])
    except getopt.GetoptError:
        print("Error: %s -s <since> -u <until>" % sys.argv[0])
        print("   or: %s --since=<since> --until=<until>" % sys.argv[0])
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("%s -s <since> -u <until>" % sys.argv[0])
            print("or: %s --since=<since> --until=<until>" % sys.argv[0])
            sys.exit()
        elif opt in ("-s", "--since"):
            SINCE = arg
        elif opt in ("-u", "--until"):
            UNTIL = arg


def main(argv):
    init(argv)
    write_to_cvs(get_all_projects())
    # write_to_cvs(get_branch_commit(211, "test", "test", "master"))


if __name__ == "__main__":
    main(sys.argv[1:])
