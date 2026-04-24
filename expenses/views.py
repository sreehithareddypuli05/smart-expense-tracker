"""
Views for Smart Expense Tracker.

All views are function-based for clarity and beginner-friendliness.
Pattern:
  - Auth views  → signup, login_view, logout_view
  - Expense views → dashboard, add_expense, edit_expense, delete_expense
"""

from django.shortcuts          import render, redirect, get_object_or_404
from django.contrib.auth       import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib            import messages
from django.db.models          import Sum

from .forms  import SignupForm, LoginForm, ExpenseForm
from .models import Expense


# ──────────────────────────────────────────────────────────────────────────────
# AUTH VIEWS
# ──────────────────────────────────────────────────────────────────────────────

def signup_view(request):
    """
    Handle new user registration.
    GET  → render blank signup form
    POST → validate, create user, log in automatically, redirect to dashboard
    """
    # Already logged in? Skip the form.
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()                       # Creates & hashes password
            login(request, user)                     # Log in immediately
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('dashboard')
        else:
            # Form errors will be displayed in template via {{ form.errors }}
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()

    return render(request, 'expenses/signup.html', {'form': form})


def login_view(request):
    """
    Handle user login.
    GET  → render login form
    POST → authenticate credentials, create session, redirect
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                # Respect ?next= parameter for deep-link redirects
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = LoginForm()

    return render(request, 'expenses/login.html', {'form': form})


def logout_view(request):
    """
    Log out the current user and redirect to the login page.
    POST-only for CSRF safety (the template submits a form).
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


# ──────────────────────────────────────────────────────────────────────────────
# EXPENSE VIEWS  (all require login)
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    """
    Main dashboard — shows expense list + spending summary.
    Supports optional filtering by category via GET parameter.
    """
    # Only fetch this user's expenses — never leaks other users' data
    expenses = Expense.objects.filter(user=request.user)

    # ── Optional category filter ──────────────────────────────────────────────
    selected_category = request.GET.get('category', '')
    if selected_category:
        expenses = expenses.filter(category=selected_category)

    # ── Aggregated stats ─────────────────────────────────────────────────────
    total_spending = expenses.aggregate(total=Sum('amount'))['total'] or 0.0

    # Category breakdown (for the doughnut chart and category cards)
    all_expenses = Expense.objects.filter(user=request.user)  # unfiltered for stats
    category_totals = (
        all_expenses.values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    # Build list of unique categories the user has used (for the filter dropdown)
    categories = list(all_expenses.values_list('category', flat=True).distinct())

    context = {
        'expenses':          expenses,
        'total_spending':    total_spending,
        'category_totals':   category_totals,
        'categories':        categories,
        'selected_category': selected_category,
        'expense_count':     all_expenses.count(),
        # Pass category data as lists for the JS chart
        'chart_labels':  [c['category'] for c in category_totals],
        'chart_data':    [c['total']    for c in category_totals],
    }
    return render(request, 'expenses/dashboard.html', context)


@login_required
def add_expense(request):
    """
    Render and process the Add Expense form.
    GET  → blank form
    POST → validate, save with current user, redirect to dashboard
    """
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)   # Don't save yet
            expense.user = request.user          # Attach logged-in user
            expense.save()
            messages.success(request, f'"{expense.title}" added successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ExpenseForm()

    return render(request, 'expenses/expense_form.html', {
        'form':       form,
        'form_title': 'Add Expense',
        'btn_label':  'Add Expense',
    })


@login_required
def edit_expense(request, pk):
    """
    Edit an existing expense.
    get_object_or_404 with user= ensures a user can't edit another user's expense.
    """
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{expense.title}" updated successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ExpenseForm(instance=expense)   # Pre-fill with existing data

    return render(request, 'expenses/expense_form.html', {
        'form':       form,
        'form_title': 'Edit Expense',
        'btn_label':  'Save Changes',
        'expense':    expense,
    })


@login_required
def delete_expense(request, pk):
    """
    Delete an expense after a POST confirmation.
    GET  → show confirmation page
    POST → delete and redirect
    """
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        title = expense.title
        expense.delete()
        messages.success(request, f'"{title}" deleted successfully.')
        return redirect('dashboard')

    return render(request, 'expenses/delete_confirm.html', {'expense': expense})