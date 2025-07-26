from django.shortcuts import render,redirect
from Shop.froms import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .froms import CustomerDetailForm
from django.views import View

def home(request):
     
    return render(request,'shop/index.html')

def logout_page(request):

    if (request.user.is_authenticated):
        logout(request)
        messages.success(request,'Logged Out Successfully')
    return redirect('/')
def login_page(request):
    if (request.user.is_authenticated):
        return redirect('/')
    else:
        if request.method=="POST":
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect('customer_details')
            else:
                messages.error(request,'Invalid User Name or Password')
                return redirect('/login')
        return render(request,'shop/login.html')

def register(request):
    form=CustomUserForm()
    if request.method=="POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Success You can Login Now..! ')
            return redirect('/login')
        else:
            messages.warning(request,"Invalid Input Data")
    return render(request,'shop/register.html',{'form':form})


def collections(request):
        
    catagory = Category.objects.filter(status=0)
    
    return render(request,'shop/collections.html',{"catagory":catagory})

def collectionsview(request,name):
    if (Category.objects.filter(status=0)):
        products=Product.objects.filter(catagory__name=name)
        return render(request,'shop/products/index.html',{"products":products,"catagory_name":name})
    else:
        messages.warning(request,"No Such Catagory Found")
        return redirect('collections')
    
def product_details(request,cname,pname):
    
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,'shop/products/product_details.html',{"products":products})
        else:
            messages.error(request,"no Such Products Found")
            return redirect('collections')
    else:
        messages.error(request,"No Such Catagory Found")
        return redirect('collections')
    
def add_to_cart(request):
    if (request.headers.get('x-requested-with')=='XMLHttpRequest'):
        if (request.user.is_authenticated):
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status = Product.objects.get(id = product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id = product_id):
                    return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id = product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product Stock not available'},status=200)

            return JsonResponse({'status':'Product Added'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def cart_page(request):
    if (request.user.is_authenticated):
        cart = Cart.objects.filter(user = request.user)
        return render(request,'shop/cart.html',{'cart':cart})
    else:
        return redirect('/')
    
def remove_cart(request,cid):
  
    cartitem = Cart.objects.get(id = cid)
    cartitem.delete()
    return redirect('/cart')

def fav_page(request):
    if (request.headers.get('x-requested-with')=='XMLHttpRequest'):
        if (request.user.is_authenticated):
            data=json.load(request)
            product_id=data['pid']
            product_status = Product.objects.get(id = product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id = product_id):
                    return JsonResponse({'status':'Product Already in Favourite'},status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id = product_id)
                    return JsonResponse({'status':'Product Added to Favourite'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Favourite'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def favviewpage(request):

    if (request.user.is_authenticated):
        fav = Favourite.objects.filter(user = request.user)
        return render(request,'shop/fav.html',{'fav':fav})
    else:
        return redirect('/')
    
def remove_fav(request,fid):
  
    item = Favourite.objects.get(id = fid)
    item.delete()
    return redirect('/favviewpage')


@login_required
def customer_details(request):
    # Check if the user already has customer details
    existing_details = CustomerDetail.objects.filter(user=request.user).first()
    print(f"Existing details found: {existing_details}")
    print(f"Checking customer details for user: {request.user.username}")


    # If details exist, redirect to another page (e.g., home)
    if existing_details:
        return redirect('home')  # Redirect to your desired view (e.g., home page)

    # Retrieve cart details for the current user
    cart = Cart.objects.filter(user=request.user)

    if (request.method == 'POST'):
        form = CustomerDetailForm(request.POST)
        
        if form.is_valid():
            # Save the customer details
            customer_detail = form.save(commit=False)
            customer_detail.user = request.user  # Link the customer detail to the user
            customer_detail.save()
            print(f"Customer details saved: {customer_detail}")  # Debugging output

            # Associate the cart items with the customer and save them
            for item in cart:
                item.customer_detail = customer_detail  # Link the cart item to the customer
                item.status = 'Processed'  # Set the status of the cart item
                item.save()  # Save the updated cart item
                print(f"Processing cart item: {item}")  # Debugging output

            # Add a success message and redirect to the home page
            messages.success(request, "Your order has been successfully placed!")
            return redirect('home')
        else:
            # Print form errors for debugging
            print("Form is invalid. Errors:")
            print(form.errors)
    else:
        form = CustomerDetailForm()

    # Render the form and cart data together
    return render(request, 'shop/customer_details.html', {'form': form})


def address(request):
    # Retrieve address details for the current user
    add = CustomerDetail.objects.filter(user=request.user).distinct()
    return render(request, 'shop/address.html', {'add': add})
class updateAddress(View):
    def get(self, request, pk):
        add = CustomerDetail.objects.get(pk=pk)
        form = CustomerDetailForm(instance=add)
        return render(request,'shop/updateAddress.html',locals())
    def post(self, request, pk):
        add = CustomerDetail.objects.get(pk=pk)  # Get the address instance
        form = CustomerDetailForm(request.POST, instance=add)  # Pass the instance to the form
        
        if form.is_valid():
            form.save()  # Save the form directly instead of manually updating fields
            messages.success(request, "Your Address Updated Successfully.")
        else:
            messages.warning(request, "Invalid Input Data")
        
        return redirect('address')

 
def checkout(request):
    if (request.user.is_authenticated):
        add = CustomerDetail.objects.filter(user=request.user).distinct()
        cart = Cart.objects.filter(user=request.user)
        # Calculate total cost and include Rs. 40
        total_cost = sum(item.product.price * item.product_qty for item in cart) + 40
        return render(request, 'shop/checkout.html', {'add': add, 'cart': cart, 'total_cost': total_cost})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('login')
