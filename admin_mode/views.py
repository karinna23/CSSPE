from django.forms import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

# Models
from account.models import Account, CustomUser

# Create your views here.
@login_required
def referees(request):
    if not request.user.is_superuser:
        return redirect('logout/')
    
    accounts = CustomUser.objects.filter(is_superuser=False)
    
    return render(request, 'admin/referees.html', {'accounts': accounts})

@login_required
def add_referee(request):
    if not request.user.is_superuser:
        return redirect('logout/')
    
    if request.method == 'POST':
        f_name = request.POST['f_name'].strip().capitalize()   # Remove leading and trailing spaces
        m_name = request.POST['m_name'].strip().capitalize()   # Remove leading and trailing spaces
        l_name = request.POST['l_name'].strip().capitalize()   # Remove leading and trailing spaces
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        arnis = 'arnis' in request.POST
        volleyB = 'volleyB' in request.POST
        tTennis = 'tTennis' in request.POST

        try:
            # Create the user with provided data using the CustomUser manager
            user = CustomUser.objects.create_user(
                username = username, 
                email = email, 
                password = password
            )

            # Create the Account instance and link it to the user
            Account.objects.create(
                user=user,
                first_name = f_name,
                middle_name = m_name,
                last_name = l_name,
                contact_num = '09972517522',
                arnis = arnis,
                volleyB = volleyB,
                tTennis = tTennis
            )

            return redirect('myapp:landing')

        except ValidationError as e:
            error_message = str(e)
        except:
            error_message = 'Error creating an Referee. Please try again later.'

        return render(request, 'admin/referees.html', {'error_message': error_message})

    
    return render(request, 'admin/add_referee.html')