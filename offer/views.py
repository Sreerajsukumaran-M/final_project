from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Offer
from .forms import OfferForm
from store.models import Store
from django.utils import timezone
from django.contrib import messages

@login_required
def create_offer(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    
    # Check if user owns the store
    if not request.user == store.user:
        messages.error(request, "You don't have permission to create offers for this store")
        return redirect('shop_dashboard')
    
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.store = store
            offer.save()
            messages.success(request, 'Offer created successfully!')
            return redirect('shop_offers', store_id=store.id)
    else:
        form = OfferForm()
    
    return render(request, 'offers/create_offer.html', {'form': form, 'store': store})

@login_required
def update_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    
    # Check if user owns the store
    if not request.user == offer.store.user:
        messages.error(request, "You don't have permission to edit this offer")
        return redirect('shop_dashboard')
    
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Offer updated successfully!')
            return redirect('shop_offers', store_id=offer.store.id)
    else:
        form = OfferForm(instance=offer)
    
    return render(request, 'offers/update_offer.html', {'form': form, 'offer': offer})

@login_required
def delete_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    
    # Check if user owns the store
    if not request.user == offer.store.user:
        messages.error(request, "You don't have permission to delete this offer")
        return redirect('shop_dashboard')
    
    store_id = offer.store.id
    offer.delete()
    messages.success(request, 'Offer deleted successfully!')
    return redirect('shop_offers', store_id=store_id)

@login_required
def shop_offers(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    
    # Check if user owns the store
    if not request.user == store.user:
        messages.error(request, "You don't have permission to view these offers")
        return redirect('shop_dashboard')
    
    offers = Offer.objects.filter(store=store).order_by('-start_date')
    return render(request, 'offers/shop_offers.html', {'offers': offers, 'store': store})

def mall_offers(request, mall_id):
    current_time = timezone.now()
    offers = Offer.objects.filter(
        store__mall_id=mall_id,
        start_date__lte=current_time,
        end_date__gte=current_time,
        is_active=True
    ).order_by('-start_date')
    return render(request, 'offers/mall_offers.html', {'offers': offers})

def store_offers(request, store_id):
    current_time = timezone.now()
    offers = Offer.objects.filter(
        store_id=store_id,
        start_date__lte=current_time,
        end_date__gte=current_time,
        is_active=True
    ).order_by('-start_date')
    store = get_object_or_404(Store, id=store_id)
    return render(request, 'offers/store_offers.html', {'offers': offers, 'store': store})