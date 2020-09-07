import boto3
session = boto3.Session(profile_name='foxsports-gitops-prod')
ecr = session.client('ecr')
repos = ecr.describe_repositories()
for repo in repos['repositories']:
    images = ecr.list_images(repositoryName=repo['repositoryName'])
    #print(images['imageIds']['imageTag'])
    for image in images['imageIds']:
        if 'imageTag' not in image:
            continue
        try:
           findings = ecr.describe_image_scan_findings(repositoryName=repo['repositoryName'],imageId=image)
           for finding in findings['imageScanFindings']['findings']:
               severity = finding['severity']
               if (severity == 'CRITICAL' or severity == 'HIGH'):
                   print (image, repo['repositoryName'])
        except:
           continue
