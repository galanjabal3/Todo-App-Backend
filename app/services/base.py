from typing import Type
from pydantic import BaseModel
from app.utils.logger import logger
from app.utils.other import list_filter_dict_to_list

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
    
    def format_filters(self, filters=None):
        return filters if isinstance(filters, list) else list_filter_dict_to_list(filters=filters or [])

    def get_all_with_filters_and_pagination(self, filters=[], page=1, limit=10, schema_response=None):
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
            datas, pagination = self.repo.get_all_with_filters_and_pagination(
                filters=filters,
                page=page,
                limit=limit
            )
            
            schema = schema_response or self.schema

            if schema:
                datas = [
                    schema.from_orm(obj).model_dump()
                    for obj in datas
                ]
            
            return datas, pagination
        except Exception as e:
            logger.error(f"Err in get_all_with_filters_and_pagination: {e}", exc_info=e)
            raise

    def get_all_with_filters(self, filters=None, schema_response=None):
        """
        Retrieve all records with filters.

        Args:
            filters: A list/dict of filters to apply.

        Returns:
            A list/dict of filtered data.

        Raises:
            Exception: If an error occurs during data retrieval.
        """
        try:
            filters = self.format_filters(filters)
            datas, _ = self.get_all_with_filters_and_pagination(filters=filters, schema_response=schema_response)
            return datas
        except Exception as e:
            logger.error(f"Err in get_all_with_filters: {e}", exc_info=e)
            raise

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
            raise

    def get_one_by_filters(self, filters=None, to_model=False, schema_response=None):
        """
        Retrieve a single record matching the filters.

        Args:
            filters: A list/dict of filters to apply.

        Returns:
            The record matching the filters.

        Raises:
            Exception: If an error occurs during data retrieval.
        """
        try:
            filters = self.format_filters(filters)
            datas = self.repo.get_one_by_filters(filters)
            if not datas:
                return None
            
            if to_model:
                return datas
            
            schema = schema_response or self.schema
            if schema:
                datas = schema.from_orm(datas).model_dump()
            
            return datas
        except Exception as e:
            logger.error(f"Err in get_one_by_filters: {e}", exc_info=e)
            raise

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
            new_record = self.repo.create(data)
            validated_data = self.schema.model_validate(new_record)
            return validated_data.model_dump()
        except Exception as e:
            logger.error(f"Err in create: {e}", exc_info=e)
            raise

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
            datas = self.repo.update(data)
            return self.schema.from_orm(datas).model_dump()
        except Exception as e:
            logger.error(f"Err in update: {e}", exc_info=e)
            raise
    
    def update_one_with_filters(self, filters=None, data: dict = {}):
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
            filters = self.format_filters(filters)
            datas = self.repo.update_one_with_filters(filters, data)
            if not datas:
                return datas

            return self.schema.from_orm(datas).model_dump()
        except Exception as e:
            logger.error(f"Err in update_one_with_filters: {e}", exc_info=e)
            raise

    def delete_by_id(self, id, soft_delete=True):
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
            return self.repo.delete_by_id(id, soft_delete=soft_delete)
        except Exception as e:
            logger.error(f"Err in delete_by_id: {e}", exc_info=e)
            raise
