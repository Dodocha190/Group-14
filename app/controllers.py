from .models import User, Unit, DiaryEntry, Faculty
from app import db
from sqlalchemy import func

def get_avg_rating_for_unit(unit_id):
    """
    Get the average rating for a unit.
    """
    entries = db.session.query(DiaryEntry).filter(DiaryEntry.unit_id == unit_id).all()
    if not entries:
        return None
    total_rating = sum(entry.overall_rating for entry in entries)
    avg_rating = total_rating / len(entries)
    return avg_rating.__round__(2)

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
    return avg_rating.__round__(2)

def get_difficulty_rating_avg_for_unit(unit_id):
    """
    Get the average difficulty rating for a unit.
    """
    entries = db.session.query(DiaryEntry).filter(DiaryEntry.unit_id == unit_id).all()
    if not entries:
        return None
    total_rating = sum(entry.difficulty_rating for entry in entries)
    avg_rating = total_rating / len(entries)
    return avg_rating.__round__(2)

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
    return avg_workload.__round__(2)

def get_assessment_types_for_unit(unit_id):
    """
    Get the assessment types for a unit.
    """
    assessment_types = db.session.query(Unit).filter(Unit.id==unit_id).first()
    assessment_selected = assessment_types.assessment_types
    if not assessment_types:
        return None
    return assessment_selected

def get_diary_entries_from_user(user_id):
    """
    Fetches all diary entries associated with a given user id, including their units.
    """ 
    query = db.session.query(DiaryEntry, Unit).join(Unit, DiaryEntry.unit_id == Unit.id).order_by(DiaryEntry.year.desc(), DiaryEntry.semester.desc())
    results = query.filter(DiaryEntry.user_id == user_id).all()
    return results

def get_total_units_logged(user_id):
    """
    Retrieves the total number of units logged by a specific user.

    Args:
        user_id: The id of the user.

    Returns:
        The total count of units logged by the user.
    """
    entries = db.session.query(DiaryEntry).filter(DiaryEntry.user_id == user_id).all()
    return len(entries)

def get_highest_wam_faculty(user_id):
    """
    Retrieves the faculty with the highest average grade (WAM) for a specific user.

    Args:
        user_id: The id of the user.

    Returns:
        A tuple containing the faculty name and the average grade,
        or None if no diary entries are found for the user.
    """ 
    highest_wam_area_data = db.session.query(Unit.faculty_id, func.avg(DiaryEntry.grade)).join(Unit, DiaryEntry.unit_id == Unit.id).filter(DiaryEntry.user_id == user_id).group_by(Unit.faculty_id).order_by(func.avg(DiaryEntry.grade).desc()).first()
    if not highest_wam_area_data:
        return "No data available"
    return f"{highest_wam_area_data[0]}: Average grade of {highest_wam_area_data[1]}%"

def get_percentage_by_faculty(user_id):
    """
    Retrieves the percentage of units logged by a specific user for each faculty.

    Args:
        user_id: The id of the user.

    Returns:
        A list of tuples, where each tuple contains the faculty name and the
        percentage of units logged in that faculty.
    """
    total_units_logged = get_total_units_logged(user_id)
    if total_units_logged == 0:
        return []
    percentage_by_fac= db.session.query(Unit.faculty_id, (100*func.count(Unit.id)/total_units_logged)).join(DiaryEntry, DiaryEntry.unit_id == Unit.id).filter(DiaryEntry.user_id == user_id).group_by(Unit.faculty_id).all()
    json_friendly_data = [{"faculty": item[0], "percentage": float(item[1])} for item in percentage_by_fac]
    return json_friendly_data


def get_total_credits_passed(user_id):
    """
    Retrieves the total credits for units passed (grade >= 50) by a specific user.
    Assuming each unit is worth 6 credits.

    Args:
        user_id: The id of the user.

    Returns:
        The total credits for passed units.
    """
    passed_entries = db.session.query(DiaryEntry).filter(DiaryEntry.user_id == user_id, DiaryEntry.grade >= 50).all()
    return len(passed_entries) * 6

def get_average_difficulty(user_id):
    """
    Retrieves the average difficulty rating for a specific user.

    Args:
        user_id: The id of the user.

    Returns:
        The average difficulty rating, or None if no diary entries are found.
    """
    entries = db.session.query(DiaryEntry).filter(DiaryEntry.user_id == user_id).all()
    if not entries:
        return None
    total_difficulty = sum(entry.difficulty_rating for entry in entries)
    avg_difficulty = total_difficulty / len(entries)
    return avg_difficulty.__round__(2)

def get_review_card_data_for_unit(unit_id):
    """
    Return a list of dictionaries with review card data (optional_comments, overall_rating, semester, year)
    for a specific unit.
    """
    results = db.session.query(
        DiaryEntry.optional_comments,
        DiaryEntry.overall_rating,
        DiaryEntry.semester,
        DiaryEntry.year
    ).filter(
        DiaryEntry.unit_id == unit_id,
        DiaryEntry.optional_comments != None,
        DiaryEntry.optional_comments != ''
    ).all()
    if not results:
        return []
    return [
        {
            'optional_comments': r.optional_comments,
            'overall_rating': r.overall_rating,
            'semester': r.semester,
            'year': r.year
        }
        for r in results
    ]