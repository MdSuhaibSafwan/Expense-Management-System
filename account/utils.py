from django.db.models import Q
from django.contrib.auth import get_user_model
from account.models import Account, FundTransfer
from expense.models import Expense
from openpyxl import Workbook

User = get_user_model()


def take_first(lst):
	return lst[0]


def report_for_an_account(account):
	ledger_list = []

	qs = FundTransfer.objects.filter(from_account=account)
	from_acc_temp_lst = list(qs.values_list("date_created", "to_account__name", "id", "amount"))
	temp_lst = []
	for i in from_acc_temp_lst:
		i = list(i)
		i.append(False)
		temp_lst.append(i)

	ledger_list.extend(temp_lst)

	qs = FundTransfer.objects.filter(to_account=account)
	to_acc_temp_lst = list(qs.values_list("date_created", "from_account__name", "id", "amount"))
	temp_lst = []
	for i in to_acc_temp_lst:
		i = list(i)
		i.append(True)
		temp_lst.append(i)

	ledger_list.extend(temp_lst)

	expense_temp_lst = list(Expense.objects.filter(account=account).values_list("date_created", "title", "id", "cost"))	
	for i in expense_temp_lst:
		i = list(i)
		i.append(True)
		temp_lst.append(i)

	ledger_list.extend(temp_lst)

	# ledger_list = list(FundTransfer.objects.filter(Q(from_account=account) | 
	# 		Q(to_account=account)).values_list("date_created", "id", "amount"))
	# ledger_list.extend(list(Expense.objects.filter(account=account).values_list("date_created", "id", "cost")))

	sorted_ledger_list = sorted(ledger_list, key=take_first)	
	return sorted_ledger_list


def create_worksheet_for_account_report(account, response):
	sorted_ledger_list = account_report(account)
	headers = ["date", "content_obj_id", "amount", "debit", "credit"]
	wb = Workbook()
	ws = wb.active
	ws.title = "Account Worksheet"
	ws.append(headers)

	for account in sorted_ledger_list:
		print(account)

	# wb.save(response)
	return wb, response



def account_report(account):
	ft_qs = FundTransfer.objects.filter(Q(from_account=account) | Q(to_account=account))
	ledger_list = []
	for ft_obj in ft_qs:
		if ft_obj.from_account == account:
			title = f"Outgoing Fund transfer from {account} to {ft_obj.to_account}"
			dr_cr = "DR"
		else:
			title = f"Fund Inserted for a transfer from {ft_obj.from_account} to {account}"
			dr_cr = "CR"

		temp_lst = [ft_obj.transaction_code, title, ft_obj.amount, dr_cr]
		ledger_list.append(temp_lst)
		
	expense_qs = Expense.objects.filter(account=account)
	for exp_obj in expense_qs:
		temp_lst = [exp_obj.transaction_code, exp_obj.title, exp_obj.cost, "DR"]
		ledger_list.append(temp_lst)

	return ledger_list

