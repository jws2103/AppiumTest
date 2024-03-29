import argparse
import datetime
import os
import random
import string
import time
import boto3
import requests

# The following script runs a test through Device Farm
#
# Things you have to change:
parser = argparse.ArgumentParser()
parser.add_argument("--appFilePath")
parser.add_argument("--projectArn")
parser.add_argument("--devicePoolArn")
parser.add_argument("--awsAccessKeyId")
parser.add_argument("--awsSecretKey")
parser.add_argument("--testBundlePath")
parser.add_argument("--testSpecPath")
args = parser.parse_args()
config = {
    # This is our app under test.
    "appFilePath":args.appFilePath,
    "projectArn": args.projectArn,
    # Since we care about the most popular devices, we'll use a curated pool.
    "poolArn":args.devicePoolArn,
    "namePrefix":"AutomatedTest",
    # This is our test package. This tutorial won't go into how to make these.
    "testPackage":args.testBundlePath,
    "testSpec": args.testSpecPath,
    "awsAccessKeyId" : args.awsAccessKeyId,
    "awsSecretKey" : args.awsSecretKey
}

print(config['appFilePath'], config['projectArn'], config['poolArn'], config['testPackage'], config['testSpec'])

client = boto3.client('devicefarm', region_name='us-west-2', aws_access_key_id=config['awsAccessKeyId'], aws_secret_access_key=config['awsSecretKey'])
unique = config['namePrefix']+"-"+(datetime.date.today().isoformat())+(''.join(random.sample(string.ascii_letters,8)))

print(f"The unique identifier for this run is going to be {unique} -- all uploads will be prefixed with this.")

def upload_df_file(filename, type_, mime='application/octet-stream'):
    response = client.create_upload(projectArn=config['projectArn'],
        name = (unique)+"_"+os.path.basename(filename),
        type=type_,
        contentType=mime
        )
    # Get the upload ARN, which we'll return later.
    upload_arn = response['upload']['arn']
    # We're going to extract the URL of the upload and use Requests to upload it
    upload_url = response['upload']['url']
    with open(filename, 'rb') as file_stream:
        print(f"Uploading {filename} to Device Farm as {response['upload']['name']}... ",end='')
        put_req = requests.put(upload_url, data=file_stream, headers={"content-type":mime})
        print(' done')
        if not put_req.ok:
            raise Exception("Couldn't upload, requests said we're not ok. Requests says: "+put_req.reason)
    started = datetime.datetime.now()
    while True:
        print(f"Upload of {filename} in state {response['upload']['status']} after "+str(datetime.datetime.now() - started))
        if response['upload']['status'] == 'FAILED':
            raise Exception("The upload failed processing. DeviceFarm says reason is: \n"+response['upload']['message'])
        if response['upload']['status'] == 'SUCCEEDED':
            break
        time.sleep(5)
        response = client.get_upload(arn=upload_arn)
    print("")
    return upload_arn

our_upload_arn = upload_df_file(config['appFilePath'], "ANDROID_APP")
our_test_spec_arn = upload_df_file(config['testSpec'], "APPIUM_JAVA_TESTNG_TEST_SPEC");
our_test_package_arn = upload_df_file(config['testPackage'], 'APPIUM_PYTHON_TEST_PACKAGE')
print(our_upload_arn, our_test_package_arn, our_test_spec_arn)
# Now that we have those out of the way, we can start the test run...
response = client.schedule_run(
    projectArn = config["projectArn"],
    appArn = our_upload_arn,
    devicePoolArn = config["poolArn"],
    name=unique,
    test = {
        "type":"APPIUM_PYTHON",
        "testSpecArn": our_test_spec_arn,
        "testPackageArn": our_test_package_arn
        }
    )
run_arn = response['run']['arn']
start_time = datetime.datetime.now()
print(f"Run {unique} is scheduled as arn {run_arn} ")

response = client.get_run(arn=run_arn)
state = response['run']['status']
print(f" Run {unique} in state {state}, total time " + str(datetime.datetime.now() - start_time))

"""try:

    while True:
        response = client.get_run(arn=run_arn)
        state = response['run']['status']
        if state == 'COMPLETED' or state == 'ERRORED':
            break
        else:
            print(f" Run {unique} in state {state}, total time "+str(datetime.datetime.now()-start_time))
            time.sleep(10)
except:
    # If something goes wrong in this process, we stop the run and exit.

    client.stop_run(arn=run_arn)
    exit(1)
print(f"Tests finished in state {state} after "+str(datetime.datetime.now() - start_time))
# now, we pull all the logs.
jobs_response = client.list_jobs(arn=run_arn)
# Save the output somewhere. We're using the unique value, but you could use something else
save_path = os.path.join(os.getcwd(), unique)
os.mkdir(save_path)
# Save the last run information
for job in jobs_response['jobs'] :
    # Make a directory for our information
    job_name = job['name']
    os.makedirs(os.path.join(save_path, job_name), exist_ok=True)
    # Get each suite within the job
    suites = client.list_suites(arn=job['arn'])['suites']
    for suite in suites:
        for test in client.list_tests(arn=suite['arn'])['tests']:
            # Get the artifacts
            for artifact_type in ['FILE','SCREENSHOT','LOG']:
                artifacts = client.list_artifacts(
                    type=artifact_type,
                    arn = test['arn']
                )['artifacts']
                for artifact in artifacts:
                    # We replace : because it has a special meaning in Windows & macos
                    path_to = os.path.join(save_path, job_name, suite['name'], test['name'].replace(':','_') )
                    os.makedirs(path_to, exist_ok=True)
                    filename = artifact['type']+"_"+artifact['name']+"."+artifact['extension']
                    artifact_save_path = os.path.join(path_to, filename)
                    print("Downloading "+artifact_save_path)
                    with open(artifact_save_path, 'wb') as fn, requests.get(artifact['url'],allow_redirects=True) as request:
                        fn.write(request.content)"""
                    #/for artifact in artifacts
                #/for artifact type in []
            #/ for test in ()[]
        #/ for suite in suites
    #/ for job in _[]
# done
#print("Finished")