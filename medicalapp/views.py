from django.shortcuts import render, redirect
from .models import customer  
from django.contrib import messages
from django.db import IntegrityError
from .models import Medicine
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404



def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Initialize error messages
        errors = {}

        # Check if username is empty
        if not username:
            errors['username'] = "Username cannot be empty."

        # Check if username already exists
        if customer.objects.filter(username=username).exists():
            errors['username'] = "This username is already taken."

        # Check if passwords match
        if password != confirm_password:
            errors['password'] = "Passwords do not match."
        
        # Check for minimum password length
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters long."

        # If there are no errors, create the user
        if not errors:  # Proceed only if there are no errors
            new_customer = customer(username=username, password=password)  # Store plain text password
            
            try:
                new_customer.save()  # Save the user instance
                messages.success(request, "Sign up successful! You can now log in.")
                return redirect('login_page')  # Redirect to login page after successful signup
            except IntegrityError:
                messages.error(request, "An error occurred. Please try again.")

        # If there are errors, display them as messages
        for key, value in errors.items():
            messages.error(request, value)

    return render(request, 'html/signup.html')  # Render the signup template



#login page views

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        try:
            # Fetch the user from the database
            user = customer.objects.get(username=username)  # Ensure 'Customer' is your correct model name
        except customer.DoesNotExist:
            # User not found, redirect to sign up
            messages.error(request, 'User not found, please sign up.')
            return redirect('signup')

        # Compare plain text passwords (Note: It's better to hash passwords in the future for security)
        if password == user.password:
            # Login successful, set session data
            request.session['customer_id'] = user.id  # Store user ID in session

            messages.success(request, "Login successful!")
            return redirect('home')  # Redirect to home or another page
        else:
            # Invalid credentials
            messages.error(request, 'Invalid username or password.')
            return render(request, 'html/login.html')

    return render(request, 'html/login.html')

#home_page view

def home_page(request):
    return render(request,'html/home.html')



#adding medicine views


def add_medicine(request):
    # Check if the user is logged in by checking session data
    if 'customer_id' not in request.session:
        return redirect('login_page')  # Redirect to the login page if not logged in

    # Get the logged-in customer based on session data
    current_customer =  customer.objects.get(id=request.session['customer_id'])

    # Count how many medicines have been added by the current customer
    medicines_count = Medicine.objects.filter(user=current_customer).count()

    if request.method == "POST":
        # Check if the customer has reached the limit of 5 medicines
        if medicines_count >= 5:
            return render(request, 'html/add_medicine.html', {'error': 'You can only add up to 5 medicines.'})

        # Get the data from the form
        name = request.POST.get('name')
        stock = request.POST.get('stock')

        # Check if the data is captured correctly
        if not name or stock is None:
            return render(request, 'html/add_medicine.html', {'error': 'Please fill in all fields.'})

        # Create a new medicine instance associated with the current customer and save it
        Medicine.objects.create(name=name, stock=stock, user=current_customer)

   

    # Render the form for GET request
    return render(request, 'html/add_medicine.html')



#listing_medicine



def list_medicines(request):
    # Check if the user is logged in by checking session data
    if 'customer_id' not in request.session:
        return redirect('login_page')  # Redirect to the login page if not logged in

    # Get the logged-in customer based on session data
    current_customer = customer.objects.get(id=request.session['customer_id'])

    query = request.GET.get('q', '')

    if query:
        # Filter medicines added by the current customer and matching the query
        medicines = Medicine.objects.filter(name__icontains=query, user=current_customer)
    else:
        # Show all medicines added by the current customer
        medicines = Medicine.objects.filter(user=current_customer)

    paginator = Paginator(medicines, 3)  # Show 3 medicines per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Check if the request is AJAX
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax:
        return render(request, 'html/medicine_rows.html', {'page_obj': page_obj})

    return render(request, 'html/list_medicine.html', {'page_obj': page_obj})




#edit medicines


def edit_medicine(request, medicine_id):
    # Get the medicine object or return a 404 error if not found
    medicine = get_object_or_404(Medicine, id=medicine_id)
    
    if request.method == 'POST':
        # Update the medicine fields from the form data
        medicine.name = request.POST.get('name')
        medicine.stock = request.POST.get('stock')
        
        # Save the updated medicine instance
        medicine.save()
        
        # Redirect to the list of medicines after saving
        return redirect('list_medicines')
    
    # Render the edit medicine template with the medicine instance
    return render(request, 'html/edit_medicine.html', {'medicine': medicine})


# delete medicines

def delete_medicine(request, medicine_id):
    # Get the medicine object or return a 404 error if not found
    medicine = get_object_or_404(Medicine, id=medicine_id)
    
    if request.method == 'POST':
        # Delete the medicine instance
        medicine.delete()
       
        return redirect('list_medicines')
    
    # If not POST, render a confirmation template (optional)
    return render(request, 'html/list_medicine.html', {'medicine': medicine})

#logout views


def logout_view(request):
    # Clear the session
    request.session.flush()

    # Optionally, display a success message
    messages.success(request, "You have successfully logged out.")

    # Redirect to the login page or another page
    return redirect('login_page')

#contact us view

def contact_us(request):
    return render(request,'html/contactus.html')