# Jira 2 Notion DB

Jira issue to Notion database Migration Tool

## Installation

```shell
pip install jira-2-notion-db
```

## Configuration

* Jira login token
* Notion integration token


## CLI Usage

should be able to find Notion db using Jira project name.

```shell
jira-2-notion-db --url "https://your.atlassian.net" --username "your@mail.com" --password "yourAtlassianToken" --project "PJ" --notion "yourNotionIntegrationToken"
```

* arguments:
  * --url URL
    * Jira url ex) https://your.atlassian.net
  * --username
    * Jira username
  * --password
    * Jira api token (Not Password)
  * --project
    * Jira project name
  * --notion
    * Notion integration bot token
  * --delay
    * Notion update delay


## Python Usage

```python
# jira
from jira_2_notion_db.services.jira_service import JiraService
jira = JiraService(base_url="https://your.atlassian.net", username="username", password="password")
all_projects = jira.read_project()
jira.login()
jira_contents = jira.collect(project="PJ", only_my_issue=False)

# notion
from jira_2_notion_db.services.notion_service import NotionService
notion = NotionService(notion_key="notionToken")
notion.run(db_name="PJ", data=jira_contents, delay_time=1)
```

## Open source license
[LICENSE](LICENSE)

## Related projects

* https://github.com/minwook-shin/notion-database