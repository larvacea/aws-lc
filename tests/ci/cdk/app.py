#!/usr/bin/env python3

# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from aws_cdk import core

from cdk.aws_lc_github_ci_stack import AwsLcGitHubCIStack
from cdk.linux_docker_image_batch_build_stack import LinuxDockerImageBatchBuildStack
from cdk.windows_docker_image_build_stack import WindowsDockerImageBuildStack
from cdk.ecr_stack import EcrStack
from util.metadata import AWS_ACCOUNT, AWS_REGION, LINUX_X86_ECR_REPO, LINUX_AARCH_ECR_REPO, WINDOWS_X86_ECR_REPO

# Initialize app.
app = core.App()

# Initialize env.
env = core.Environment(account=AWS_ACCOUNT, region=AWS_REGION)

# Define AWS ECR stacks.
# ECR holds the docker images, which are pre-built to accelerate the code builds/tests of git pull requests.
EcrStack(app, "aws-lc-ecr-linux-x86", LINUX_X86_ECR_REPO, env=env)
EcrStack(app, "aws-lc-ecr-linux-aarch", LINUX_AARCH_ECR_REPO, env=env)
EcrStack(app, "aws-lc-ecr-windows-x86", WINDOWS_X86_ECR_REPO, env=env)

# Define CodeBuild Batch job for testing code.
LinuxDockerImageBatchBuildStack(app, "aws-lc-docker-image-build-linux", env=env)

# DIND is not supported on Windows and, therefore, AWS CodeBuild is not used to build Windows Server container images.
# Windows Docker images are created by running commands in Windows EC2 instance.
WindowsDockerImageBuildStack(app, "aws-lc-docker-image-build-windows", env=env)

# Define CodeBuild Batch job for testing code.
AwsLcGitHubCIStack(app, "aws-lc-ci-linux-x86", "./cdk/codebuild/github_ci_linux_x86_omnibus.yaml", env=env)
AwsLcGitHubCIStack(app, "aws-lc-ci-linux-arm", "./cdk/codebuild/github_ci_linux_arm_omnibus.yaml", env=env)
AwsLcGitHubCIStack(app, "aws-lc-ci-windows-x86", "./cdk/codebuild/github_ci_windows_x86_omnibus.yaml", env=env)

app.synth()