"""statistics.py - /api/statistics"""
from flask import Blueprint, jsonify

from database import get_statistics

bp = Blueprint("statistics", __name__)


@bp.get("/api/statistics")
def statistics():
    return jsonify(success=True, **get_statistics())
