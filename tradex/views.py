from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.http import HttpRequest
from django.contrib import messages
from django.db import IntegrityError
from .models import Wallet,Tradxtar,Asset
from .models import Escrowsale
from decimal import Decimal
# Create your views here.

def homePage(request):
    return HttpResponse("<h2 align='center' style='color : green;'>  HELLO TRADEXER </h2>")
def aboutPage(request):
    return HttpResponse("<h2 align='center' style='color : green;'>  ABOUTPAGE </h2>")
def contactPage(request):
    return HttpResponse("<h2 align='center' style='color : green;'>  CONTACTPAGE </h2>")

def getspecificAsset(request):
    try :
        asset1 = Asset.objects.get(pk=1)
        print(asset1)
    
        html = f"""
           <h2>Asset</h2>
           <p>{asset1.name}</p>
           <p>{asset1.price}</p>
           """
    except:
        html ="""
            <h2>Not Found</h2>  
        """
    return HttpResponse(html)

@login_required(login_url='tradex-login-page')
def updateSpecificAsset(request):
    try:
        asset1 = Asset.objects.get(pk=1)
        asset1.name= "XTRA-STUB"
        asset1.save()
    except:
        html ="""
            <h2>Not Found</h2> 
            <p>Asset could not be updated</P>
        """
    return HttpResponse(html)

def signupview(request:HttpRequest):
    # user1 = User.objects.create_user(username="divine1",email="swissb506@gmail.com",password="di1vi2ne3")
    # user1.save()
    if request.method == "POST":
        username= request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        if password != password1 or len(password) < 8:
            return render(request,"auth/signup.html",{"error":"password do not match or minimum length of password not met"})
        if not username or not email :
           return render(request,"auth/signup.html",{"error":"username and email is required"}) 
        try:
            user_exist = User.objects.filter(username = username).first()
            if user_exist :
                return render(request,"auth/signup.html",{'error':"user already exist","success":None})
            # getting to this stage means we are good to signup the user
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            tradxtar = Tradxtar.objects.create(trader=user)
            tradxtar.save()
            return render(request,"auth/signup.html",{'error':None,"success":"signup successful"})
        except Exception as e :
            print(e)
    return render(request,"auth/signup.html",{'error':"Server Error","success":None})



'''if request.method == "POST":
        username =request.POST.get('username')
        email =request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if password1 != password2 or len(password1) < 8:
            print(password1)
            return render(request, "Auth/signup.html",{'error': "password does not match minimum length"})
        if not username or not email:
            return render(request, "Auth/signup.html",{"error":"username and email does not match"})
        try:
            user_exist = User.objects.filter(username=username).first()
            if user_exist: 
                return render(request,"auth/signup.html",{"error": "user already exist","sucess":None})
            user = User.objects.create_user(username=username, email = email, password=password1)
            user.save()
            tradxtar = Tradxtar.objects.create(trader=user)
            tradxtar.save()
            return render(request,"auth/signup.html",{"sucess":"user created successfully","error":None})
        except Exception as e:
            print(e)
            return render(request,"auth/signup.html",{"error":"user could not be created","sucess":None})
    return render(request,"auth/signup.html",{"error":None,"sucess":None})'''

def loginview(request:HttpRequest):
    # user1 = User.objects.create_user(username="divine1",email="swissb506@gmail.com",password="di1vi2ne3")
    # user1.save()
    if request.method == "POST":
        username= request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('/tradex/wallet/')
        else :
            return render(request,"auth/login.html",{'error':"Server Error","success":None})
        
    return render(request,"auth/login.html",{})
    
'''if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or password:
            return render(request, "auth/login.html", {"error": "username and password does not match", "success": None})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "auth/login.html", {"success": "Login successful", "error": None})
        else:
            return render(request, "auth/login.html", {"error": "Invalid credentials", "success": None})
    return render(request, "auth/login.html", {"error": None, "success": None})'''

