from typing import Type
from pydantic import BaseModel
from app.utils.logger import logger

class BaseService:
    """
    BaseService provides a generic service layer for interacting with repositories and schemas.

    Attributes:
        repository: The default repository to be used by the service.
        schema_class: The default schema class to be used for data serialization/deserialization.
    """
    repository = None
    schema_class = None

    def __init__(self, repository=None, schema_class: Type[BaseModel] = None):
        """
        Initialize the BaseService with a repository and schema class.

        Args:
            repository: An instance of the repository to interact with the database.
            schema_class: A Pydantic model class for data validation and serialization.

        Raises:
            ValueError: If no repository is provided.
        """
        self.repo = repository or self.repository
        self.schema = schema_class or self.schema_class
        
        if not self.repo:
            raise ValueError("Repository must be provided")

    def get_all_with_filters_and_pagination(self, filters=[], page=1, limit=10, to_response="to_response"):
        """
        Retrieve all records with filters and pagination.

        Args:
            filters: A list of filters to apply.
            page: The page number for pagination.
            limit: The number of records per page.
            to_response: The method to transform data to response format.

        Returns:
            A tuple containing the filtered data and pagination details.

        Raises:
            Exception: If an error occurs during data retrieval.
        """
        try:
            datas, pagination = self.repo.get_all_with_filters_and_pagination(filters=filters, page=page, limit=limit)
            if datas:
                datas = [self.schema.from_orm(x).model_dump() for x in datas]
            
            return datas, pagination
        except Exception as e:
            logger.error(f"Err in get_all_with_filters_and_pagination: {e}", exc_info=e)
            raise e

    def get_all_with_filters(self, filters=[]):
        """
        Retrieve all records with filters.

        Args:
            filters: A list of filters to apply.

        Returns:
            A list of filtered data.

        Raises:
            Exception: If an error occurs during data retrieval.
        """
        try:
            datas, _ = self.get_all_with_filters_and_pagination(filters=filters)
            return datas
        except Exception as e:
            logger.error(f"Err in get_all_with_filters: {e}", exc_info=e)
            raise e

    def get_by_id(self, id):
        """
        Retrieve a record by its ID.

        Args:
            id: The ID of the record to retrieve.

        Returns:
            The record with the specified ID.

        Raises:
            Exception: If an error occurs during data retrieval.
        """
        try:
            return self.repo.get_by_id(id)
        except Exception as e:
            logger.error(f"Err in get_by_id: {e}", exc_info=e)
            raise e

    def get_one_by_filters(self, filters=[]):
        """
        Retrieve a single record matching the filters.

        Args:
            filters: A list of filters to apply.

        Returns:
            The record matching the filters.

        Raises:
            Exception: If an error occurs during data retrieval.
        """
        try:
            return self.repo.get_one_by_filters(filters)
        except Exception as e:
            logger.error(f"Err in get_one_by_filters: {e}", exc_info=e)
            raise e

    def create(self, data):
        """
        Create a new record.

        Args:
            data: The data for the new record.

        Returns:
            The created record.

        Raises:
            Exception: If an error occurs during record creation.
        """
        try:
            return self.repo.create(data)
        except Exception as e:
            logger.error(f"Err in create: {e}", exc_info=e)
            raise e

    def update(self, data):
        """
        Update an existing record.

        Args:
            data: The updated data for the record.

        Returns:
            The updated record.

        Raises:
            Exception: If an error occurs during record update.
        """
        try:
            return self.repo.update(data)
        except Exception as e:
            logger.error(f"Err in update: {e}", exc_info=e)
            raise e

    def delete(self, id, soft_delete=True):
        """
        Delete a record by its ID.

        Args:
            id: The ID of the record to delete.
            soft_delete: Whether to perform a soft delete (default: True).

        Returns:
            The result of the delete operation.

        Raises:
            Exception: If an error occurs during record deletion.
        """
        try:
            return self.repo.delete(id, soft_delete=soft_delete)
        except Exception as e:
            logger.error(f"Err in delete: {e}", exc_info=e)
            raise e
