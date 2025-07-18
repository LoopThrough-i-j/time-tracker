from datetime import datetime, timezone
from typing import Any, Generic, Type, TypeVar

from pymongo import ReturnDocument
from pymongo.collection import Collection

from database.mongodb import mongo_db
from database.mongodb.models.base import BaseMongoModel

ModelType = TypeVar("ModelType", bound=BaseMongoModel)


class BaseActions(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model: Type[ModelType] = model
        self.collection: Collection[dict[str, Any]] = mongo_db[model.collection]

    def insert_record(self, record: ModelType) -> ModelType:
        record.updated_at = datetime.now(timezone.utc)
        record_detail = record.model_dump_db()
        self.collection.insert_one(record_detail)
        return record

    def insert_many_records(self, records: list[ModelType]) -> list[ModelType]:
        if not records:
            return records

        current_time = datetime.now(timezone.utc)
        for record in records:
            record.updated_at = current_time
        record_details = [record.model_dump_db() for record in records]
        self.collection.insert_many(record_details)
        return records

    def get_by_id(
        self, document_id: str, is_active: bool | None = True, is_deleted: bool | None = False
    ) -> ModelType | None:
        query = {"_id": document_id}

        if is_active is not None:
            query["is_active"] = is_active
        if is_deleted is not None:
            query["is_deleted"] = is_deleted

        document = self.collection.find_one(query)

        if document:
            return self.model.model_validate(document)
        return None

    def update_document(self, data: ModelType) -> ModelType:
        data.updated_at = datetime.now(timezone.utc)

        document = self.collection.find_one_and_update(
            {"_id": data.id}, {"$set": data.model_dump_db()}, return_document=ReturnDocument.AFTER
        )

        return self.model.model_validate(document)

    def update_fields(
        self, doc_id: str, data: dict[str, Any], custom: dict[str, Any] = {}, ignore_none: bool = True
    ) -> ModelType:
        data = {k: v for k, v in data.items() if v is not None or not ignore_none}
        data["updated_at"] = datetime.now(timezone.utc)

        document = self.collection.find_one_and_update(
            {"_id": doc_id}, {"$set": data, **custom}, return_document=ReturnDocument.AFTER
        )
        return self.model.model_validate(document)

    def add_to_set(self, doc_id: str, field: str, value: list) -> ModelType:
        update_operation = {
            "$addToSet": {field: {"$each": value}},
            "$set": {"updated_at": datetime.now(timezone.utc)},
        }

        document = self.collection.find_one_and_update(
            {"_id": doc_id},
            update_operation,
            return_document=ReturnDocument.AFTER,
        )
        return self.model.model_validate(document)

    def find_records(
        self,
        query: dict[str, Any] | None = None,
        sort: list[tuple[str, int]] | None = None,
        offset: int | None = None,
        limit: int | None = None,
        is_active: bool | None = True,
        is_deleted: bool | None = False,
    ) -> list[ModelType]:
        if query is None:
            query = {}

        if is_active is not None:
            query["is_active"] = is_active
        if is_deleted is not None:
            query["is_deleted"] = is_deleted

        cursor = self.collection.find(filter=query)

        if sort:
            cursor = cursor.sort(sort)
        if offset:
            cursor = cursor.skip(offset)
        if limit:
            cursor = cursor.limit(limit)

        return [self.model.model_validate(doc) for doc in cursor]

    def delete_record(self, document_id: str, soft_delete: bool = True) -> bool:
        if soft_delete:
            result = self.collection.update_one(
                {"_id": document_id}, {"$set": {"is_deleted": True, "updated_at": datetime.now(timezone.utc)}}
            )
        else:
            result = self.collection.delete_one({"_id": document_id})

        return result.modified_count > 0 or result.deleted_count > 0

    def count_records(
        self,
        query: dict[str, Any] | None = None,
        is_active: bool | None = True,
        is_deleted: bool | None = False,
    ) -> int:
        if query is None:
            query = {}

        if is_active is not None:
            query["is_active"] = is_active
        if is_deleted is not None:
            query["is_deleted"] = is_deleted

        return self.collection.count_documents(query)

    def bulk_add_to_set(self, doc_ids: list[str], field: str, value: list) -> int:
        result = self.collection.update_many(
            {"_id": {"$in": doc_ids}},
            {
                "$addToSet": {field: {"$each": value}},
                "$set": {"updated_at": datetime.now(timezone.utc)},
            },
        )
        return result.modified_count

    def bulk_pull(self, doc_ids: list[str], field: str, value: list) -> int:
        result = self.collection.update_many(
            {"_id": {"$in": doc_ids}},
            {
                "$pull": {field: {"$in": value}},
                "$set": {"updated_at": datetime.now(timezone.utc)},
            },
        )
        return result.modified_count
