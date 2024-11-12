from typing import Any, Dict, List

from data_loaders.projects_loader import ProjectsLoader
from dtos.identified_project import IdentifiedProject
from dtos.project import Project
from services.content.project_identifier_service import ProjectIdentifierService


class ContentDataPreparer:
    def __init__(self):
        self._list_of_projects = ProjectsLoader.get_projects()
        self._project_identifier_service = ProjectIdentifierService(self._list_of_projects)

    def extract_project(self, input_text: str) -> IdentifiedProject | None:
        """ Extracts the project from the input text. """

        identified_project = self._project_identifier_service.extract_project(input_text)
        return identified_project

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

        user_authorization_ids = [str(project.id).upper() for project in user_projects]
        return user_authorization_ids

    # retrieves the list of projects in which a user invested for the given email.
    def get_user_projects(self, user_email: str) -> List[Project]:
        return ProjectsLoader.get_projects_by_email(user_email)

    # retrieves the list of upcoming and delayed repayments for the given email.
    def get_repayments(self, user_email: str) -> List[Dict[str, Any]]:
        return []
