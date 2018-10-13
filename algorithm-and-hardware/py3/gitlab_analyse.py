# coding:utf-8

import requests
import csv
import json
import sys
import getopt

TITLE = ["date", "username", "action_name", "project_name", "git_path", "target_type", "comment", "git_branch",
         "commit"]


def get_all_users(state):
    users = []
    page = 1
    while True:
        try:
            url = API_BASE_URL + "users?per_page=100&page=" + str(page)
            resp = requests.get(url, headers=HEADERS).json()
            if len(resp) <= 0:
                return users

            for it in resp:
                if state and state == it["state"]:
                    users.append(it["username"])

            page = page + 1
        except Exception as e:
            print(e)
            return users


def get_user_activities(username):
    activities = []
    page = 1
    while True:
        try:
            url = API_BASE_URL + "users/" + username + "/events?per_page=100&page=" + str(page)
            resp = requests.get(url, headers=HEADERS).json()

            if len(resp) <= 0:
                return activities

            for it in resp:
                activity = {}.fromkeys(TITLE)
                activity["date"] = it["created_at"]
                activity["username"] = it["author_username"]
                activity["action_name"] = it["action_name"]

                pid = it["project_id"]
                if pid:
                    name, path = get_project_name(pid)
                    activity["project_name"] = name
                    activity["git_path"] = path

                if it["target_type"]:
                    activity["target_type"] = it["target_type"]
                    activity["comment"] = it["target_title"]

                if "push_data" in it:
                    push_data = it["push_data"]
                    activity["comment"] = push_data["commit_title"]
                    activity["git_branch"] = push_data["ref"]
                    activity["commit"] = push_data["commit_to"]

                activities.append(activity)

            page = page + 1
        except Exception as e:
            print(e)
            return activities


def get_user_projects(username):
    projects = dict()
    page = 1
    while True:
        try:
            url = API_BASE_URL + "users/" + username + "/events?per_page=100&page=" + str(page)
            resp = requests.get(url, headers=HEADERS).json()

            if len(resp) <= 0:
                return projects

            for it in resp:
                action = it["action_name"]
                if not "pushed" in action:
                    continue
                pid = it["project_id"]
                if pid:
                    name, path = get_project_name(pid)
                    projects[name] = path

            page = page + 1
        except Exception as e:
            print(e)
            return projects


def get_project_name(pid):
    try:
        url = API_BASE_URL + "projects/" + str(pid)
        resp = requests.get(url, headers=HEADERS).json()
        return resp["name"], resp["web_url"]
    except Exception as e:
        print(e)
        return "", ""


def write_to_cvs(username, activities):
    f = open(username + ".csv", "w")

    writer = csv.writer(f)
    writer.writerow(TITLE)
    for activity in activities:
        row = []
        for it in TITLE:
            row.append(activity[it])
        writer.writerow(row)

    f.close()


def get_all_projects():
    projects = []
    page = 1
    while True:
        try:
            url = API_BASE_URL + "projects?per_page=100&page=" + str(page)
            resp = requests.get(url, headers=HEADERS).json()
            if len(resp) <= 0:
                return projects

            for it in resp:
                projects.append(
                    [it["path_with_namespace"], it["web_url"], it["description"], get_contributors(it["id"])])

            page = page + 1
        except Exception as e:
            print(e)
            return projects


def get_contributors(pid):
    contributors = set()
    page = 1
    while True:
        try:
            url = API_BASE_URL + "projects/" + str(pid) + "/events?per_page=100&page=" + str(page)
            resp = requests.get(url, headers=HEADERS).json()
            if len(resp) <= 0:
                return contributors

            for it in resp:
                contributors.add(it["author_username"])

            page = page + 1
        except Exception as e:
            print(e)
            return contributors


def write_to_cvs(projects):
    f = open("projects.csv", "w")

    # pTitle = []

    writer = csv.writer(f)
    # writer.writerow(TITLE)
    for project in projects:
        # row = []
        # for it in TITLE:
        #     row.append(activity[it])
        writer.writerow(project)

    f.close()


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

    f = open("user_projects.csv", "w")
    writer = csv.writer(f)
    writer.writerow(["username", "projects"])
    users = get_all_users("active")
    for user in users:
        print(user)
        projects = get_user_projects(user)
        for k in projects:
            print(k, projects[k])
            writer.writerow([user, k, projects[k]])
    f.close()


if __name__ == "__main__":
    main(sys.argv[1:])
