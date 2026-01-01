import math
from pony.orm import db_session, select
from app.utils.logger import logger

class BaseRepository:
    """
    BaseRepository provides a generic repository layer for interacting with the database.

    Attributes:
        entity: The database entity (model) associated with this repository.
        filter_map: A mapping of fields to their respective filter handlers.
    """
    entity = None
    
    # mapping field → handler
    filter_map = {}
    
    def __init__(self):
        """
        Initialize the BaseRepository.
        """
        if self.entity is None:
            raise NotImplementedError(
                "Repository must define entity"
            )
        
            
    def apply_filters(self, query, filters):
        """
        Apply filters to a query.

        Args:
            query: The query to apply filters to.
            filters: A list of filters to apply.

        Returns:
            The filtered query.
        """
        try:
            if filters is None or not filters:
                return query

            for f in filters:
                field = f.get("field")
                value = f.get("value")

                handler = self.filter_map.get(field)
                if handler:
                    query = handler(query, value)

            return query
        except Exception as e:
            logger.error(f"Error in apply_filters: {e}", exc_info=e)
            raise e

    @db_session
    def get_by_id(self, id):
        """
        Retrieve an entity by its ID.

        Args:
            id: The ID of the entity to retrieve.

        Returns:
            The entity with the specified ID.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            return self.entity.get(id=id)
        except Exception as e:
            logger.error(f"Error in get_by_id: {e}", exc_info=e)
            raise e

    @db_session
    def get_all_with_filters_and_pagination(self, filters=None, page=1, limit=10):
        """
        Retrieve all entities with filters and pagination.

        Args:
            filters: A list of filters to apply.
            page: The page number for pagination.
            limit: The number of entities per page.

        Returns:
            A tuple containing the filtered entities and pagination details.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            if filters is None:
                filters = []
            query = select(e for e in self.entity)
            query = self.apply_filters(query, filters)
            
            # Paginate
            page = max(page, 1)
            limit = max(limit, 1)

            total = query.count()
            total_pages = math.ceil(total / limit)

            offset = (page - 1) * limit
            items = query[offset: offset + limit]
            
            return items, {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages
            }
        except Exception as e:
            logger.error(f"Error in get_all_with_filters_and_pagination: {e}", exc_info=e)
            return [], {
                "page": page,
                "limit": limit,
                "total": 0,
                "total_pages": 0
            }
    
    @db_session
    def get_one_by_filters(self, filters=None):
        """
        Retrieve a single entity matching the filters.

        Args:
            filters: A list of filters to apply.

        Returns:
            The entity matching the filters.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            if filters is None:
                filters = []
            query = select(e for e in self.entity)
            query = self.apply_filters(query, filters).first()
            return query
        except Exception as e:
            logger.error(f"Error in get_one_by_filters: {e}", exc_info=e)
            raise e

    @db_session
    def create(self, data: dict):
        """
        Create a new entity.

        Args:
            data: The data for the new entity.

        Returns:
            The created entity.

        Raises:
            Exception: If an error occurs during creation.
        """
        try:
            return self.entity(**data)
        except Exception as e:
            logger.error(f"Error in create: {e}", exc_info=e)
            raise e

    @db_session
    def udpate(self, data: dict):
        """
        Update an existing entity.

        Args:
            data: The updated data for the entity.

        Returns:
            The updated entity, or None if the entity does not exist.

        Raises:
            Exception: If an error occurs during update.
        """
        try:
            obj = self.get_by_id(data.get("id"))
            if not obj:
                return None
            
            obj.set(**data)
            return obj
        except Exception as e:
            logger.error(f"Error in udpate: {e}", exc_info=e)
            raise e

    @db_session
    def delete(self, id, soft_delete=True):
        """
        Delete an entity by its ID.

        Args:
            id: The ID of the entity to delete.
            soft_delete: Whether to perform a soft delete (default: True).

        Returns:
            The result of the delete operation.

        Raises:
            Exception: If an error occurs during deletion.
        """
        try:
            obj = self.get_by_id(id)
            if obj:
                if not soft_delete:
                    obj.delete()
                else:
                    obj.is_deleted = True
            
            return obj
        except Exception as e:
            logger.error(f"Error in delete: {e}", exc_info=e)
            raise e
