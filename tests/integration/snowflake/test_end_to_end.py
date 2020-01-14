from datetime import datetime
import pytest
import os
from sqlalchemy import create_engine
from snowshu.configs import PACKAGE_ROOT
from click.testing import CliRunner
from snowshu.core.main import cli

#Build the initial test replica from snowshu creds

CONN_STRING='postgresql://snowshu:snowshu@snowshu:9999/snowshu'

@pytest.fixture(scope="session")
def run_snowshu_create():
    runner=CliRunner()
    configuration_path=os.path.join(PACKAGE_ROOT,'snowshu','templates','replica.yml')
    return runner.invoke(cli,('run','--replica-file',configuration_path)).output.split('\n')


@pytest.fixture(scope="session")
def run_snowshu_launch():
    runner=CliRunner()
    runner.invoke(cli,'launch','integration-test')
    yield
    runner.invoke(cli,'down','integration-test')

def test_reports_full_catalog_start(run_snowshu_create):
    result_lines=run_snowshu_create
    assert 'Assessing full catalog...' in result_lines[2]

def test_finds_7_relations(run_snowshu_create):
    result_lines=run_snowshu_create
    assert 'Identified a total of 7 relations to sample based on the specified configurations.' in result_lines[4]


def test_replicates_order_items(run_snowshu_create):
    result_lines=run_snowshu_create
    assert 'Done replication of relation SNOWSHU_DEVELOPMENT.SOURCE_SYSTEM.ORDER_ITEMS' in result_lines[-3]   

@pytest.mark.skip 
def test_snowshu_explain(run_snowshu_create):
    runner= CliRunner()
    response=json.loads(runner.invoke(cli,('explain','integration-test','--json')))

    assert response['name'] == 'integration-test'
    assert response['image'] == 'postgres:12'
    assert response['target_adapter'] == 'postgres'
    assert response['source_adapter'] == 'snowflake'
    assert datetime(response['created_at']) < datetime.now()

@pytest.mark.skip
def test_launches(run_snowshu_create):
    runner=CliRunner()
    response=runner.invoke(cli,'launch','integration-test')
    assert 'ReplicaFactory integration-test launched and started.' in response.output
    assert 'You can connect to this replica with connection string: postgresql://snowshu:snowshu@snowshu:9999/snowshu' in response.output
    assert 'To stop your replica temporarily, use command `snowshu stop integration-test`' in response.output
    assert 'To spin down your replica, use command `snowshu down integration-test`' in response.output

    conn=create_engine(CONN_STRING)
    q=conn.execute('SELECT COUNT(*) FROM "SNOWSHU_DEVELOPMENT"."EXTERNAL_DATA"."ADDRESS_REGION_ATTRIBUTES"')
    count=q.fetchall()[0][0]
    assert count > 100

@pytest.mark.skip
def test_starts(run_snowshu_create):
    runner=CliRunner()
    response=runner.invoke(cli,'start','integration-test')
    assert 'ReplicaFactory integration-test restarted.' in response.output
    assert 'You can connect to this replica with connection string: postgresql://snowshu:snowshu@snowshu:9999/snowshu' in response.output
    assert 'To stop your replica temporarily, use command `snowshu stop integration-test`' in response.output
    assert 'To spin down your replica, use command `snowshu down integration-test`' in response.output
    ## cleanup
    runner.invoke(cli,'down','integration-test')
    

@pytest.mark.skip
def test_stops(run_snowshu_create):
    runner=CliRunner()
    response=runner.invoke(cli,'stop','integration-test')
    assert 'ReplicaFactory integration-test stopped.' in response.output
    assert 'You can connect to this replica with connection string: postgresql://snowshu:snowshu@snowshu:9999/snowshu' not in response.output
    assert 'To start your replica again use command `snowshu start integration-test`' in response.output

@pytest.mark.skip
def test_bidirectional(run_snowshu_create):
    conn=create_engine(CONN_STRING)
    query="""
SELECT 
    COUNT(*) 
FROM 
    "SNOWSHU_DEVELOPMENT"."SOURCE_SYSTEM"."ORDER_ITEMS" oi
FULL OUTER JOIN
     "SNOWSHU_DEVELOPMENT"."SOURCE_SYSTEM"."PRODUCTS" p
ON 
    oi.product_id = p.id
WHERE 
    oi.product_id IS NULL
OR
    p.id IS NULL
"""
    q=conn.execute(query)
    count=q.fetchall()[0][0]
    assert count == 0

@pytest.mark.skip
def test_directional(run_snowshu_create,run_snowshu_launch):
    conn=create_engine(CONN_STRING)
    query="""
WITH
joined_roots AS (
SELECT 
    oi.id AS oi_id
    ,oi.order_id AS oi_order_id
    ,o.id AS o_id
FROM 
    "SNOWSHU_DEVELOPMENT"."SOURCE_SYSTEM"."ORDER_ITEMS" oi
FULL OUTER JOIN
     "SNOWSHU_DEVELOPMENT"."SOURCE_SYSTEM"."ORDERS" o
ON 
    oi.order_id = o.id
)
SELECT 
    (SELECT COUNT(*) FROM joined_roots WHERE oi_id is null) AS upstream_missing
    ,(SELECT COUNT(*) FROM joined_roots WHERE o.id is null) AS downstream_missing
"""
    q=conn.execute(query)
    upstream_missing,downstream_missing=q.fetchall()[0]
    assert upstream_missing==0
    assert downstream_missing > 0 #it is statistically very unlikely that NONE of the upstreams without a downstream will be included.

@pytest.mark.skip
def test_view(run_snowshu_create,run_snowshu_launch):
    conn=create_engine(CONN_STRING)
    query="""
SELECT 
    (SELECT COUNT(*) FROM "SNOWSHU_DEVELOPMENT"."SOURCE_SYSTEM"."ORDER_ITEMS_VIEW") AS oiv
    ,(SELECT COUNT(*) FROM "SNOWSHU_DEVELOPMENT"."SOURCE_SYSTEM"."ORDER_ITEMS") AS oi
"""
    q=conn.execute(query)
    assert len(set(q.fetchall()[0])) == 1

