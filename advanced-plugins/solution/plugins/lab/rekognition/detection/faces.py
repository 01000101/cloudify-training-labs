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
    Rekognition.Detection.Faces
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    AWS Rekognition faces detection operations
'''
# Cloudify
from cloudify.exceptions import NonRecoverableError
from rekognition.connection import RekognitionConnection
from rekognition.utils import get_image_from_node


def start(ctx, **_):
    '''Starts an AWS Rekognition faces detection action'''
    # Get a connection to the service
    client = RekognitionConnection(ctx.node).client()
    # Start the action
    ctx.logger.info('Sending image to Rekognition for processing')
    res = client.detect_faces(
        Attributes=['ALL'],
        Image=get_image_from_node(ctx, ctx.node))
    # Extract the labels
    faces = res.get('FaceDetails', list())
    if not faces:
        raise NonRecoverableError(
            'Rekognition did not respond with any face details')
    # Save the labels as runtime properties
    ctx.instance.runtime_properties['faces'] = faces
    # Debug logging
    ctx.logger.debug('Rekognition finished processing the image')
    for face in faces:
        gender = face['Gender'] if 'Gender' in face else dict()
        age = face['AgeRange'] if 'AgeRange' in face else dict()
        glasses = face['Eyeglasses'] if 'Eyeglasses' in face else dict()
        emotions = face['Emotions'] if 'Emotions' in face else list()
        ctx.logger.debug(
            '\nFace (confidence: %s%%):\n'
            '  Gender: %s (%s%%)\n'
            '  Age: %s - %s\n'
            '  Glasses: %s (%s%%)\n'
            '  Emotions: %s' % (
                face['Confidence'],
                gender.get('Value'), gender.get('Confidence'),
                age.get('Low'), age.get('High'),
                glasses.get('Value'), glasses.get('Confidence'),
                ['%s (%s%%)' % (x['Type'], x['Confidence']) for x in emotions]
            ))
