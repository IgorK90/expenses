from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import Transaction


def index(request):
    if request.user.is_authenticated:
        return redirect('/account')
    else:
        return render(request, 'index.html')


def account(request):
    user = request.user

    if not user.is_authenticated:
        return redirect("/")
    transactions = Transaction.objects.filter(user=user)
    return render(request, 'account.html', {'user': user,"transactions":transactions})

def create_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        if request.POST.get("type", "") == "expense":
            Transaction.objects.create(
                user=user,
                description=request.POST.get("description",""),
                amount=-abs(int(request.POST.get("amount",0)))
            )
        if request.POST.get("type","")=="income":
            Transaction.objects.create(
                user=user,
                description=request.POST.get("description",""),
                amount=abs(int(request.POST.get("amount",0))),
            )
        return redirect("/")
    # return render(request, "create.html")

    raise NotImplementedError

def delete_view(request:HttpRequest, transaction_id: int)->HttpResponse:
    Transaction.objects.filter(id=transaction_id).filter(user=request.user).delete()
    return redirect("/")

