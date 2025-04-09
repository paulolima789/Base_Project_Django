from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from django.contrib.auth.models import AnonymousUser
from django.apps import apps
from django.core.paginator import Paginator


