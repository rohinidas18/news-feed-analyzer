from django.shortcuts import render
from .main_func import main_func, pick_up, jsonify_df

# Create your views here.

def home(request):
    if request.POST.get("update"): main_func()
    
    ind = request.POST.get("select")
    res = pick_up(ind)
    jarr = jsonify_df(res)

    return render(request, "index.html", jarr)
