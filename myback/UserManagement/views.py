import json
import re
import jwt
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.conf import settings
from UserManagement.models import Users
# Create your views here.

@csrf_exempt
def auth_register(request):
    # 仅处理POST请求
    if request.method != 'POST':
        return JsonResponse({
            'code': 405,
            'message': 'Method Not Allowed'
        }, status=405)

    try:
        # 解析请求体
        usr_info = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            'code': 3001,
            'message': '参数不完整或格式错误'
        }, status=400)

    # 校验必填参数
    required_fields = ['name', 'email', 'password', 'confirmPassword']
    for field in required_fields:
        if field not in usr_info or not str(usr_info[field]).strip():
            return JsonResponse({
                'code': 3001,
                'message': '参数不完整或格式错误'
            }, status=400)

    # 修改字段名为username
    username = usr_info['name'].strip()  # 从请求参数获取username
    email = usr_info['email'].strip().lower()
    password = usr_info['password']
    confirm_password = usr_info['confirmPassword']

    # 验证用户名格式
    if len(username) < 2 or len(username) > 50:  # 变量名改为username
        return JsonResponse({
            'code': 3001,
            'message': '用户名称长度需在2-50个字符之间'
        }, status=400)

    # 验证邮箱格式
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({
            'code': 3001,
            'message': '邮箱格式无效'
        }, status=400)

    # 验证密码复杂度
    if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Za-z]', password):
        return JsonResponse({
            'code': 3001,
            'message': '密码需至少8个字符且包含字母和数字'
        }, status=400)

    # 验证确认密码
    if password != confirm_password:
        return JsonResponse({
            'code': 3002,
            'message': '密码和确认密码不一致'
        }, status=400)

    # 检查邮箱重复
    if Users.objects.filter(email__iexact=email).exists():
        return JsonResponse({
            'code': 3003,
            'message': '邮箱已被注册'
        }, status=409)

    # 检查用户名重复 (改为使用username字段)
    if Users.objects.filter(username__iexact=username).exists():
        return JsonResponse({
            'code': 3004,
            'message': '用户名已被使用'
        }, status=409)

    try:
        # 创建用户 (改为使用username字段)
        user = Users.objects.create(
            username=username,  # 注意这里字段名改为username
            email=email,
            hashed_password=make_password(password),  # 根据模型字段可能需要修改
            role = 'user',
            is_active=True,  # 默认激活
        )
        print(datetime.datetime.utcnow())
        # 生成JWT Token
        payload = {
            'sub': user.id,
            'role': user.role
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
         # 确保Token转换为字符串
        if isinstance(token, bytes):
            token = token.decode('utf-8')  # 处理PyJWT 1.x版本

        # 构造响应数据
        response_data = {
            'user': {
                'id': str(user.id),
                'name': user.username,
                'email': user.email,
                'role': user.role
            },
            'token': token
        }

        return JsonResponse(response_data, status=201)

    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }, status=500)
    
@csrf_exempt
def auth_login(request):
    # 处理登录请求
    if request.method != 'POST':
        return JsonResponse({
            'code': 405,
            'message': 'Method Not Allowed'
        }, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            'code': 1001,
            'message': '参数格式错误'
        }, status=400)

    # 验证必填参数
    # email = data.get('email', '').strip().lower()
    email = '1024@qq.com'
    # password = data.get('password', '').strip()
    password = "project1024"
    if not email or not password:
        return JsonResponse({
            'code': 1001,
            'message': '邮箱或密码不能为空'
        }, status=400)

    try:
        # 自定义认证逻辑（因为Django默认使用username）
        user = Users.objects.get(email__iexact=email)
        Users.objects.filter(email=email).update(is_active=True)  # 激活用户
        user.role = 'user'
        if not user.check_password(password):
            raise ValueError('密码错误')
    except ObjectDoesNotExist:
        return JsonResponse({
            'code': 1002,
            'message': '邮箱或密码错误'
        }, status=401)
    except ValueError as e:
        return JsonResponse({
            'code': 1002,
            'message': str(e)
        }, status=401)

    # 检查账户状态
    print(user.is_active)
    if not user.is_active:
        return JsonResponse({
            'code': 1003,
            'message': '账号已被禁用'
        }, status=403)

    # 生成JWT Token
    try:
        payload = {
            'sub': user.id,
            'role': user.role,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        print(token)
        # 处理不同版本的PyJWT返回值
        if isinstance(token, bytes):
            token = token.decode('utf-8')
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'令牌生成失败: {str(e)}'
        }, status=500)

    return JsonResponse({
        'user': {
            'id': str(user.id),
            'name': user.username,
            'email': user.email,
            'role': user.role
        },
        'token': token
    }, status=200)

@csrf_exempt
def show_user(request): 
    print("ok")
    res = Users.objects.all()
    for i in res:
        print(i.username)

# 辅助函数：验证管理员权限
def is_admin(user):
    return user.role == 'admin'

# 辅助函数：解析JWT Token
def get_user_from_token(request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return Users.objects.get(id=payload['sub'])
    except (jwt.ExpiredSignatureError, jwt.DecodeError, Users.DoesNotExist):
        return None

# 获取所有用户
@csrf_exempt
def get_users(request):
    if request.method != 'GET':
        return JsonResponse({'code': 405, 'message': 'Method Not Allowed'}, status=405)
    
    # 验证Token
    current_user = get_user_from_token(request)
    if not current_user:
        return JsonResponse({'code': 401, 'message': '未认证'}, status=401)
    
    # 检查管理员权限
    if not is_admin(current_user):
        return JsonResponse({'code': 403, 'message': '无权访问'}, status=403)
    
    # 处理查询参数
    q = request.GET.get('q', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')
    
    # 构建查询
    users = Users.objects.all()
    if q:
        users = users.filter(Q(username__icontains=q) | Q(email__icontains=q))
    if role_filter in ['user', 'admin']:
        users = users.filter(role=role_filter)
    if status_filter in ['active', 'inactive', 'banned']:
        users = users.filter(status=status_filter)
    
    # 构建响应数据
    user_list = [{
        "id": str(user.id),
        "name": user.username,
        "email": user.email,
        "role": user.role,
        "status": user.status,
        "createdAt": user.created_at.isoformat() + 'Z',
        "updatedAt": user.updated_at.isoformat() + 'Z',
        "lastLoginAt": user.last_login_at.isoformat() + 'Z' if user.last_login_at else None
    } for user in users]
    
    return JsonResponse(user_list, safe=False)