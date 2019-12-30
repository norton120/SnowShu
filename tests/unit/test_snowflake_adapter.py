from snowshu.adapters.source_adapters.snowflake_adapter import SnowflakeAdapter
from tests.common import rand_string,query_equalize
from snowshu.core.models.relation import Relation
from snowshu.core.models.credentials import Credentials
from snowshu.core.models.materializations import TABLE
from snowshu.adapters.source_adapters.sample_methods import BernoulliSample


def test_conn_string_basic():
    sf=SnowflakeAdapter()
    USER,PASSWORD,ACCOUNT,DATABASE=[rand_string(15) for _ in range(4)]
    
    creds=Credentials(user=USER,password=PASSWORD,account=ACCOUNT,database=DATABASE)

    sf.credentials=creds
    
    conn_string=sf.get_connection()
    
    assert str(conn_string.url)==f'snowflake://{USER}:{PASSWORD}@{ACCOUNT}/{DATABASE}/'


def test_sample_statement():
    sf=SnowflakeAdapter()
    DATABASE,SCHEMA,TABLE=[rand_string(10) for _ in range(3)]
    relation=Relation(database=DATABASE,
                      schema=SCHEMA,
                      name=TABLE,
                      materialization=TABLE,
                      attributes=[])
    sample=sf.sample_statement_from_relation(relation,BernoulliSample(10))
    assert query_equalize(sample)==query_equalize(f"""
SELECT
    *
FROM 
    "{DATABASE}"."{SCHEMA}"."{TABLE}"
    SAMPLE BERNOULLI (10)
""")

def test_directional_statement():
    sf=SnowflakeAdapter()
    DATABASE,SCHEMA,TABLE,LOCAL_KEY,REMOTE_KEY=[rand_string(10) for _ in range(5)]
    relation=Relation(database=DATABASE,
                      schema=SCHEMA,
                      name=TABLE,
                      materialization=TABLE,
                      attributes=[])
    relation.core_query=f"""
SELECT
    *
FROM 
    "{DATABASE}"."{SCHEMA}"."{TABLE}"
    SAMPLE BERNOULLI (10)
"""
    statement=sf.predicate_constraint_statement(relation,True,LOCAL_KEY,REMOTE_KEY)
    assert query_equalize(statement)==query_equalize(f"""
{LOCAL_KEY} IN 
    ( SELECT  
        {REMOTE_KEY}
    FROM (
SELECT
    *
FROM 
    "{DATABASE}"."{SCHEMA}"."{TABLE}"
    SAMPLE BERNOULLI (10)
))
""")

def test_analyze_wrap_statement():
    sf=SnowflakeAdapter()
    DATABASE,SCHEMA,NAME=[rand_string(10) for _ in range(3)]
    relation=Relation(database=DATABASE,schema=SCHEMA,name=NAME,materialization=TABLE,attributes=[])
    sql=f"SELECT * FROM some_crazy_query"
    statement=sf.analyze_wrap_statement(sql, relation)
    assert query_equalize(statement) == query_equalize(f"""
WITH
    __SNOWSHU_COUNT_POPULATION AS (
SELECT
    COUNT(*) AS population_size
FROM
    {relation.quoted_dot_notation}
)
,__SNOWSHU_CORE_SAMPLE AS (
{sql}
)
,__SNOWSHU_CORE_SAMPLE_COUNT AS (
SELECT
    COUNT(*) AS sample_size
FROM
    __SNOWSHU_CORE_SAMPLE
)
SELECT
    s.sample_size AS sample_size
    ,p.population_size AS population_size
FROM
    __SNOWSHU_CORE_SAMPLE_COUNT s
INNER JOIN
    __SNOWSHU_COUNT_POPULATION p
ON
    1=1
LIMIT 1
""")

def test_directionally_wrap_statement_directional():
    sf=SnowflakeAdapter()
    sampling=BernoulliSample(50)
    query="SELECT * FROM highly_conditional_query"
    assert query_equalize(sf.directionally_wrap_statement(query,sampling)) == query_equalize(f"""
WITH
    __SNOWSHU_FINAL_SAMPLE AS (
{query}
)
,___SNOWSHU_DIRECTIONAL_SAMPLE AS (
SELECT
    *
FROM
    __SNOWSHU_FINAL_SAMPLE
SAMPLE BERNOULLI (50)
)
SELECT 
    *
FROM 
    __SNOWSHU_DIRECTIONAL_SAMPLE
""")