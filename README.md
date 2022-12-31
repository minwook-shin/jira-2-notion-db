# Jira 2 Notion DB

## Installation

```shell
pip install jira-2-notion-db
```

## Configuration

* Jira login token
* Notion integration token


## Usage

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

## Open source license
[LICENSE](LICENSE)

## Related projects

* https://github.com/minwook-shin/notion-database