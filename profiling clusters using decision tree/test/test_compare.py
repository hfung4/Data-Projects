"""Tests the logic for DAG comparison

This code is invoked with pytest:
  cd <pybnutil_sys_test>
  pytest
"""
import os
import pytest
import re
from src import helper


# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(ROOT_DIR,"test_data")

''' pytest fixtures
pytest fixtures are functions attached to the tests which run  before the test function is executed. 
Fixtures are a set of resources that have to be set up before other pytest "test_XXX()" functions can be run.
pytest fixture function is automatically called by the pytest framework when the name of the 
argument and the fixture is the same.
'''
@pytest.fixture
def fixture_func():
    return "fixture test"

# pytest function that uses outputs of fixture_func as argument
def test_fixture(fixture_func):
    assert fixture_func=="fixture test"


# DAG comparison tests ---------------------------------------------------

@pytest.fixture
# return a list of modelstring paths of two identical DAGs
def dag_same_paths():
   return [os.path.join(TEST_DATA_DIR,'reference'),
           os.path.join(TEST_DATA_DIR, 'test_same')]

@pytest.fixture
# return a list of modelstring paths of two identical DAGs
def dag_diff_paths():
   return [os.path.join(TEST_DATA_DIR,'reference'),
           os.path.join(TEST_DATA_DIR, 'test_diff')]


def test_compare_same(dag_same_paths):
    assert helper.BNcompare("", dag_same_paths) == "TRUE"

def test_compare_diff(dag_diff_paths):
    assert helper.BNcompare("", dag_diff_paths) != "TRUE"

