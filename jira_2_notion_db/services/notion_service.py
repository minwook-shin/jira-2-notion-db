import time

from notion_database.children import Children
from notion_database.database import Database
from notion_database.page import Page
from notion_database.properties import Properties
from notion_database.query import Direction, Timestamp
from notion_database.search import Search

from jira_2_notion_db.utils.logger_util import LOGGER


class NotionService:
    def __init__(self, notion_key):
        self.notion_key = notion_key

    def __search_database(self, db_name):
        search = Search(integrations_token=self.notion_key)
        search.search_database(query=db_name,
                               sort={"direction": Direction.ascending, "timestamp": Timestamp.last_edited_time})
        LOGGER.info(f"found {len(search.result)} database.")
        return search.result

    def __retrieve_database(self, database_id):
        db = Database(integrations_token=self.notion_key)
        db.retrieve_database(database_id, get_properties=True)
        return db

    @classmethod
    def __set_property(cls):
        notion_property = Properties()
        notion_property.set_title("title")
        notion_property.set_rich_text("key")
        notion_property.set_select("issue_type")
        notion_property.set_select("project_name")
        notion_property.set_select("priority")
        notion_property.set_select("reporter")
        notion_property.set_select("status")
        notion_property.set_date("date")
        return notion_property

    def __create_page(self, database_id, data, delay_time):
        for item in data:
            notion_property = Properties()
            notion_property.set_title("title", item["summary"])
            notion_property.set_rich_text("key", item["key"])
            notion_property.set_select("issue_type", item["issue_type"])
            notion_property.set_select("project_name", item["project_name"])
            notion_property.set_select("priority", item["priority"])
            notion_property.set_select("reporter", item["reporter"])
            notion_property.set_select("status", item["status"])
            notion_property.set_date("date", start=item["create_date"], end=item["resolution_date"])
            # Original URL
            children = Children()
            children.set_heading_1("Original URL")
            children.set_paragraph(item["url"])
            children.set_divider()
            # Parent Issue
            if item["parent"]:
                children.set_heading_1("Parent Issue")
                children.set_paragraph(item["parent"]["key"])
                children.set_paragraph(item["parent"]["summary"])
                children.set_divider()
            # Assignee
            children.set_heading_1("Assignee")
            if item["assignee"]:
                children.set_paragraph(item["assignee"])
            children.set_divider()
            # Description
            children.set_heading_1("Description")
            if item["description"]:
                divide_desc = item["description"].split("\n")
                for line in divide_desc:
                    children.set_paragraph(line)
            children.set_divider()
            # Comment
            children.set_heading_1("Comment")
            if item["comment"]:
                for line in item["comment"]:
                    children.set_paragraph(f'{line["created"]}')
                    children.set_paragraph(f'{line["author"]} : {line["body"]}')
            children.set_divider()
            # Attachment
            children.set_heading_1("Attachment")
            if item["attachment"]:
                for line in item["attachment"]:
                    children.set_paragraph(str(line))
            children.set_divider()
            # Resolution
            if item["resolution_date"]:
                children.set_heading_1("Resolution Date")
                children.set_paragraph(item["resolution_date"])
                children.set_divider()
            # create/update date
            children.set_heading_1("Create/Update Date")
            children.set_paragraph(f'created : {item["create_date"]}')
            children.set_paragraph(f'updated : {item["update_date"]}')

            page = Page(integrations_token=self.notion_key)
            LOGGER.info(f"{item['id']}:{item['summary']}")
            page.create_page(database_id=database_id, properties=notion_property, children=children)
            time.sleep(delay_time)

    def run(self, db_name, data, delay_time=0):
        db_result = self.__search_database(db_name=db_name)
        for i in db_result:
            database_id = i["id"]
            db = self.__retrieve_database(database_id=database_id)
            db.update_database(database_id=database_id, add_properties=self.__set_property())
            self.__create_page(database_id=database_id, data=data, delay_time=delay_time)
