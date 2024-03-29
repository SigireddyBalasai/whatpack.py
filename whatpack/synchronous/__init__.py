# noinspection SpellCheckingInspection
"""This is asynchronous module for whatpack
Apache License 2.0
Copyright [2023] [Sigireddy Balasai]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Use
from whatpack.synchronous import whats
help(whats)
for getting help
"""

__all__ = ['core', 'whats']
from .whats import send_img_or_video_immediately
from .core.core_ import *