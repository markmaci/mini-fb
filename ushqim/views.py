from django.shortcuts import render, redirect
from datetime import datetime, timedelta
import random

def main(request):
    return render(request, 'ushqim/main.html')

def order(request):
    daily_specials = [
    {'name': 'Dolma', 'details': 'Stuffed grape leaves with rice and herbs'},
    {'name': 'Qofte', 'details': 'Grilled meatballs seasoned with spices'},
    {'name': 'Tavë Kosi', 'details': 'Baked lamb and rice with yogurt'},
    ]
    daily_special = random.choice(daily_specials)
    context = {
        'daily_special': daily_special,
    }

    return render(request, 'ushqim/order.html', context)

def confirmation(request):
    if request.method == 'POST':
        items = request.POST.getlist('item')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        instructions = request.POST.get('instructions')
        
        prices = {
            'burek': 5,
            'kadaif': 4,
            'baklava': 3,
            'dolma': 6,
            'qofte': 6,
            'tave kosi': 6,
        }

        if 'burek' in items:
            burek_option = request.POST.get('burek_option')
            items[items.index('burek')] = f"Burek ({burek_option})"
        
        total = 0
        for item in items:
            item_key = item.lower()
            total += prices.get(item_key, 0)
        
        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))

        context = {
            'items': items,
            'name': name,
            'phone': phone,
            'email': email,
            'instructions': instructions,
            'total': total,
            'ready_time': ready_time.strftime("%I:%M %p"),
        }
        return render(request, 'ushqim/confirmation.html', context)

    return redirect('ushqim:order')
