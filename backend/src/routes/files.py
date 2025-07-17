from flask import Blueprint, jsonify, request, send_file, current_app
from werkzeug.utils import secure_filename
from src.models.file import File, db
from src.routes.auth import token_required
import os
import uuid
from datetime import datetime

files_bp = Blueprint('files', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', 'mp3', 'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_folder():
    upload_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), UPLOAD_FOLDER)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    return upload_path

@files_bp.route('/upload', methods=['POST'])
@token_required
def upload_file(current_user):
    try:
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400
        
        file = request.files['file']
        folder_path = request.form.get('folder_path', '/')
        
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            # Generar nombre único para el archivo
            original_filename = secure_filename(file.filename)
            file_extension = original_filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
            
            # Asegurar que el directorio de subida existe
            upload_path = ensure_upload_folder()
            
            # Crear subdirectorio para el usuario
            user_folder = os.path.join(upload_path, str(current_user.id))
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            
            # Guardar archivo
            file_path = os.path.join(user_folder, unique_filename)
            file.save(file_path)
            
            # Obtener información del archivo
            file_size = os.path.getsize(file_path)
            
            # Guardar metadatos en la base de datos
            file_record = File(
                filename=unique_filename,
                original_filename=original_filename,
                file_path=file_path,
                file_size=file_size,
                mime_type=file.content_type or 'application/octet-stream',
                user_id=current_user.id,
                folder_path=folder_path
            )
            
            db.session.add(file_record)
            db.session.commit()
            
            return jsonify({
                'message': 'File uploaded successfully',
                'file': file_record.to_dict()
            }), 201
        
        return jsonify({'message': 'File type not allowed'}), 400
    
    except Exception as e:
        return jsonify({'message': 'Upload failed', 'error': str(e)}), 500

@files_bp.route('/files', methods=['GET'])
@token_required
def get_files(current_user):
    try:
        folder_path = request.args.get('folder_path', '/')
        files = File.query.filter_by(user_id=current_user.id, folder_path=folder_path).all()
        
        return jsonify({
            'files': [file.to_dict() for file in files],
            'folder_path': folder_path
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get files', 'error': str(e)}), 500

@files_bp.route('/files/<int:file_id>', methods=['GET'])
@token_required
def download_file(current_user, file_id):
    try:
        file_record = File.query.filter_by(id=file_id, user_id=current_user.id).first()
        
        if not file_record:
            return jsonify({'message': 'File not found'}), 404
        
        if not os.path.exists(file_record.file_path):
            return jsonify({'message': 'File not found on disk'}), 404
        
        return send_file(
            file_record.file_path,
            as_attachment=True,
            download_name=file_record.original_filename
        )
    
    except Exception as e:
        return jsonify({'message': 'Download failed', 'error': str(e)}), 500

@files_bp.route('/files/<int:file_id>', methods=['DELETE'])
@token_required
def delete_file(current_user, file_id):
    try:
        file_record = File.query.filter_by(id=file_id, user_id=current_user.id).first()
        
        if not file_record:
            return jsonify({'message': 'File not found'}), 404
        
        # Eliminar archivo del disco
        if os.path.exists(file_record.file_path):
            os.remove(file_record.file_path)
        
        # Eliminar registro de la base de datos
        db.session.delete(file_record)
        db.session.commit()
        
        return jsonify({'message': 'File deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Delete failed', 'error': str(e)}), 500

@files_bp.route('/files/<int:file_id>/rename', methods=['PUT'])
@token_required
def rename_file(current_user, file_id):
    try:
        data = request.get_json()
        new_name = data.get('new_name')
        
        if not new_name:
            return jsonify({'message': 'New name is required'}), 400
        
        file_record = File.query.filter_by(id=file_id, user_id=current_user.id).first()
        
        if not file_record:
            return jsonify({'message': 'File not found'}), 404
        
        # Actualizar nombre original
        file_record.original_filename = secure_filename(new_name)
        db.session.commit()
        
        return jsonify({
            'message': 'File renamed successfully',
            'file': file_record.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Rename failed', 'error': str(e)}), 500

