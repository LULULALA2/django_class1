from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model #사용자가 있는지 검사하는 함수
from django.contrib import auth # 사용자 auth 기능
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')


        if password != password2:
            # 패스워드가 같지 않다고 알람
            return render(request, 'user/signup.html', {'error':'패스워드를 확인해 주세요!'})
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '사용자 이름과 비밃번호는 필수입니다!'})

            # username이 내가 지금 입력한 username이랑 같은 사용자가 있는지의 조건(filter)으로 검색한다
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user: # 필터링된 유저가 존재한다면
                # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
                return render(request, 'user/signup.html', {'error': '사용자가 존재합니다.'})
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in')  # 회원가입이 완료되었으므로 로그인 페이지로 이동


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 사용자 불러오기
        me = auth.authenticate(request, username=username, password=password)
        # me = UserModel.objects.get(username=username) # get: 데이터가 무조건 있어야 됨, 없으면 Error
        # 데이터베이스 UserModel에서 username과 같은 정보를 불러와서 me에 저장

        if me is not None:
            auth.login(request, me)
        # if me.password == password: # 저장된 사용자의 pw와 입력받은 pw 비교
        #     request.session['user'] = me.username # 세션에 사용자 이름 저장
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error':'유저이름과 패스워드를 확인해주세요;ㅅ;'})



    elif request.method == 'GET':
        return render(request, 'user/signin.html')


@login_required # 로그인 한 사용자만 접근 할 수 있게 해 주는 기능
def logout(request):
    auth.logout(request) # 인증 되어있는 정보를 없애기
    return redirect("/")


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')