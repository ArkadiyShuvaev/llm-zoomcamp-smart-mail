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
    def extract_project_id(self, input_text: str) -> str | None:
        identified_project = self._project_identifier_service.extract_project(input_text)
        if identified_project is None:
            return None

        for project in self._list_of_projects:
            if project.name.lower() == identified_project.name.lower():
                return str(project.id)

    def get_user_authorization_ids(self, email_from: str) -> List[str] | None:
        """
        Retrieves the list of authorization ids for the given email.
        The first implementation retrieves the list of projects in which a user invested for the given email.

        Args:
            email_from (str): The email address of the user.

        Returns:
            List[UUID] | None: The list of authorization resource ids a user has access to.

        """
        user_projects = self.get_user_projects(email_from)
        if len(user_projects) == 0:
            return None

        user_authorization_ids = [str(project.id) for project in user_projects]
        return user_authorization_ids

    # retrieves the list of projects in which a user invested for the given email.
    def get_user_projects(self, user_email: str) -> List[Project]:
        return ProjectsAgent.get_projects_by_email(user_email)

    # retrieves the list of upcoming and delayed repayments for the given email.
    def get_repayments(self, user_email: str) -> List[Dict[str, Any]]:
        return []
