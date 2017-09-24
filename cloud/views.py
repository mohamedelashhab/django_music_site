from django.shortcuts import render,redirect,get_object_or_404,reverse
from .forms import UserForm,AlbumForm,SongForm
from django.contrib.auth import authenticate,login,logout
from .models import Album,Song
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

def index(request):
    context = {}
    return render(request,'cloud/index.html',context)

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username = username , password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                context = {'albums':albums}
                return render(request,'cloud/index.html',context)
    context = {
        'form':form
    }
    return render(request,'cloud/register.html',context)


def user_login(request):
    if request.user.is_authenticated():
        return redirect('cloud:profile')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username , password = password)
        if user is not None:
            if user.is_active:
                login(request,user)
                albums = Album.objects.filter(user=request.user)
                context = {'albums':albums}
                return render(request,'cloud/albums.html',context)
            else:
                context = {
                    'error_message':'your account is disabled'
                }
                return render(request,'cloud/login.html',context)
        else:
            context = {
                'error_message':'invalid login'
            }
            return (request,'cloud/login.html',context)
    context = {}
    return render(request,'cloud/login.html',context)

def user_logout(request):
    logout(request)
    return redirect('cloud:login')

@login_required
def create_album(request):
    form = AlbumForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        album = form.save(commit=False)
        album.user = request.user
        album.logo = request.FILES['logo']
        file_type = album.logo.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in ['png', 'jpg', 'jpeg']:
            form = AlbumForm(instance=album)
            context = {
                'album': album,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'cloud/add_album.html', context)
        album.save()
        return redirect('cloud:detail',pk=album.pk)
    context = {'form':form}
    return render(request,'cloud/add_album.html',context)

@login_required
def detail(request,pk):
    album = get_object_or_404(Album,pk=pk)
    context = {'album':album}
    return render(request,'cloud/detail.html',context)

@login_required
def add_song(request,pk):
    form = SongForm(request.POST or None,request.FILES or None)
    album = get_object_or_404(Album,pk=pk)
    if form.is_valid():
        for song in album.songs():
            if song.title == form.cleaned_data.get('title'):
                context = {
                    'form':form,
                    'message':'This song already exist',
                    'album': album
                }
                return render(request,'cloud/add_song.html',context)
        song = form.save(commit=False)
        song.album = album
        file_type =  song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in ['wav', 'mp3', 'ogg']:
            context = {
                'form':SongForm(instance=song),
                'message':'Audio file must be WAV, MP3, or OGG',
                'album':album
            }
            return render(request,'cloud/add_song.html',context)

        form.save()
        return redirect('cloud:detail', pk=album.pk)

    context = {'form':form,
               'album': album}
    return render(request,'cloud/add_song.html',context)

@login_required
def profile(request):
    albums = Album.objects.filter(user=request.user)
    context = {'albums':albums}
    return render(request,'cloud/albums.html',context)

@login_required
def delete_album(request,pk):
    album = get_object_or_404(Album,pk=pk)
    album.delete()

    return redirect('cloud:profile')