from pathlib import Path
from typing import Collection, Mapping, Union

from pyspark.sql import Column, DataFrame, SparkSession
import pyspark.sql.functions as psf
from pyspark.sql.types import (
    BooleanType,
    ByteType,
    DateType,
    IntegerType,
    ShortType,
    StringType,
)


spark = SparkSession.builder.getOrCreate()
frame = spark.read.json(
    'data_part_1.json'
)
#     # For a CSV, `inferSchema=False` means every column stays of the string
#     # type. There is no time wasted on inferring the schema, which is
#     # arguably not something you would depend on in production either.
#     inferSchema=False,
#     header=True,
#     # The dataset mixes two values for null: sometimes there's an empty attribute,
#     # which you will see in the CSV file as two neighboring commas. But there are
#     # also literal "null" strings, like in this sample: `420.0,null,,1.0,`
#     # The following option makes a literal null-string equivalent to the empty value.
#     nullValue="null",
# )
