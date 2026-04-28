"""Rendering Queue Calculator.

This tool calculates the needed rendering time for three projects by the count of the frames and the time per frame.
All three projects are provided by a static hardcoded list in this module.
Output rendering time in minutes per project and the needed time for the project with longest rendering time.
"""

# Hardcoded list provides project data
jobs = [
    ["Charakter_Animation", 120, 15.5],  
    ["Background_Static", 450, 1.2],
    ["Water_Simulation", 80, 45.0]
]

# Calculate time for each project
job_1 = float(jobs[0][1] * jobs[0][2]) / 60     
job_2 = float(jobs[1][1] * jobs[1][2]) / 60
job_3 = float(jobs[2][1] * jobs[2][2]) / 60

# Generates time list with results of all projects
time = [job_1, job_2, job_3]   

# Extracts longest rendering time
max_time = max(time)    

# Outputs results via standard output
print(f"Render Dauer in Minuten:\nProjekt_1: {job_1}\nProjekt_2: {job_2}\nProjekt_3: {job_3}") 
print(f"Das längste Projekt dauert: {max_time} min.") 