# @login_required(login_url='/tradex/login/')
# def walletview(request):
    # return render(request,"user/walletpage.html",{})
@login_required(login_url='tradex-login-page')
def buyAssetview(request:HttpRequest,pk):
    try:
        asset = Asset.objects.get(pk = pk)
        if request.method == "POST":
            quantity_to_buy = Decimal(request.POST.get("buy-quantity"))
            amount_to_pay = asset.price * quantity_to_buy
            tradxtar = Tradxtar.objects.get(trader=request.user)
            if tradxtar.balance < amount_to_pay:
                raise Exception(f'Your Tradxtar balance is less than NGN{amount_to_pay}.')
                #return render(request,"user/buyasset.html",{'error':"Insufficient balance","asset":asset})
            user_wallet = Wallet.objects.get(holder= tradxtar, asset = asset)
            if not user_wallet:
                raise Exception(f'You do not have an asset wallet for{asset.symbol}.')
            
            tradxtar.balance -= amount_to_pay
            user_wallet_quantity += quantity_to_buy
            tradxtar.save()
            user_wallet.save()
            redirect("tradex-wallet-page")
        return render(request,"user/buyasset.html",{'asset':asset})
    except Exception as e:
        print(e)
        return render(request,"user/buyasset.html",{'error':str(e),'asset':asset})
   # return render(request,"user/buyasset.html",{})

@login_required(login_url='tradex-login-page')
def fundWalletview(request):
    return render(request,"user/fundwallet.html",{})

@login_required(login_url='tradex-login-page')
def offerview(request,pk):
    try:
        asset = Asset.objects.get(pk=pk)
        tradxtar= Tradxtar.objects.get(trader=request.user)
        user_wallet = Wallet.objects.get(holder=tradxtar, asset = asset)
        if not user_wallet:
            return redirect("tradex-create-wallet")
        
        if request.method == 'POST':
            price = Decimal(request.POST.get("instant-price"))
            quantity = Decimal(request.POST.get("quantity"))

            #perform 2 Validation
            #1. ensure the quantity the user wants to sell is greater than 0
            if quantity <0.00 or quantity > user_wallet.Quantity:
                return render(request,"user/offerview.html",{"error":"quantity to sell must be greater than 0 as well as not greater than the quantity in your wallet","user_wallet":user_wallet})
            
            if not price or price <= 0.00:
                return render(request,"user/offerview.html",{"error":"Specify your sell rate","user_wallet":user_wallet})
            
            sale_offer = Escrowsale.objects.create(wallet_seller = user_wallet, rate =price, quantity = quantity)
            sale_offer.save()
            user_wallet.save()
            return redirect("tradex-wallet-page")
        return render(request,"user/offerview.html",{"error": None, "user_wallet": user_wallet})
          
    
    except Exception as e :
        return render(request,"user/offerview.html",{"error": str(e)})

@login_required(login_url='tradex-login-page')
def myofferedAsset4sale(request):
    try:
        my_escrow_sales = Escrowsale.objects.filter(wallet_seller_holder_trader= request.user)

        context = {
            'my_escrow_sales': my_escrow_sales,
            "totalAssetCountonSale":len(my_escrow_sales)
        }
        print(context)
        return render(request, 'user/myAsset4Sale.html.',context)
    except Tradxtar.DoesNotExist:
        return redirect("tradex-wallet-Page")
    except Exception as e:
        return render(request,"user/myAsset4Sale.html",{"error":str(e)})
    
@login_required(login_url='/tradex/login')
def otherUserAssetOffer4Sales(request):
    try:
        tradxtar_profile = Tradxtar.objects.get(trader=request.user)
        my_wallets = Wallet.objects.filter(holder=tradxtar_profile)
        other_escrow_sales = EscrowSale.objects.exclude(wallet_seller__in=my_wallet)
        context ={
            "other_escrow_sales": other_escrow_sales,
            "totalAssetCountonSale":len(other_escrow_sales)
        }
        print(context)
        return render(request,"user/otherAsset4Sale.html",context)
    except Tradxtar.DoesNotExist:
        return redirect("tradex-wallet-page")
    except Exception as e:
        return render(request, 'user/otherAsset4Sale.html',{"error": str(e)})

