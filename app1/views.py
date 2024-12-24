from django.shortcuts import render,redirect
from . models import *
from . forms import *
import datetime
from django.db.models import Sum
# Create your views here.

def indexPage(request):
    if request.method=='POST':
        Expense=ExpenseForm(request.POST)
        if Expense.is_valid():
            Expense.save()
    expenses=expense.objects.all()
    total_expenses=expenses.aggregate(Sum('amount'))

    # Logic to calculate 365 days expense
    last_year=datetime.date.today() - datetime.timedelta(days=365)
    data=expense.objects.filter(date__gt=last_year)
    yearly_sum=data.aggregate(Sum('amount'))

    # Logic to calculate 30 days expense
    last_month=datetime.date.today() - datetime.timedelta(days=30)
    data=expense.objects.filter(date__gt=last_month)
    monthly_sum=data.aggregate(Sum('amount'))

    # Logic to calculate last week expense
    last_week=datetime.date.today() - datetime.timedelta(days=7)
    data=expense.objects.filter(date__gt=last_week)
    weekly_sum=data.aggregate(Sum('amount'))

    # Logic to calculate daily expense
    today_exp=datetime.date.today()-datetime.timedelta(days=1)
    data=expense.objects.filter(date__gt=today_exp)
    today_sum=data.aggregate(Sum('amount'))

    # Expense on particular date
    daily_sums=expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))

    # Expense on particular date
    categorical_sums=expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    
    expense_form=ExpenseForm()
    return render(request,'index.html',{'expense_form':expense_form,'expenses':expenses,'total_expenses':total_expenses,'yearly_sum':yearly_sum,'weekly_sum':weekly_sum,'monthly_sum':monthly_sum,'daily_sums':daily_sums,'categorical_sums':categorical_sums,'today_sum':today_sum})

def edit(request,id):
    Expense=expense.objects.get(id=id)
    expense_form=ExpenseForm(instance=Expense)
    if request.method=="POST":
        Expense=expense.objects.get(id=id)
        form=ExpenseForm(request.POST,instance=Expense)
        if form.is_valid():
            form.save()
            return redirect(indexPage)
    return render(request,'edit.html',{'expense_form':expense_form})

def delete(request,id):
    Expense=expense.objects.get(id=id)
    Expense.delete()
    return redirect(indexPage)