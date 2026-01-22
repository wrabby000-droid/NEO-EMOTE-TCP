"""
API Server for Emote System
This file handles the API endpoints that the frontend calls
Can work as standalone or proxy to backend server at 92.118.206.166:30300
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://92.118.206.166:30300')
USE_PROXY = os.getenv('USE_PROXY', 'true').lower() == 'true'

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Backend URL: {BACKEND_URL}")
logger.info(f"Proxy Mode: {'Enabled' if USE_PROXY else 'Disabled'}")

@app.route('/api/fastemote', methods=['GET'])
def fastemote():
    """
    Fast Emote API endpoint
    Parameters: tc (teamcode), uid1, uid2, uid3, uid4, emote_id
    """
    try:
        # If proxy mode is enabled, forward to backend server
        if USE_PROXY:
            backend_url = f"{BACKEND_URL}/fastemote"
            params = request.args.to_dict()
            
            logger.info(f"Proxying FastEmote to {backend_url} with params: {params}")
            
            try:
                response = requests.get(backend_url, params=params, timeout=30)
                return response.json(), response.status_code
            except requests.exceptions.RequestException as e:
                logger.error(f"Backend proxy error: {str(e)}")
                return jsonify({'status': 'error', 'message': f'Backend server error: {str(e)}'}), 502
        
        # Standalone mode - handle locally
        teamcode = request.args.get('tc', '')
        uid1 = request.args.get('uid1', '')
        uid2 = request.args.get('uid2', '')
        uid3 = request.args.get('uid3', '')
        uid4 = request.args.get('uid4', '')
        emote_id = request.args.get('emote_id', '')
        
        # Validation
        if not teamcode:
            return jsonify({'status': 'error', 'message': 'Team code is required'}), 400
        
        if not emote_id:
            return jsonify({'status': 'error', 'message': 'Emote ID is required'}), 400
        
        # Get all valid UIDs
        uids = [uid for uid in [uid1, uid2, uid3, uid4] if uid]
        
        if not uids:
            return jsonify({'status': 'error', 'message': 'At least one UID is required'}), 400
        
        logger.info(f"FastEmote request: TC={teamcode}, EmoteID={emote_id}, UIDs={uids}")
        
        # TODO: Add your actual emote sending logic here
        # For now, return success response
        
        return jsonify({
            'status': 'success',
            'message': f'Fast emote {emote_id} sent to {len(uids)} player(s)',
            'data': {
                'teamcode': teamcode,
                'emote_id': emote_id,
                'uids': uids
            }
        }), 200
        
    except Exception as e:
        logger.error(f"FastEmote error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/join', methods=['GET'])
def join_emote():
    """
    Join Emote API endpoint
    Parameters: tc (teamcode), emote_id, uid1, uid2, uid3, uid4
    """
    try:
        # If proxy mode is enabled, forward to backend server
        if USE_PROXY:
            backend_url = f"{BACKEND_URL}/join"
            params = request.args.to_dict()
            
            logger.info(f"Proxying JoinEmote to {backend_url} with params: {params}")
            
            try:
                response = requests.get(backend_url, params=params, timeout=30)
                return response.json(), response.status_code
            except requests.exceptions.RequestException as e:
                logger.error(f"Backend proxy error: {str(e)}")
                return jsonify({'status': 'error', 'message': f'Backend server error: {str(e)}'}), 502
        
        # Standalone mode - handle locally
        teamcode = request.args.get('tc', '')
        emote_id = request.args.get('emote_id', '')
        uid1 = request.args.get('uid1', '')
        uid2 = request.args.get('uid2', '')
        uid3 = request.args.get('uid3', '')
        uid4 = request.args.get('uid4', '')
        
        # Validation
        if not teamcode:
            return jsonify({'status': 'error', 'message': 'Team code is required'}), 400
        
        if not emote_id:
            return jsonify({'status': 'error', 'message': 'Emote ID is required'}), 400
        
        # Get all valid UIDs
        uids = [uid for uid in [uid1, uid2, uid3, uid4] if uid]
        
        if not uids:
            return jsonify({'status': 'error', 'message': 'At least one UID is required'}), 400
        
        logger.info(f"JoinEmote request: TC={teamcode}, EmoteID={emote_id}, UIDs={uids}")
        
        # TODO: Add your actual join emote logic here
        # For now, return success response
        
        return jsonify({
            'status': 'success',
            'message': f'Join emote {emote_id} sent to {len(uids)} player(s)',
            'data': {
                'teamcode': teamcode,
                'emote_id': emote_id,
                'uids': uids
            }
        }), 200
        
    except Exception as e:
        logger.error(f"JoinEmote error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/join-send-leave', methods=['GET'])
def join_send_leave():
    """
    Join-Send-Leave workflow endpoint
    Bot joins team -> sends emote -> leaves team
    Parameters: tc (teamcode), uid (target UID), emote_id
    """
    try:
        # If proxy mode is enabled, forward to backend server
        if USE_PROXY:
            backend_url = f"{BACKEND_URL}/join-send-leave"
            params = request.args.to_dict()
            
            logger.info(f"Proxying Join-Send-Leave to {backend_url} with params: {params}")
            
            try:
                response = requests.get(backend_url, params=params, timeout=45)  # Longer timeout for 3-step process
                return response.json(), response.status_code
            except requests.exceptions.RequestException as e:
                logger.error(f"Backend proxy error: {str(e)}")
                return jsonify({'status': 'error', 'message': f'Backend server error: {str(e)}'}), 502
        
        # Standalone mode - handle locally
        teamcode = request.args.get('tc', '')
        uid = request.args.get('uid', '')
        emote_id = request.args.get('emote_id', '')
        
        # Validation
        if not teamcode:
            return jsonify({'status': 'error', 'message': 'Team code is required'}), 400
        
        if not uid:
            return jsonify({'status': 'error', 'message': 'UID is required'}), 400
        
        if not emote_id:
            return jsonify({'status': 'error', 'message': 'Emote ID is required'}), 400
        
        logger.info(f"Join-Send-Leave request: TC={teamcode}, EmoteID={emote_id}, UID={uid}")
        
        # TODO: Add your actual join-send-leave logic here
        # For now, return success response
        
        return jsonify({
            'status': 'success',
            'message': f'Bot joined team, sent emote {emote_id} to UID {uid}, then left',
            'data': {
                'teamcode': teamcode,
                'emote_id': emote_id,
                'uid': uid,
                'steps': ['joined', 'sent', 'left']
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Join-Send-Leave error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API server is running'}), 200


@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Emote API Server',
        'endpoints': {
            '/api/fastemote': 'Fast emote endpoint',
            '/api/join': 'Join emote endpoint',
            '/api/join-send-leave': 'Join team, send emote, leave team',
            '/health': 'Health check'
        }
    }), 200


if __name__ == '__main__':
    # For development
    app.run(host='0.0.0.0', port=5000, debug=True)
