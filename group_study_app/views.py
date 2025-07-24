from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import Http404, HttpResponse
from django.contrib import messages
from .models import *
from .forms import *


# def chat_view(request, chatroom_name = 'public_group'):
    
#     chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
#     chat_messages = chat_group.chat_messages.all()[:30]
#     form = ChatmessageCreateForm()

#     other_user = None
#     if chat_group.is_private:
#         if request.user not in chat_group.members.all():
#             raise Http404()
#         for member in chat_group.members.all():
#             if member != request.user:
#                 other_user = member
#                 break 
    
#     if chat_group.groupchat_name:
#         if request.user not in chat_group.members.all():
#             if request.user.emailaddress_set.filter(verified=True).exists():
#                 chat_group.members.add(request.user)
#             else:
#                 messages.warning(request, 'You need to verify your email to join the chat!')
#                 return redirect('profile-settings')        
    
#     if request.htmx:
#         # Get message body and type from request
#         text_body = request.POST.get("text_body", "").strip()
#         latex_body = request.POST.get("latex_body", "").strip()

#         body = latex_body if latex_body else text_body

#         message_type = request.POST.get("message_type", "text")
#         if body:
#             # Create message with type
#             message = GroupMessage.objects.create(
#                 body=body,
#                 author=request.user,
#                 group=chat_group,
#                 message_type=message_type  # Add message type
#             )
            
#             context = {
#                 'message': message,
#                 'user': request.user
#             }
#             return render(request, 'group_study_app/partials/chat_message_p.html', context)
        
#         # Handle regular form-based messages (fallback)
#         form = ChatmessageCreateForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.author = request.user
#             message.group = chat_group
#             message.save()
            
#             context = {
#                 'message': message,
#                 'user': request.user
#             }
#             return render(request, 'group_study_app/partials/chat_message_p.html', context)

#     context = {
#         'chat_messages': chat_messages, 
#         'form': form, 
#         'chatroom_name': chatroom_name,
#         'other_user': other_user,
#         'chat_group': chat_group,
#     }
#     return render(request, 'group_study_app/chat.html', context)

def chat_view(request, chatroom_name = 'public_group'):
    
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break 
    
    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            if request.user.emailaddress_set.filter(verified=True).exists():
                chat_group.members.add(request.user)
            else:
                messages.warning(request, 'You need to verify your email to join the chat!')
                return redirect('profile-settings')        
    
    if request.htmx:
        # Get message body and type from request
        text_body = request.POST.get("text_body", "").strip()
        latex_body = request.POST.get("latex_body", "").strip()

        body = latex_body if latex_body else text_body

        message_type = request.POST.get("message_type", "text")
        if body:
            # Create message with type
            message = GroupMessage.objects.create(
                body=body,
                author=request.user,
                group=chat_group,
                message_type=message_type
            )
            
            # DON'T return HTML partial - let WebSocket handle it
            # Just return empty response or success status
            from django.http import HttpResponse
            return HttpResponse(status=200)
        
        # Handle regular form-based messages (fallback)
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            
            # DON'T return HTML partial - let WebSocket handle it
            return HttpResponse(status=200)

    context = {
        'chat_messages': chat_messages, 
        'form': form, 
        'chatroom_name': chatroom_name,
        'other_user': other_user,
        'chat_group': chat_group,
    }
    return render(request, 'group_study_app/chat.html', context)

def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    
    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    
    for chatroom in my_chatrooms:
        if other_user in chatroom.members.all():
            return redirect('chatroom', chatroom.group_name)

    
    chatroom = ChatGroup.objects.create(is_private=True)
    chatroom.members.add(other_user, request.user)
    return redirect('chatroom', chatroom.group_name)

@login_required
def create_groupchat(request):
    form = NewGroupForm()
    
    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)
    
    context = {
        'form': form
    }
    return render(request, 'group_study_app/create_groupchat.html', context)


@login_required
def chatroom_edit_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name = chatroom_name)
    if request.user != chat_group.admin:
        raise Http404
    
    form = ChatRoomEditForm(instance=chat_group) 
    
    if request.method == 'POST':
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()     
        remove_members = request.POST.get_list('remove_members')
        for member_id in remove_members:
            member = User.get(id=member_id)
            chat_group.members.remove(member)
        return redirect('chatroom', chatroom_name)     
    
    context = {
        'form' : form,
        'chat_group' : chat_group
    }   
    return render(request, 'group_study_app/chatroom_edit.html', context)

def chatroom_delete_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name = chatroom_name)
    if request.user != chat_group.admin:
        raise Http404

    if request.method == 'POST':
        chat_group.delete()
        messages.success(request, 'Chatroom Deleted')
        return redirect('home')

    return render(request, 'group_study_app/chatroom_delete.html', {'chat_group': chat_group})    

from django.shortcuts import redirect

def chatroom_leave_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)

    if request.user not in chat_group.members.all():
        raise Http404

    if request.method == 'POST':
        chat_group.members.remove(request.user)
        messages.success(request, 'You left the group')
        return redirect('home')  

   
    return render(request, 'group_study_app/chatroom_leave.html', {'chat_group': chat_group})

def chat_file_upload(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    
    if request.htmx and request.FILES:
        file = request.FILES['file']
        message = GroupMessage.objects.create(
            file = file,
            author = request.user, 
            group = chat_group,
        )
        channel_layer = get_channel_layer()
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(channel_layer.group_send)(
            chatroom_name, event
        )
        return HttpResponse()
    

    
