"""history.py - /api/history"""
from flask import Blueprint, jsonify

from database import delete_record, list_records

bp = Blueprint("history", __name__)


@bp.get("/api/history")
def history():
    return jsonify(success=True, records=list_records())


@bp.delete("/api/history/<int:record_id>")
def remove(record_id):
    if not delete_record(record_id):
        return jsonify(success=False, error="Record not found."), 404
    return jsonify(success=True, deleted=record_id)
