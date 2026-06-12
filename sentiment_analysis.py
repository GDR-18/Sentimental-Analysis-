from nltk.sentiment import SentimentIntensityAnalyzer
from wordfreq import zipf_frequency

sia = SentimentIntensityAnalyzer()

# ======================================================
# POSITIVE WORDS
# ======================================================

employee_positive = {
    "guidance","helps","supports","knowledge","experienced","valuable","creative","organized",
    "experienced","expert","skilled","knowledgeable",
    "dedicated","innovative","creative","responsive",
    "approachable","understanding","inspiring",
    "talented","organized","valuable","reliable",
    "promotion", "bonus", "growth", "learning",
    "supportive", "flexible", "opportunity",
    "appreciation", "reward", "friendly",
    "excellent", "great", "good", "helpful",
    "motivating", "encouraging", "respectful",
    "cooperative", "professional", "happy",
    "guidance", "mentor", "mentoring",
    "knowledgeable", "support", "improve",
    "collaborative", "productive", "efficient",
    "successful", "achievement", "recognition"
}

# ======================================================
# NEGATIVE WORDS
# ======================================================

employee_negative = {
    "pressure","stressed","stressful","burden","strict","stress","toxic","underpaid","overtime","micromanagement",
    "pressure","burnout","unfair","poor","workload","bad","worst","rude","harassment",
    "frustrating","difficult","negative","slow","delay","delayed","confusing","confusion",
    "inefficient","useless","waste","wastes","wrong","mistake","mistakes","problem","problems",
    "issue","issues","lack","unskilled","inexperienced","poorly","failed","failure",
    "wasting","unresponsive","ignorant","incompetent","disorganized","careless","unprofessional","arrogant","biased",
    "overloaded","overworked","demotivating","discouraging"
}

# ======================================================
# POSITIVE PHRASES
# ======================================================

positive_phrases = [
    "helps me",
    "supports me",
    "good management",
    "excellent leadership",
    "great learning",
    "career growth",
    "friendly environment",
    "helpful supervisor",
    "supportive manager",
    "good mentor",
    "excellent guidance",
    "encourages learning",
    "helps in projects",
    "good work culture","highly knowledgeable",
    "excellent mentor",
    "good decision making",
    "strong leadership",
    "very supportive",
    "great manager",
    "excellent supervisor",
    "quick problem solving",
    "good communication"
]

# ======================================================
# NEGATIVE PHRASES
# ======================================================

negative_phrases = [
    "high workload","heavy workload","workload is high","workload is very high",
    "wastes my time",
    "waste my time",
    "does not work",
    "doesn't work",
    "not working",
    "lack of knowledge",
    "no technical knowledge",
    "poor management",
    "bad management",
    "poor guidance",
    "poor leadership",
    "unhelpful manager",
    "unskilled supervisor",
    "inefficient process",
    "high workload",
    "too much pressure",
    "very stressful",
    "toxic environment",
    "poor communication",
    "does not help",
    "not supportive",
    "lack of experience","wastes time",
    "not knowledgeable",
    "does not understand",
    "poor decisions",
    "bad decisions",
    "poor technical skills",
    "wrong recommendations",
    "lack of technical knowledge",
    "unnecessary delays",
    "does not listen",
    "not effective"
]


def is_real_word(word):
    
    word = word.lower().strip()

    if len(word) <= 1:
        return False

    if word.isdigit():
        return False

    return zipf_frequency(word, "en") > 1


# ======================================================
# SUMMARY
# ======================================================

def generate_summary(review):

    review = review.lower()
    topics = []

    if any(word in review for word in
           ["manager", "management", "boss", "hod", "supervisor"]):
        topics.append("Management")

    if any(word in review for word in
           ["salary", "pay", "bonus", "underpaid"]):
        topics.append("Compensation")

    if any(word in review for word in
           ["team", "colleague", "coworker", "employees"]):
        topics.append("Teamwork")

    if any(word in review for word in
           ["project", "training", "learning", "skill"]):
        topics.append("Growth & Development")

    if any(word in review for word in
           ["culture", "environment", "office"]):
        topics.append("Work Culture")

    if any(word in review for word in
           ["academic", "academics", "faculty"]):
        topics.append("Academics")

    if not topics:
        return "General Employee Feedback"

    return ", ".join(topics)


# ======================================================
# SUGGESTIONS
# ======================================================

