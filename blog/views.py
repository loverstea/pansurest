from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Photo, Rating
from .forms import PhotoForm
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.db.models import Avg


def photo_detail(request, pk):
    photo = get_object_or_404(Photo, id=pk)
    average_rating = Rating.objects.filter(
        image=photo
    ).aggregate(Avg("value"))["value__avg"]

    rating_count = Rating.objects.filter(
        image=photo
    ).count()

    return render(request, "blog/photo_detail.html", {
        "photo": photo,
        "average_rating": average_rating,
        "rating_count": rating_count,
    })

def profile(request, username):

    user = get_object_or_404(User, username=username)

    photos = Photo.objects.filter(user=user).order_by('-created_at')

    return render(request, 'blog/profile.html', {
        'profile_user': user,
        'photos': photos
    })

def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('/')
    else:

        form = RegisterForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )

def photo_list(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'blog/photo_list.html', {'photos': photos})

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()

    return render(request, 'blog/upload_photo.html', {'form': form})

@login_required
def delete_photo(request, pk):

    photo = get_object_or_404(Photo, pk=pk)

    if photo.user != request.user and not request.user.is_staff:
        return redirect('photo_list')

    photo.delete()

    return redirect('photo_list')

@login_required
def edit_photo(request, pk):

    photo = get_object_or_404(Photo, pk=pk)

    if photo.user != request.user and not request.user.is_staff:
        return redirect('photo_list')

    if request.method == 'POST':

        form = PhotoForm(
            request.POST,
            request.FILES,
            instance=photo
        )

        if form.is_valid():
            form.save()
            return redirect('photo_list')

    else:
        form = PhotoForm(instance=photo)

    return render(request, 'blog/edit_photo.html', {
        'form': form
    })

@login_required
def rate(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if request.method == "POST":
        value = int(request.POST.get("value"))

        Rating.objects.update_or_create(
            user=request.user,
            image=photo,
            defaults={"value": value}
        )

    return redirect("photo_detail", pk=photo.id)