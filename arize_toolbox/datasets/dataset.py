from typing import Optional
from arize.utils.types import Schema
from pandas import DataFrame, read_csv
from dataclasses import dataclass

@dataclass
class Dataset():
    def __init__(self,dataframe:DataFrame, schema:Schema):
        print(type(dataframe))
        parsed_dataframe = parse_dataframe(dataframe, schema)

        self.dataframe = parsed_dataframe
        self.schema = schema


    # TODO(assign): Find a good representation of the Dataset Object
    # Ideas in HF & Evidently
    # def __repr__(self):

    def head(self, num_rows:Optional[int]=5):
        # TODO(assign): Look at Pandas and create our own head method
        return self.dataframe.head(num_rows)

    def get_column(self, col_name:str):
        return self.dataframe[col_name]

def from_dataframe(dataframe:DataFrame, schema:Schema)->Dataset:
    return Dataset(dataframe, schema)

def from_csv(filepath:str, schema:Schema)->Dataset:
    df = read_csv(filepath)
    return Dataset(df, schema)

def parse_dataframe(dataframe:DataFrame, schema:Schema):
    # feature_column_names
    # embedding_feature_column_names
    # timestamp_column_name
    # prediction_label_column_name
    # prediction_score_column_name
    # actual_label_column_name
    # actual_score_column_name
    schema_cols = [schema.timestamp_column_name,
                  schema.prediction_label_column_name,
                  schema.prediction_score_column_name,
                  schema.actual_label_column_name,
                  schema.actual_score_column_name
                ]
    schema_cols += schema.feature_column_names

    for emb_feat_cols in schema.embedding_feature_column_names:
        schema_cols.append(emb_feat_cols.vector_column_name)
        if emb_feat_cols.data_column_name:
            schema_cols.append(emb_feat_cols.data_column_name)
        if emb_feat_cols.link_to_data_column_name:
            schema_cols.append(emb_feat_cols.link_to_data_column_name)

    drop_cols=[col for col in dataframe.columns if col not in schema_cols]
    return dataframe.drop(columns=drop_cols)