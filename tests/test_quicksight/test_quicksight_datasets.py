import boto3
import sure  # noqa # pylint: disable=unused-import

from moto import mock_quicksight
from moto.core import ACCOUNT_ID

# See our Development Tips on writing tests for hints on how to write good tests:
# http://docs.getmoto.org/en/latest/docs/contributing/development_tips/tests.html


@mock_quicksight
def test_create_data_set():
    client = boto3.client("quicksight", region_name="eu-west-1")

    resp = client.create_data_set(
        AwsAccountId=ACCOUNT_ID,
        DataSetId="myset",
        Name="My Data Set",
        ImportMode="SPICE",
        PhysicalTableMap={
            "table1": {
                "RelationalTable": {
                    "DataSourceArn": "d:s:arn",
                    "Catalog": "cat",
                    "Name": "dog",
                    "InputColumns": [{"Name": "c1", "Type": "string"}],
                }
            }
        },
    )

    resp.should.have.key("Arn").equals(
        f"arn:aws:quicksight:eu-west-1:{ACCOUNT_ID}:data-set/myset"
    )
    resp.should.have.key("DataSetId").equals("myset")
    resp.should.have.key("IngestionArn").equals(
        f"arn:aws:quicksight:eu-west-1:{ACCOUNT_ID}:ingestion/tbd"
    )


@mock_quicksight
def test_create_ingestion():
    client = boto3.client("quicksight", region_name="eu-west-1")

    client.create_data_set(
        AwsAccountId=ACCOUNT_ID,
        DataSetId="myset",
        Name="My Data Set",
        ImportMode="SPICE",
        PhysicalTableMap={
            "table1": {
                "RelationalTable": {
                    "DataSourceArn": "d:s:arn",
                    "Catalog": "cat",
                    "Name": "dog",
                    "InputColumns": [{"Name": "c1", "Type": "string"}],
                }
            }
        },
    )

    resp = client.create_ingestion(
        AwsAccountId=ACCOUNT_ID,
        DataSetId="n_a",
        IngestionId="n_a2",
        IngestionType="FULL_REFRESH",
    )

    resp.should.have.key("Arn").equals(
        f"arn:aws:quicksight:eu-west-1:{ACCOUNT_ID}:data-set/n_a/ingestions/n_a2"
    )
    resp.should.have.key("IngestionId").equals("n_a2")
    resp.should.have.key("IngestionStatus").equals("INITIALIZED")