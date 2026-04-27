"""Asset tracker for nested list.

This Modul iterates thruth nested list, checks different attributes to display a summary string.
"""


liste = {
    "projekt_1": [{"name": "Angels", "programm": "Blender", "status": "fertig", "polygon_count": 52000}],
    "projekt_2": [{"name": "Drifters", "programm": "Blender", "status": "in arbeit", "polygon_count": 1600}],
    "projekt_3": [{"name": "House", "programm": "Photoshop", "status": "fertig", "polygon_count": 0}]
}
# definiert die Daten in einer Liste

def high_poly(liste):
    """Tracks count of projects with polygon count over 10000.

    Args:
        liste: A list containing project names as keys and a for each project a list of asset details as values.

    Returns:
        An Integer representing the total count of high-poly assets.
    
    """
    high_poly_count = 0
    for high_poly in liste.values():
        for poly_items in high_poly:
            if poly_items["polygon_count"] > 10000:
                high_poly_count += 1
    return high_poly_count

# edit status of two projects
liste ["projekt_3"][0]["status"] = "in arbeit"
liste ["projekt_2"][0]["status"] = "fertig"


blender_list = [
      item['name']
      for items in liste.values()
      for item in items
      if item['status'] == "fertig" and item['programm'] != "Photoshop"
]


project_count = len(liste)


def in_progress(liste):
    """Tracks count of projects that are currently in progress.
    
    Args:
        liste: A list containing project names as keys and a for each project a list of asset details as values.

    Returns:
        An Integer representing the total count of assets with the status 'in arbeit'.
    """
    assets_in_progress = 0
    for items in liste.values():
        for item in items:
            if item['status'] == "in arbeit":
                assets_in_progress += 1
    return(assets_in_progress)

assets_in_progress = in_progress(liste)

high_polygon_count = sum(
    1
    for items in liste.values()
    for item in items
    if item.get("polygon_count", 0) > 10000
)

report = ""
progress_report = assets_in_progress
high_poly_report = high_polygon_count
all_projects_reprot = project_count
blender_report = len(blender_list)

print(f"Insgesamt sind {all_projects_reprot} Projekte geladen.\n{progress_report} Projekte sind noch in arbeit.\n{high_poly_report} Projekte sind High-Poly Objekte.\nInsgesamt sind {blender_report} von {all_projects_reprot} Projekte Blender Daten.")