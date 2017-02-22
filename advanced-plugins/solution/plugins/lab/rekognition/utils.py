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
    Rekognition.Utils
    ~~~~~~~~~~~~~~~~~
    AWS Rekognition helper utilities
'''
from cloudify.exceptions import NonRecoverableError


def get_image_from_node(ctx, node):
    '''Extracts and validates an image to be processed'''
    props = node.properties
    if 'image' not in props:
        raise NonRecoverableError('Missing image to process')
    image = props['image']
    # Check if it's a local file
    if isinstance(image, basestring):
        ctx.logger.info('Using local image file: %s' % image)
        with open(image, mode='rb') as _file:
            return dict(Bytes=_file.read())
    # Check if it's an S3 file
    if isinstance(image, dict) and \
       'bucket' in image and 'name' in image:
        ctx.logger.info('Using S3 image file: %s' % image)
        return dict(S3Object=dict(
            Bucket=image['bucket'],
            Name=image['name'],
            Version=image.get('version')))
    raise NonRecoverableError(
        'Could not determine type of image to process. Must be either '
        'string (path to local file) or dict (S3 object)')
