import jira

from jira_2_notion_db.utils.logger_util import LOGGER


class JiraService:
    def __init__(self, base_url, username, password):
        self.api = None
        self.base_url = base_url
        self.username = username
        self.password = password

    def login(self):
        self.api = jira.JIRA(server=self.base_url, basic_auth=(self.username, self.password))

    def read_project(self):
        return [x.key for x in self.api.projects()]

    def __search_issue(self, project, only_my_issue):
        base_query = 'project="%s"'
        if only_my_issue:
            base_query += ' AND assignee=currentUser()'
        issues = []
        i = 0
        chunk_size = 100
        LOGGER.info(base_query % project)
        while True:
            query = self.api.search_issues(base_query % project, json_result=True, startAt=i, maxResults=chunk_size)
            i += chunk_size
            LOGGER.info(f"fetching {i} issues.")
            issues.extend(query["issues"])
            total_count = int(query.get('total', 0))
            if i >= total_count:
                LOGGER.info(f"fetched total {total_count} issues.")
                LOGGER.info(f"Done.")
                break
        return issues, total_count

    @classmethod
    def __set_comments_data(cls, issue):
        simple_comments = []
        comments = issue["fields"]["comment"]["comments"]
        for i in comments:
            item = {"id": i["id"], "author": i["author"]["displayName"], "body": i["body"], "created": i["created"]}
            simple_comments.append(item)
        return simple_comments

    @classmethod
    def __set_parent_data(cls, issue):
        if issue["fields"].get("parent", None):
            parent = {'id': issue["fields"]["parent"]["id"], 'key': issue["fields"]["parent"]["key"],
                      'summary': issue["fields"]["parent"]["fields"]["summary"]}
        else:
            parent = None
        return parent

    @classmethod
    def __set_assignee_data(cls, issue):
        if issue["fields"].get("assignee", None):
            assignee = issue["fields"]["assignee"]["displayName"]
        else:
            assignee = "None"
        return assignee

    def __set_issue_url(self, issue):
        return self.base_url + "/browse/" + issue["key"]

    @classmethod
    def __set_attachment_data(cls, issue):
        attachments = issue["fields"].get("attachment", [])
        all_attachments = []
        if attachments:
            for attachment in attachments:
                attachment_data = {'id': attachment["id"],
                                   'filename': attachment["filename"],
                                   'created': attachment["created"],
                                   'size': attachment["size"],
                                   'mimeType': attachment["mimeType"],
                                   'content': attachment["content"]}
                all_attachments.append(attachment_data)
        return all_attachments

    def collect(self, project, only_my_issue=True):
        all_issue = []
        issues, count = self.__search_issue(project=project, only_my_issue=only_my_issue)
        for issue in issues:
            if count:
                simple_comments = self.__set_comments_data(issue=issue)
                parent = self.__set_parent_data(issue=issue)
                assignee = self.__set_assignee_data(issue=issue)
                data = {
                    "id": issue["id"],
                    "key": issue["key"],
                    "url": self.__set_issue_url(issue=issue),
                    "issue_type": issue["fields"]["issuetype"]["name"],
                    "project_name": issue["fields"]["project"]["name"],
                    "resolution_date": issue["fields"]["resolutiondate"],
                    "create_date": issue["fields"]["created"],
                    "update_date": issue["fields"]["updated"],
                    "priority": issue["fields"]["priority"]["name"],
                    "assignee": assignee,
                    "reporter": issue["fields"]["reporter"]["displayName"],
                    "status": issue["fields"]["status"]["name"],
                    "summary": issue["fields"]["summary"],
                    "description": issue["fields"]["description"],
                    "comment": simple_comments,
                    "attachment": self.__set_attachment_data(issue=issue),
                    "parent": parent
                }
                all_issue.append(data)
        return all_issue