def generate_suggestions(review):

    review = review.lower()
    suggestions = []

    if "strict" in review:
        suggestions.append(
            "Balance discipline with constructive guidance."
        )

    if any(x in review for x in
           ["stress", "pressure", "burnout"]):
        suggestions.append(
            "Reduce workload pressure and improve employee well-being."
        )

    if any(x in review for x in
           ["salary", "underpaid", "pay"]):
        suggestions.append(
            "Review compensation policies and employee benefits."
        )

    if "toxic" in review:
        suggestions.append(
            "Promote a healthier workplace culture."
        )

    if any(x in review for x in
           ["manager", "boss", "hod", "supervisor"]):
        suggestions.append(
            "Improve leadership communication and mentoring."
        )

    if any(x in review for x in
           ["project", "learning", "training"]):
        suggestions.append(
            "Continue supporting employee growth and skill development."
        )

    if any(x in review for x in
           ["waste", "delay", "inefficient"]):
        suggestions.append(
            "Improve decision-making efficiency and project planning."
        )

    if "technical knowledge" in review:
        suggestions.append(
            "Provide additional technical training for supervisors."
        )

    if "does not work" in review:
        suggestions.append(
            "Validate solutions before recommending them to employees."
        )

    if not suggestions:
        suggestions.append(
            "Continue maintaining a productive work environment."
        )

    return suggestions


# ======================================================
# MAIN SENTIMENT FUNCTION
# ======================================================

def analyze_sentiment(review):

    review = str(review).lower().strip()

    if review == "":
        return {
        "rating": None,
        "category": "Invalid Input",
        "summary": "No review provided",
        "suggestions": [
            "Please enter an employee review."
        ]
    }

    words = review.split()

    real_word_count = sum(
        1 for word in words
        if is_real_word(word)
    )
    if len(words) > 0:
        real_ratio = real_word_count / len(words)
    else:
        real_ratio = 0

    if real_ratio < 0.30:

        return {
            "rating": None,
            "category": "Invalid Input",
            "summary": "Input contains mostly meaningless words",
            "suggestions": [
                "Please enter a meaningful employee review."
            ]
        }

    if real_word_count == 0:
        return {
        "rating": None,
        "category": "Invalid Input",
        "summary": "Input contains no meaningful words",
        "suggestions": [
            "Please enter a valid employee review."
        ]
    }

    vader_score = sia.polarity_scores(review)["compound"]

    custom_score = 0

    # Word matching
    for word in words:

        word = word.strip(".,!?()[]{}")

        if word in employee_positive:
            custom_score += 1.0

        elif word in employee_negative:
            custom_score -= 1.0

    # Phrase matching
    for phrase in positive_phrases:
        if phrase in review:
            custom_score += 0.75

    for phrase in negative_phrases:
        if phrase in review:
            custom_score -= 0.5

    # Handle BUT
    if " but " in review:

        parts = review.split(" but ")

        if len(parts) > 1:

            after_but = sia.polarity_scores(
                parts[-1]
            )["compound"]
            
            before_but = sia.polarity_scores(parts[0])["compound"]

            vader_score = (
                vader_score * 0.3 +
                after_but * 0.7
            )

    # Handle HOWEVER
    if " however " in review:

        parts = review.split(" however ")

        if len(parts) > 1:

            after_part = sia.polarity_scores(
                parts[-1]
            )["compound"]

            vader_score = (
                vader_score * 0.3 +
                after_part * 0.7
            )

    final_score = vader_score + (custom_score * 0.10)
    
    if "strict" in review and "help" in review:
        final_score -= 0.15

    if "pressure" in review:
        final_score -= 0.20
        
    positive_count = sum(
        1 for word in words
        if word.strip(".,!?()[]{}") in employee_positive
    )

    negative_count = sum(
        1 for word in words
        if word.strip(".,!?()[]{}") in employee_negative
    )

    if positive_count >= 1 and negative_count >= 1:
        final_score = final_score * 0.5

    final_score = max(-1, min(1, final_score))

    # ==================================================
    # RATING
    # ==================================================

    if final_score >= 0.75:
        rating = 1
        category = "Strong Positive"

    elif final_score >= 0.45:
        rating = 2
        category = "Strong Positive"

    elif final_score >= 0.20:
        rating = 3
        category = "Mild Positive"

    elif final_score >= 0.05:
        rating = 4
        category = "Mild Positive"

    elif final_score > -0.10:
        rating = 5
        category = "Mixed / Neutral"

    elif final_score > -0.20:
        rating = 6
        category = "Mild Negative"

    elif final_score > -0.45:
        rating = 7
        category = "Mild Negative"

    elif final_score > -0.75:
        rating = 8
        category = "Strong Negative"

    elif final_score > -0.90:
        rating = 9
        category = "Strong Negative"

    else:
        rating = 10
        category = "Strong Negative"

    return {
        "rating": rating,
        "category": category,
        "summary": generate_summary(review),
        "suggestions": generate_suggestions(review)
    }