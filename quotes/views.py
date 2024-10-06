import random
from django.shortcuts import render

# Create your views here.

quotes = [
    {
        'text': "Hello there!",
        'image': "images/obi-wan-kenobi-revenge-of-the-sith.jpg.jpeg",
        'era': "Revenge of the Sith",
    },
    {
        'text': "These aren't the droids you're looking for.",
        'image': "images/Obi-Wan-Kenobi-in-Star-Wars-A-New-Hope.jpeg",
        'era': "A New Hope",
    },
    {
        'text': "Only a Sith deals in absolutes.",
        'image': "images/obi-wan-kenobi-revenge-of-the-sith.jpg.jpeg",
        'era': "Revenge of the Sith",
    },
    {
        'text': "The Force will be with you, always.",
        'image': "images/Obi-Wan-Kenobi-in-Star-Wars-A-New-Hope.jpeg",
        'era': "A New Hope",
    },
    {
        'text': "You were the chosen one!",
        'image': "images/obi-wan-kenobi-revenge-of-the-sith.jpg.jpeg",
        'era': "Revenge of the Sith",
    },
    {
        'text': "I have the high ground!",
        'image': "images/obi-wan-kenobi-revenge-of-the-sith.jpg.jpeg",
        'era': "Revenge of the Sith",
    },
    {
        'text': "Strike me down, and I will become more powerful than you can possibly imagine.",
        'image': "images/Obi-Wan-Kenobi-in-Star-Wars-A-New-Hope.jpeg",
        'era': "A New Hope",
    },
    {
        'text': "In my experience, there's no such thing as luck.",
        'image': "images/Obi-Wan-Kenobi-in-Star-Wars-A-New-Hope.jpeg",
        'era': "A New Hope",
    },
    {
        'text': "So uncivilized.",
        'image': "images/obi-wan-kenobi-revenge-of-the-sith.jpg.jpeg",
        'era': "Revenge of the Sith",
    },
    {
        'text': "Your eyes can deceive you. Don’t trust them.",
        'image': "images/Obi-Wan-Kenobi-in-Star-Wars-A-New-Hope.jpeg",
        'era': "A New Hope",
    },
    {
        'text': "Who's more foolish? The fool or the fool who follows him?",
        'image': "images/Obi-Wan-Kenobi-in-Star-Wars-A-New-Hope.jpeg",
        'era': "A New Hope",
    },
    {
        'text': "You must do what you feel is right, of course.",
        'image': "images/Obi-Wan-Kenobi-in-Star-Wars-A-New-Hope.jpeg",
        'era': "A New Hope",
    },
    {
        'text': "You cannot escape your destiny.",
        'image': "images/Ewan-McGregor-as-Obi-Wan-in-The-Phantom-Menace.jpeg",
        'era': "The Phantom Menace",
    },
    {
        'text': "That's no moon. It's a space station.",
        'image': "images/Obi-Wan-Kenobi-in-Star-Wars-A-New-Hope.jpeg",
        'era': "A New Hope",
    },
    {
        'text': "Be mindful of your thoughts, Anakin, they betray you.",
        'image': "images/Obi-Wan-in-Star-Wars-Episode-II-Attack-of-the-Clones.jpeg",
        'era': "Attack of the Clones",
    },
    {
        'text': "You were my brother, Anakin. I loved you.",
        'image': "images/obi-wan-kenobi-revenge-of-the-sith.jpg.jpeg",
        'era': "Revenge of the Sith",
    },
    {
        'text': "Why do I get the feeling you're going to be the death of me?",
        'image': "images/Obi-Wan-in-Star-Wars-Episode-II-Attack-of-the-Clones.jpeg",
        'era': "Attack of the Clones",
    },
    {
        'text': "If you strike me down, I shall become more powerful than you can possibly imagine.",
        'image': "images/Obi-Wan-Kenobi-in-Star-Wars-A-New-Hope.jpeg",
        'era': "A New Hope",
    },
    {
        'text': "Anakin, Chancellor Palpatine is evil!",
        'image': "images/Obi-Wan-in-Star-Wars-Episode-II-Attack-of-the-Clones.jpeg",
        'era': "Revenge of the Sith",
    }
]

def quote(request):
    selected_quote = random.choice(quotes)
    context = {
        'quote': selected_quote,
    }
    return render(request, 'quotes/quote.html', context)


def show_all(request):
    context = {
        'quotes': quotes,
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    return render(request, 'quotes/about.html')

