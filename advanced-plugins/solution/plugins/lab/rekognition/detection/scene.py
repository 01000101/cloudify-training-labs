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
    Rekognition.Detection.Scene
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    AWS Rekognition scene detection operations
'''
# Cloudify
from cloudify.exceptions import NonRecoverableError
from rekognition.connection import RekognitionConnection
from rekognition.utils import get_image_from_node


def start(ctx, **_):
    '''Starts an AWS Rekognition scene detection action'''
    # Get a connection to the service
    client = RekognitionConnection(ctx.node).client()
    # Start the action
    ctx.logger.info('Sending image to Rekognition for processing')
    res = client.detect_labels(
        Image=get_image_from_node(ctx, ctx.node))
    # Extract the labels
    labels = res.get('Labels', list())
    if not labels:
        raise NonRecoverableError(
            'Rekognition did not respond with any image labels')
    # Save the labels as runtime properties
    ctx.instance.runtime_properties['labels'] = labels
    # Debug logging
    ctx.logger.debug('Rekognition finished processing the image')
    for label in labels:
        ctx.logger.debug('Label: "%s" | Confidence: %s'
                         % (label['Name'], label['Confidence']))
