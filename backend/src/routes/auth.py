from flask import Blueprint, jsonify, request, current_app
from src.models.user import User, db
import jwt
from datetime import datetime, timedelta
from functools import wraps
import secrets

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Token format invalid'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['user_id']).first()
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def generate_tokens(user_id):
    """Genera access token y refresh token para un usuario"""
    # Access token con duración corta (1 hora)
    access_token = jwt.encode({
        'user_id': user_id,
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    # Refresh token con duración larga (30 días)
    refresh_token = jwt.encode({
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(days=30),
        'jti': secrets.token_hex(16)  # Unique identifier
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    return access_token, refresh_token

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password') or not data.get('email'):
            return jsonify({'message': 'Username, email and password are required'}), 400
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
        
        # Crear nuevo usuario
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User created successfully', 'user': user.to_dict()}), 201
    
    except Exception as e:
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Username and password are required'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            # Generar tokens
            access_token, refresh_token = generate_tokens(user.id)
            
            # Guardar el refresh token en el usuario (opcional, para invalidación)
            user.refresh_token = refresh_token
            db.session.commit()
            
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }), 200
        
        return jsonify({'message': 'Invalid credentials'}), 401
    
    except Exception as e:
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    try:
        data = request.get_json()
        
        if not data or not data.get('refresh_token'):
            return jsonify({'message': 'Refresh token is required'}), 400
        
        refresh_token = data['refresh_token']
        
        try:
            # Verificar el refresh token
            payload = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            
            if payload.get('type') != 'refresh':
                return jsonify({'message': 'Invalid token type'}), 401
            
            user_id = payload['user_id']
            user = User.query.filter_by(id=user_id).first()
            
            if not user:
                return jsonify({'message': 'User not found'}), 401
            
            # Verificar que el refresh token coincida con el almacenado (opcional)
            if hasattr(user, 'refresh_token') and user.refresh_token != refresh_token:
                return jsonify({'message': 'Invalid refresh token'}), 401
            
            # Generar nuevos tokens
            new_access_token, new_refresh_token = generate_tokens(user_id)
            
            # Actualizar el refresh token almacenado
            user.refresh_token = new_refresh_token
            db.session.commit()
            
            return jsonify({
                'access_token': new_access_token,
                'refresh_token': new_refresh_token,
                'user': user.to_dict()
            }), 200
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Refresh token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid refresh token'}), 401
    
    except Exception as e:
        return jsonify({'message': 'Token refresh failed', 'error': str(e)}), 500

@auth_bp.route('/verify', methods=['GET'])
@token_required
def verify_token(current_user):
    return jsonify({
        'message': 'Token is valid',
        'user': current_user.to_dict()
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    try:
        # Invalidar el refresh token
        current_user.refresh_token = None
        db.session.commit()
        
        return jsonify({'message': 'Logout successful'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Logout failed', 'error': str(e)}), 500

