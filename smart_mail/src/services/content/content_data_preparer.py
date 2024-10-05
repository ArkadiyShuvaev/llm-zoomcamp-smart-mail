from typing import Any, Dict, List
from agents.projects_agent import ProjectsAgent
from dtos.project import Project
from services.content.project_identifier_service import ProjectIdentifierService


class ContentDataPreparer:
    def __init__(self):
        self._list_of_projects: List[Project] = ProjectsAgent.get_projects()
        project_names = [project.name for project in self._list_of_projects]
        self._project_identifier_service = ProjectIdentifierService(project_names)

    # extracts the project from the input text.
    def extract_project(self, input_text: str) -> Project | None:
        identified_project_name = self._project_identifier_service.extract_project_name(input_text)
        if identified_project_name is None:
            return None

        for project in self._list_of_projects:
            if project.name.lower() == identified_project_name.lower():
                return project

    # retrieves the list of projects in which a user invested for the given email.
    def get_user_projects(self, user_email: str) -> List[Project]:
        return ProjectsAgent.get_projects_by_email(user_email)

    # retrieves the list of upcoming and delayed repayments for the given email.
    def get_repayments(self, user_email: str) -> List[Dict[str, Any]]:
        return []
