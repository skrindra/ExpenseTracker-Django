from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    if request.method == "POST":
        expense_form = ExpenseForm(request.POST)
        
        if expense_form.is_valid():
            expense = Expense(user=request.user, 
                              name=expense_form.cleaned_data['name'], 
                              category=expense_form.cleaned_data['category'], 
                              amount=expense_form.cleaned_data['amount'])
            expense.save()

    expenses = Expense.objects.filter(user=request.user)
    total_expense = expenses.aggregate(Sum('amount'))
    # print(total_expense)

    # Logic to calulate 1 year expenses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(user=request.user,date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))

    # Logic to calulate monthy expenses
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expense.objects.filter(user=request.user,date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))

    # Logic to calulate weekly expenses
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = Expense.objects.filter(user=request.user,date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))

    # Logic to calculate daily expenses
    daily_sums = Expense.objects.filter(user=request.user).values('date').order_by('date').annotate(sum=Sum('amount'))
    # print(daily_sums)

    # Logic to calculate category expenses
    categorical_sums = Expense.objects.filter(user=request.user).values('category').order_by('category').annotate(sum=Sum('amount'))
    
    # print(categorical_sums)
    expense_form = ExpenseForm()
    return render(request,'myapp/index.html',
                  {'expense_form':expense_form , 
                   'expenses':expenses,'total_expense':total_expense,
                   'yearly_sum':yearly_sum,'monthly_sum':monthly_sum,'weekly_sum':weekly_sum,
                   'daily_sums':daily_sums,
                   'categorical_sums':categorical_sums})


def edit(request, id):
    expense = Expense.objects.filter(user=request.user, id=id).first()
    if expense:
        expense_form = ExpenseForm(instance=expense)
        if request.method == "POST":
            expense_form = ExpenseForm(request.POST, instance=expense)
            if expense_form.is_valid():
                expense_form.save()
                return redirect('index')
    
    return render(request, 'myapp/edit.html', {'expense_form': expense_form})




def delete(request,id):
    expense = Expense.objects.filter(user=request.user,id=id)
    expense.delete()
    return redirect('index')