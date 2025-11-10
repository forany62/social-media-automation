"""
Validation Utility
أداة التحقق من صحة البيانات

Validates URLs, file paths, and other inputs
"""

import os
from urllib.parse import urlparse
from pathlib import Path


def validate_url(url):
    """
    Validate URL format
    التحقق من صحة تنسيق الرابط
    
    Args:
        url (str): URL to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def validate_file_path(file_path, check_exists=True):
    """
    Validate file path
    التحقق من صحة مسار الملف
    
    Args:
        file_path (str): Path to validate
        check_exists (bool): Check if file exists
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        path = Path(file_path)
        
        if check_exists:
            return path.exists() and path.is_file()
        else:
            return True
    except:
        return False


def validate_video_file(file_path, max_size_mb=100):
    """
    Validate video file
    التحقق من صحة ملف الفيديو
    
    Args:
        file_path (str): Path to video file
        max_size_mb (int): Maximum file size in MB
    
    Returns:
        dict: Validation result
    """
    if not validate_file_path(file_path):
        return {'valid': False, 'error': 'File not found'}
    
    # Check file extension
    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    path = Path(file_path)
    if path.suffix.lower() not in valid_extensions:
        return {'valid': False, 'error': f'Invalid file extension. Allowed: {valid_extensions}'}
    
    # Check file size
    file_size_mb = path.stat().st_size / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return {'valid': False, 'error': f'File too large ({file_size_mb:.1f}MB). Max: {max_size_mb}MB'}
    
    return {'valid': True, 'size_mb': file_size_mb}


def validate_image_file(file_path, max_size_mb=10):
    """
    Validate image file
    التحقق من صحة ملف الصورة
    
    Args:
        file_path (str): Path to image file
        max_size_mb (int): Maximum file size in MB
    
    Returns:
        dict: Validation result
    """
    if not validate_file_path(file_path):
        return {'valid': False, 'error': 'File not found'}
    
    # Check file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    path = Path(file_path)
    if path.suffix.lower() not in valid_extensions:
        return {'valid': False, 'error': f'Invalid file extension. Allowed: {valid_extensions}'}
    
    # Check file size
    file_size_mb = path.stat().st_size / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return {'valid': False, 'error': f'File too large ({file_size_mb:.1f}MB). Max: {max_size_mb}MB'}
    
    return {'valid': True, 'size_mb': file_size_mb}
