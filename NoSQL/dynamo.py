import boto3
s3 = boto3.resource('s3',aws_access_key_id='aws_secret_access_key', aws_secret_access_key='aws_access_key_id' )

try:
    s3.create_bucket(Bucket='shalini-s3bucket', CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}) 
except Exception as e:
    print (e)

bucket = s3.Bucket("shalini-s3bucket")
bucket.Acl().put(ACL='public-read')

# Uploading data into bucket
body = open('/Users/shalini/Documents/experiments.csv', 'rb')

o = s3.Object('shalini-s3bucket', 'test').put(Body=body )
s3.Object('shalini-s3bucket', 'test').Acl().put(ACL='public-read')


dyndb = boto3.resource('dynamodb',region_name='us-west-2',aws_access_key_id='aws_secret_access_key', aws_secret_access_key='aws_access_key_id')

try:
	table = dyndb.create_table(
		TableName='DataTable',
		KeySchema=[
		{
		'AttributeName': 'PartitionKey',
		'KeyType': 'HASH'
		},
		{
		'AttributeName': 'RowKey',
		'KeyType': 'RANGE'
		}],
		AttributeDefinitions=[
		{
		'AttributeName': 'PartitionKey',
		'AttributeType': 'S'
		},
		{
		'AttributeName': 'RowKey',
		'AttributeType': 'S'
		},],
		ProvisionedThroughput={
		'ReadCapacityUnits': 5,
		'WriteCapacityUnits': 5
	}
	)
except Exception as e:
    print (e)
    #if there is an exception, the table may already exist.
    table = dyndb.Table("DataTable")

table.meta.client.get_waiter('table_exists').wait(TableName='DataTable')
print(table.item_count)

import csv
with open('/Users/shalini/Documents/experiments.csv', 'r') as csvfile: 
	csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
	next(csvf)
	for item in csvf:
		print(item)
		body = open('/Users/shalini/Documents/datafiles/'+item[4], 'rb') 
		s3.Object('shalini-s3bucket', item[4]).put(Body=body)
		md = s3.Object('shalini-s3bucket', item[4]).Acl().put(ACL='public-read')
		url = " https://s3-us-west-2.amazonaws.com/shalini-s3bucket/"+item[3] 
		metadata_item = {'PartitionKey': item[0], 'RowKey': item[1],'description' : item[4], 'date' : item[2], 'url':url}
		try: 
			table.put_item(Item=metadata_item)
		except:
			print("item may already be there or another failure")


response = table.get_item(Key={'PartitionKey': '1','RowKey': '4'})
#item = response['Item'] 
print(response)


