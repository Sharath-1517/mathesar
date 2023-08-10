import pytest
from sqlalchemy import select, func
from sqlalchemy.exc import NoSuchTableError

from db.tables.operations.alter import comment_on_table, rename_table
from db.tables.operations.create import create_mathesar_table
from db.tables.operations.select import get_oid_from_table, reflect_table, reflect_table_from_oid
from db.tests.tables import utils as test_utils
from db.metadata import get_empty_metadata
from db.schemas.utils import get_schema_oid_from_name


def test_rename_table(engine_with_schema):
    engine, schema = engine_with_schema
    table_name = "test_rename_table"
    new_table_name = "test_rename_table_new"
    schema_oid = get_schema_oid_from_name(schema, engine)
    old_table_oid = create_mathesar_table(engine, table_name, schema_oid)

    rename_table(table_name, schema, engine, new_table_name)
    new_table = reflect_table(new_table_name, schema, engine, metadata=get_empty_metadata())
    new_oid = get_oid_from_table(new_table.name, new_table.schema, engine)

    assert old_table_oid == new_oid
    assert new_table.name == new_table_name

    with pytest.raises(NoSuchTableError):
        reflect_table(table_name, schema, engine, metadata=get_empty_metadata())


def test_comment_on_table(engine_with_roster, roster_table_name):
    engine, schema = engine_with_roster
    table_oid = get_oid_from_table(roster_table_name, schema, engine)
    expect_comment = 'my super test comment'
    comment_on_table(roster_table_name, schema, engine, expect_comment)
    with engine.begin() as conn:
        res = conn.execute(select(func.obj_description(table_oid, 'pg_class')))
    actual_comment = res.fetchone()[0]

    assert actual_comment == expect_comment

    expect_new_comment = 'my new test comment'
    comment_on_table(roster_table_name, schema, engine, expect_new_comment)
    with engine.begin() as conn:
        res = conn.execute(select(func.obj_description(table_oid, 'pg_class')))
    actual_new_comment = res.fetchone()[0]

    assert actual_new_comment == expect_new_comment
