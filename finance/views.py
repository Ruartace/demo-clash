import json
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.utils import timezone
import openpyxl
from .models import Income, Expense

@csrf_exempt
def add_transaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            type_ = data.get('type')
            
            if type_ == 'income':
                obj = Income.objects.create(
                    amount=data['amount'],
                    note=data.get('description', ''),
                    date=data.get('date', timezone.now().date())
                )
            elif type_ == 'expense':
                obj = Expense.objects.create(
                    amount=data['amount'],
                    note=data.get('description', ''),
                    date=data.get('date', timezone.now().date())
                )
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid type'}, status=400)
                
            return JsonResponse({'status': 'success', 'id': obj.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@csrf_exempt
def delete_transaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_ = data.get('id')
            type_ = data.get('type')

            if not id_ or not type_:
                return JsonResponse({'status': 'error', 'message': 'No no id or type'}, status=400)

            if type_ == 'income':
                try:
                    obj = Income.objects.get(id=id_)
                    obj.delete()
                except Income.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Income not found'}, status=404)
            elif type_ == 'expense':
                try:
                    obj = Expense.objects.get(id=id_)
                    obj.delete()
                except Expense.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Expense not found'}, status=404)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid type'}, status=400)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

def get_transactions(request):
    # Combine income and expense, sort by date
    incomes = Income.objects.all().values('id', 'date', 'amount', 'note', 'category')
    expenses = Expense.objects.all().values('id', 'date', 'amount', 'note', 'category')
    
    data = []
    for i in incomes:
        i['type'] = 'income'
        i['description'] = i.pop('note', '') # Map note to description for frontend
        data.append(i)
        
    for e in expenses:
        e['type'] = 'expense'
        e['description'] = e.pop('note', '')
        data.append(e)
    
    # Sort by date descending
    data.sort(key=lambda x: str(x['date']), reverse=True)
    
    return JsonResponse({'transactions': data})

def dashboard_stats(request):
    # Calculate current month's balance
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    # Aggregate income and expense
    income = Income.objects.filter(
        date__year=current_year,
        date__month=current_month,
    ).aggregate(total=Sum('amount'))['total'] or 0

    expense = Expense.objects.filter(
        date__year=current_year,
        date__month=current_month,
    ).aggregate(total=Sum('amount'))['total'] or 0

    balance = income - expense

    return JsonResponse({
        'month': current_month,
        'year': current_year,
        'income': income,
        'expense': expense,
        'balance': balance
    })

def export_excel(request):
    # Create a workbook and add a worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Transactions"

    # Add headers
    headers = ['Date', 'Type', 'Amount', 'Description/Note']
    ws.append(headers)

    # Set column widths
    ws.column_dimensions['A'].width = 15
    ws.column_dimensions['B'].width = 10
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 30

    # Get data
    incomes = Income.objects.all()
    expenses = Expense.objects.all()
    
    all_txs = []
    for i in incomes:
        all_txs.append({'date': i.date, 'type': 'Income', 'amount': i.amount, 'desc': i.note})
    for e in expenses:
        all_txs.append({'date': e.date, 'type': 'Expense', 'amount': e.amount, 'desc': e.note})
        
    all_txs.sort(key=lambda x: x['date'], reverse=True)

    for t in all_txs:
        ws.append([
            t['date'].strftime('%Y-%m-%d') if t['date'] else '',
            t['type'],
            t['amount'],
            t['desc']
        ])

    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=transactions.xlsx'
    
    wb.save(response)
    return response
