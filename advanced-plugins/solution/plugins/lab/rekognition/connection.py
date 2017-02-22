# #######
# Copyright (c) 2017 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.
'''
    Rekognition.Connection
    ~~~~~~~~~~~~~~~~~~~~~~
    AWS Rekognition connection
'''
# Boto
import boto3
# Cloudify
from rekognition.constants import AWS_CONFIG_PROPERTY

# pylint: disable=R0903


class RekognitionConnection(object):
    '''
        Provides a sugared connection to the AWS Rekognition service

    :param `cloudify.context.NodeContext` node: A Cloudify node
    :param dict aws_config: AWS connection configuration overrides
    '''
    def __init__(self, node, aws_config=None):
        aws_config_whitelist = [
            'aws_access_key_id', 'aws_secret_access_key', 'region_name']
        self.aws_config = node.properties.get(AWS_CONFIG_PROPERTY, dict())
        # Merge user-provided AWS config with generated config
        self.aws_config.update(aws_config or dict())
        # Prepare region name for Boto
        self.aws_config['region_name'] = self.aws_config.get(
            'rekognition_region_name', self.aws_config.get('ec2_region_name'))
        # Delete all non-whitelisted keys
        self.aws_config = {k: v for k, v in self.aws_config.iteritems()
                           if k in aws_config_whitelist}

    def client(self):
        '''
            Builds an AWS Rekognition connection client

        :returns: An AWS Rekognition boto3 client
        :rtype: `boto.emr.connection.EmrConnection`
        :raises: :exc:`cloudify.exceptions.NonRecoverableError`
        '''
        return boto3.client('rekognition', **self.aws_config)
