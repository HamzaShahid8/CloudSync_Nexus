from django.shortcuts import render
import asyncio
from .models import *
import logging
from django.http import JsonResponse
from asgiref.sync import sync_to_async

logger = logging.getLogger('api')

# Create your views here.

@sync_to_async
def get_users():
    return list(User.objects.values())

@sync_to_async
def get_posts():
    return list(Post.objects.select_related('user').values())


async def dashboard(request):
    logger.info('Dashboard')
    
    try:
        
        users, posts = await asyncio.gather(get_users(), get_posts())
        
        logger.info('DB queries completed')
        
        return JsonResponse({
            'status': 'success',
            'users': users,
            'posts': posts
        })
        
    except Exception as e:
        logger.error(f"Error in dashboard view: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })