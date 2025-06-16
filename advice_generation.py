def generate_daily_advice(numerology_insights: dict, astrology_influences: dict) -> list:
    advice_items = []
    actions_to_do = set()
    actions_to_avoid = set()

    # Safely extract personal day number
    raw_pd = numerology_insights.get("personal_day")
    try:
        pd = int(str(raw_pd).split()[0])  # Supports formats like "1", "1 (Leadership)", etc.
    except (ValueError, TypeError):
        pd = None

    # --- Numerology-based recommendations ---
    if pd == 1:
        actions_to_do.add("Start new projects.")
    elif pd == 2:
        actions_to_do.add("Cooperate and listen actively.")
    elif pd == 3:
        actions_to_do.add("Express yourself creatively.")
    elif pd == 4:
        actions_to_do.add("Focus on practical and organized tasks.")
    elif pd == 5:
        actions_to_do.add("Embrace flexibility and adapt to change.")
    elif pd == 6:
        actions_to_do.add("Attend to responsibilities at home or work.")
    elif pd == 7:
        actions_to_do.add("Reflect, research, and spend time in solitude.")
    elif pd == 8:
        actions_to_do.add("Make bold business or financial decisions.")
    elif pd == 9:
        actions_to_do.add("Let go of what no longer serves you.")

    # --- Astrology-based recommendations ---
    if astrology_influences.get("mercury_retrograde", False):
        actions_to_avoid.add("Sign contracts or make irreversible decisions without review.")
        actions_to_do.add("Review, revise, and reconnect with the past.")

    transit_category = astrology_influences.get("key_transit_category")
    if transit_category == "Harmonious":
        actions_to_do.add("Leverage positive energies; things may flow easily.")
    elif transit_category == "Challenging":
        actions_to_avoid.add("Force confrontations or push aggressively.")
        actions_to_do.add("Handle obstacles with patience and resilience.")

    moon_sign = astrology_influences.get("transiting_moon_sign", "")
    fire_signs = {"Aries", "Leo", "Sagittarius"}
    earth_signs = {"Taurus", "Virgo", "Capricorn"}
    air_signs = {"Gemini", "Libra", "Aquarius"}
    water_signs = {"Cancer", "Scorpio", "Pisces"}

    if moon_sign in fire_signs:
        actions_to_do.add("Act boldly and pursue inspiration.")
    elif moon_sign in earth_signs:
        actions_to_do.add("Ground yourself and handle practical matters.")
    elif moon_sign in air_signs:
        actions_to_do.add("Communicate, network, and exchange ideas.")
    elif moon_sign in water_signs:
        actions_to_do.add("Listen to emotions and nurture relationships.")

    # --- Combined day-astrology synergies ---
    if pd == 1 and transit_category == "Harmonious":
        advice_items.append("⚡ POWER DAY: Excellent energy to launch new initiatives with confidence!")

    # --- Consolidated output ---
    if actions_to_do:
        advice_items.append("✅ Consider DOING: " + "; ".join(sorted(actions_to_do)))
    if actions_to_avoid:
        advice_items.append("⚠️ Consider AVOIDING: " + "; ".join(sorted(actions_to_avoid)))

    if not advice_items:
        advice_items.append("A general day. Trust your intuition and stay centered.")

    return advice_items
