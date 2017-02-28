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
    API_Gateway.Resources.REST_API
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    AWS API Gateway REST API resource interface
'''
# Cloudify
from cloudify.exceptions import RecoverableError, NonRecoverableError
from api_gateway.constants import (
    EXTERNAL_RESOURCE_ID, ALLOWED_KEYS_REST_API)
from api_gateway import utils
from api_gateway.connection import APIGatewayConnection
# Boto
from botocore.exceptions import ClientError


def create(ctx, **_):
    '''Creates an AWS API Gateway REST API'''
    # Get a connection to the service
    client = APIGatewayConnection(ctx.node).client()
    # Create the resource if needed
    create_if_needed(ctx, client)
    # Get the resource ID (must exist at this point)
    resource_id = utils.get_resource_id(raise_on_missing=True)
    # Get the resource
    ctx.logger.debug('Getting REST API "%s" properties' % resource_id)
    try:
        resource = client.get_rest_api(restApiId=resource_id)
        ctx.logger.debug('REST API "%s": %s' % (resource_id, resource))
    except ClientError:
        raise NonRecoverableError('Error creating REST API')


def delete(ctx, **_):
    '''Deletes an AWS API Gateway REST API'''
    # Get a connection to the service
    client = APIGatewayConnection(ctx.node).client()
    # Get the resource ID (must exist at this point)
    resource_id = utils.get_resource_id()
    if not resource_id:
        ctx.logger.warn('Missing resource ID. Skipping workflow...')
        return
    # Get the resource
    resource = client.get_rest_api(restApiId=resource_id)
    # Delete the resource (if needed)
    if ctx.node.properties['use_external_resource']:
        return
    if ctx.operation.retry_number == 0:
        ctx.logger.info('Deleting REST API "%s"' % resource_id)
        try:
            client.delete_rest_api(restApiId=resource.id)
            ctx.logger.debug('REST API "%s" deleted' % resource_id)
        except ClientError:
            raise RecoverableError('Error deleting REST API')


def create_if_needed(ctx, client):
    '''
        Creates a new resource if the context
        is that of a non-external type. This automatically
        updates the current contexts' resource ID.
    '''
    props = ctx.node.properties
    if props['use_external_resource'] or ctx.operation.retry_number > 0:
        ctx.logger.debug('External resource declared')
        return
    # Actually create the resource
    ctx.logger.info('Creating REST API')
    resource = client.create_rest_api(
        **utils.filter_boto_params(props, ALLOWED_KEYS_REST_API))
    if 'id' not in resource:
        NonRecoverableError(
            'Creating resource yielded an unexpected response: %s' % resource)
    ctx.logger.info('Successfully created REST API "%s"' % resource['id'])
    ctx.instance.runtime_properties[EXTERNAL_RESOURCE_ID] = resource['id']
