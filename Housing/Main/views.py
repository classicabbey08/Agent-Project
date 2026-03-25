from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm
from .models import Property, SavedProperty


def home(request):
    # Show 3 featured active properties on homepage
    featured = Property.objects.filter(status='active').order_by('-created_at')[:3]
    return render(request, 'home.html', {'featured': featured})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            user.profile.role = role
            user.profile.save()
            login(request, user)
            messages.success(request, f'Welcome to NaijaNest, {user.username}!')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required(login_url='/login/')
def dashboard(request):
    role = request.user.profile.role
    if role == 'agent':
        # Agent dashboard — their listings and enquiries
        my_listings = Property.objects.filter(owner=request.user).order_by('-created_at')
        total_views  = sum(p.views for p in my_listings)
        context = {
            'my_listings':  my_listings,
            'total_views':  total_views,
            'listing_count': my_listings.filter(status='active').count(),
        }
        return render(request, 'agent_dashboard.html', context)

    # Tenant dashboard — saved properties
    saved = SavedProperty.objects.filter(user=request.user).select_related('property')
    recommended = Property.objects.filter(status='active').order_by('-created_at')[:3]
    context = {
        'saved_properties': saved,
        'recommended':      recommended,
    }
    return render(request, 'tenant_dashboard.html', context)


def property_list(request):
    properties = Property.objects.filter(status='active')

    # ── Filters ──
    prop_type  = request.GET.get('type', '')
    location   = request.GET.get('location', '')
    bedrooms   = request.GET.get('bedrooms', '')
    max_price  = request.GET.get('max_price', '')

    if prop_type:
        properties = properties.filter(property_type=prop_type)
    if location:
        properties = properties.filter(location__icontains=location)
    if bedrooms:
        if bedrooms == 'selfcon':
            properties = properties.filter(bedrooms=0)
        else:
            properties = properties.filter(bedrooms=int(bedrooms))
    if max_price:
        properties = properties.filter(price__lte=int(max_price))

    properties = properties.order_by('-created_at')

    context = {
        'properties':      properties,
        'total':           properties.count(),
        'selected_type':   prop_type,
        'selected_loc':    location,
        'selected_bed':    bedrooms,
        'selected_price':  max_price,
    }
    return render(request, 'property_list.html', context)


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)

    # Increment view count
    property.views += 1
    property.save()

    # Check if tenant has saved this property
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedProperty.objects.filter(
            user=request.user, property=property
        ).exists()

    # Similar properties — same location, exclude current
    similar = Property.objects.filter(
        status='active',
        location=property.location
    ).exclude(pk=pk)[:3]

    context = {
        'property': property,
        'is_saved': is_saved,
        'similar':  similar,
    }
    return render(request, 'property_detail.html', context)


@login_required(login_url='/login/')
def property_create(request):
    if request.method == 'POST':
        title         = request.POST.get('title')
        description   = request.POST.get('description')
        property_type = request.POST.get('property_type')
        listing_type  = request.POST.get('listing_type')
        location      = request.POST.get('location')
        address       = request.POST.get('address', '')
        price         = request.POST.get('price')
        bedrooms      = request.POST.get('bedrooms', 1)
        bathrooms     = request.POST.get('bathrooms', 1)
        toilets       = request.POST.get('toilets', 1)
        size          = request.POST.get('size') or None
        phone         = request.POST.get('phone')
        whatsapp      = request.POST.get('whatsapp', '')
        availability  = request.POST.get('availability', '')
        amenities     = request.POST.getlist('amenities')

        # Validate required fields
        if not all([title, description, property_type, listing_type, location, price, phone]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'property_create.html')

        # Create and save property
        prop = Property.objects.create(
            owner         = request.user,
            title         = title,
            description   = description,
            property_type = property_type,
            listing_type  = listing_type,
            location      = location,
            address       = address,
            price         = price,
            bedrooms      = bedrooms,
            bathrooms     = bathrooms,
            toilets       = toilets,
            size          = size,
            phone         = phone,
            whatsapp      = whatsapp,
            availability  = availability,
            status        = 'active',
            has_water     = 'water'    in amenities,
            has_light     = 'light'    in amenities,
            has_security  = 'security' in amenities,
            has_parking   = 'parking'  in amenities,
            has_cctv      = 'cctv'     in amenities,
            has_bq        = 'bq'       in amenities,
            has_kitchen   = 'kitchen'  in amenities,
            has_wardrobe  = 'wardrobe' in amenities,
            has_ac        = 'ac'       in amenities,
            has_pool      = 'pool'     in amenities,
        )

        # Handle image upload
        if 'images' in request.FILES:
            prop.image = request.FILES['images']
            prop.save()

        messages.success(request, 'Your property has been listed successfully!')
        return redirect('property_list')

    return render(request, 'property_create.html')


@login_required(login_url='/login/')
def save_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    saved, created = SavedProperty.objects.get_or_create(
        user=request.user,
        property=property
    )
    if not created:
        # Already saved — unsave it
        saved.delete()
        messages.info(request, 'Property removed from saved.')
    else:
        messages.success(request, 'Property saved successfully!')

    return redirect('property_detail', pk=pk)

def agents(request):
    return render(request, 'agents.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')