import math
from pony.orm import db_session, select, desc
from app.utils.logger import logger

class BaseRepository:
    """
    BaseRepository provides a generic repository layer for interacting with the database.

    Attributes:
        entity: The database entity (model) associated with this repository.
        filter_map: A mapping of fields to their respective filter handlers.
    """
    entity = None
    
    # mapping field to filter → handler
    filter_map = {
        "id": lambda x, v: x.filter(lambda t: str(t.id) == v),
        "is_deleted": lambda x, v: x.filter(lambda t: t.is_deleted == v),
    }
    
    def __init__(self):
        """
        Initialize the BaseRepository.
        """
        if self.entity is None:
            raise NotImplementedError(
                "Repository must define entity"
            )
        
            
    def apply_query_options(self, query, filters, order_by=None):
        """
        Apply filters to a query.

        Args:
            query: The query to apply filters to.
            filters: A list of filters to apply.

        Returns:
            The filtered query.
        """
        try:
            filters = filters or []
            
            # Default soft delete
            if not any(f.get("field") == "is_deleted" for f in filters):
                handler = self.filter_map.get("is_deleted")
                if handler:
                    query = handler(query, False)

            # Apply filters
            for f in filters:
                field = f.get("field")
                value = f.get("value")

                handler = self.filter_map.get(field)
                if handler:
                    query = handler(query, value)
            
            # Apply ordering
            if order_by:
                descending = order_by.startswith("-")
                field_name = order_by.lstrip("-")

                field = getattr(self.entity, field_name)
                if field:
                    query = query.order_by(desc(field) if descending else field)
            
            return query
        except Exception as e:
            logger.error(f"Error in apply_query_options: {e}", exc_info=e)
            raise

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
            return self.entity.get(id=id, is_deleted=False)
        except Exception as e:
            logger.error(f"Error in get_by_id: {e}", exc_info=e)
            raise

    @db_session
    def get_all_with_filters_and_pagination(self, filters=None, page=1, limit=10, order_by="-created_at"):
        """
        Retrieve all entities with filters and pagination.

        Args:
            filters: A list of filters to apply.
            page: The page number for pagination.
            limit: The number of entities per page.
            order_by: Field name to sort by, prefixed with "-" for descending order. 

        Returns:
            A tuple containing the filtered entities and pagination details.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            if filters is None:
                filters = []
            query = select(e for e in self.entity)
            query = self.apply_query_options(query, filters, order_by)
            
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
            query = self.apply_query_options(query, filters)
            return (query[:1] or [None])[0]
        except Exception as e:
            logger.error(f"Error in get_one_by_filters: {e}", exc_info=e)
            raise

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
            entity_obj = self.entity(**data)
            return entity_obj.to_dict(with_collections=True) 
        except Exception as e:
            logger.error(f"Error in create: {e}", exc_info=e)
            raise

    @db_session
    def update(self, data: dict):
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
            entity_obj = self.get_by_id(data.get("id"))
            if not entity_obj:
                return None
            
            entity_obj.set(**data)
            return entity_obj.to_dict(with_collections=True)
        except Exception as e:
            logger.error(f"Error in update: {e}", exc_info=e)
            raise
    
    @db_session
    def update_one_with_filters(self, filters=None, data: dict = {}):
        """
        Update an existing entity with fitlers.

        Args:
            data: The updated data for the entity with fitlers.

        Returns:
            The updated entity, or None if the entity does not exist.

        Raises:
            Exception: If an error occurs during update.
        """
        try:
            entity_obj = self.get_one_by_filters(filters)
            if not entity_obj:
                return None
            
            entity_obj.set(**data)
            return entity_obj.to_dict(with_collections=True)
        except Exception as e:
            logger.error(f"Error in update_one_with_filters: {e}", exc_info=e)
            raise

    @db_session
    def delete_by_id(self, id, soft_delete=True):
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
            
            return True
        except Exception as e:
            logger.error(f"Error in delete_by_id: {e}", exc_info=e)
            raise
