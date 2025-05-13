from app import application
from .models import db, User, Unit, DiaryEntry, Faculty

def get_avg_rating_for_unit(unit_id):
    """
    Get the average rating for a unit.
    """
    entries = db.session.query(DiaryEntry).filter(DiaryEntry.unit_id == unit_id).all()
    if not entries:
        return None
    total_rating = sum(entry.overall_rating for entry in entries)
    avg_rating = total_rating / len(entries)
    return avg_rating

def get_optional_comments_for_unit(unit_id):
    """
    Get all comments for a unit.
    """
    entries = db.session.query(DiaryEntry).filter(DiaryEntry.unit_id == unit_id).all()
    commmented_reviews=[]
    if entries is None:
        return commented_reviews

    for entry in entries:
        if entry.optional_comments:
            commmented_reviews.append(entry)
            print(entry.optional_comments.strip())
    return commmented_reviews

def avg_rating_for_unit_coord(unit_id):
    """
    Get the average rating for a unit coordinator.
    """
    entries = db.session.query(DiaryEntry).filter(DiaryEntry.unit_id == unit_id).all()
    if not entries:
        return None
    total_rating = sum(entry.coordinator_rating for entry in entries)
    avg_rating = total_rating / len(entries)
    return avg_rating

def get_difficulty_rating_avg_for_unit(unit_id):
    """
    Get the average difficulty rating for a unit.
    """
    entries = db.session.query(DiaryEntry).filter(DiaryEntry.unit_id == unit_id).all()
    if not entries:
        return None
    total_rating = sum(entry.difficulty_rating for entry in entries)
    avg_rating = total_rating / len(entries)
    return avg_rating

def get_overall_rating_count_for_unit(unit_id):
    """
    Get the count of overall ratings for a unit.
    """
    entries = db.session.query(DiaryEntry).filter(DiaryEntry.unit_id == unit_id).all()
    if not entries:
        return {"Amazing": 0, "Great": 0, "Okay": 0, "Bad": 0, "Poor": 0}
    review_ratings = {"Amazing": 0, "Great": 0, "Okay": 0, "Bad": 0, "Poor": 0}
    for entry in entries:
        if entry.overall_rating == 5:
            review_ratings["Amazing"] += 1
        elif entry.overall_rating == 4:
            review_ratings["Great"] += 1
        elif entry.overall_rating == 3:
            review_ratings["Okay"] += 1
        elif entry.overall_rating == 2:
            review_ratings["Bad"] += 1
        elif entry.overall_rating == 1:
            review_ratings["Poor"] += 1
    return review_ratings

def get_workload_avg_for_unit(unit_id):
    """
    Get the average workload for a unit.
    """
    entries = db.session.query(DiaryEntry).filter(DiaryEntry.unit_id == unit_id).all()
    if not entries:
        return None
    total_workload = sum(entry.workload_hours_per_week for entry in entries)
    avg_workload = total_workload / len(entries)
    return avg_workload

def get_assessment_breakdown_for_unit(unit_id):
    """
    Get the assessment breakdown for a unit.
    """
    entries = db.session.query(DiaryEntry).filter(DiaryEntry.unit_id == unit_id).all()
    if not entries:
        return None
    assessment_breakdown = {}
    for entry in entries:
        assessments = entry.assessment_breakdowns
        for assessment in assessments:
            if assessment.type not in assessment_breakdown:
                assessment_breakdown[assessment.type] = 0
            assessment_breakdown[assessment.type] += assessment.percentage
    return assessment_breakdown