@login_required(login_url='tradex-login-page')   
def onSaleview(request):
    return render(request,"user/onsale.html",{})

@login_required(login_url='tradex-login-page')
def bidExchangeview(request):
    return render(request,"user/bidexchange.html",{})

@login_required(login_url='tradex-login-page')
def logoutview(request):
    logout(request)
    return render(request,"auth/login.html",{"success":"logout successful","error":None})


#1st code
@login_required(login_url='tradex-login-page')
def createWalletView(request:HttpRequest):
    """
    View to handle the creation of a new wallet for the user.
    Displays a form to select an asset and processes the form submission.
    """
    # Fetch all available assets to populate the dropdown
    assets = Asset.objects.all()

    if request.method == 'POST':
        # Get the selected asset ID from the form
        asset_id = request.POST.get('asset')

        if not asset_id:
            messages.error(request, "Please select an asset.")
            return redirect('tradex-create-wallet') 

        try:
            # Get the selected Asset object
            asset = Asset.objects.get(id=asset_id)
            tradxtar = Tradxtar.objects.get(trader=request.user)

            # Check if a wallet for this asset already exists for the user
            if Wallet.objects.filter(holder=tradxtar, asset=asset).exists():
                messages.warning(request, f"You already have a wallet for {asset.symbol}.")
                return redirect('tradex-wallet-page') 

            # Create a new Wallet instance
            new_wallet = Wallet(holder=tradxtar, asset=asset)
            new_wallet.save()

            messages.success(request, f"Wallet for {asset.symbol} created successfully!")
            return redirect('tradex-wallet-page') 

        except Asset.DoesNotExist:
            messages.error(request, "Selected asset not found.")
            return redirect('tradex-create-wallet') 

        except Tradxtar.DoesNotExist:
            
            messages.error(request, "Your Tradxtar profile could not be found.")
            return redirect('profile') 

        except IntegrityError:
            messages.error(request, f"A wallet for {asset.symbol} already exists.")
            return redirect('tradex-wallet-page')

        except Exception as e:
            print(f"An error occurred during wallet creation: {e}")
            messages.error(request, "An unexpected error occurred while creating the wallet.")
            return redirect('create_wallet')
  
    context = {
        'assets': assets,
    }
    return render(request, "user/createWallet.html", context)


@login_required(login_url='tradex-login-page')
def walletView(request:HttpRequest):
    """
    View to display the user's wallet information.
    Fetches the user's Tradxtar profile and their associated wallets.
    """
    if request.user.is_superuser:
        return redirect("/admin")
    try:
        
        # Get or create the Tradxtar profile for the logged-in user
        tradxtar = Tradxtar.objects.get_or_create(trader=request.user)

        # Get all wallets belonging to this Tradxtar
        wallets = Wallet.objects.filter(holder=tradxtar[0]).select_related('asset') 

        # Prepare the context data to pass to the template
        context = {
            'tradxtar': tradxtar[0],
            'wallets': wallets,
            # 'total_asset_value': calculate_total_asset_value(wallets)
        }

        # Render the wallet page template with the context data
        return render(request, "user/walletpage.html", context)

    except Tradxtar.DoesNotExist:
        context = {
            'tradxtar': None, # Or a default Tradxtar object if appropriate
            'wallets': [],
            'error': 'Your Tradxtar profile could not be loaded.'
        }
        return render(request, "user/walletpage.html", context)

    except Exception as e:
        # Catch any other potential errors
        print(f"An error occurred in walletView: {e}")
        context = {
            'tradxtar': None,
            'wallets': [],
            'error': 'An unexpected error occurred while loading your wallet.'
        }
        return render(request, "user/walletpage.html", context)

