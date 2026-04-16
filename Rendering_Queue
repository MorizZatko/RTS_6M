"""
Module: Rendering Queue Calculator
Description: This tool calculates the needed rendering time for three projects by the count of the frames and the time per frame.
Function:
    1. The three given projects are located in a nested list with name, frames and time per frame.
    2. Every project gets calculatet as a float and gets divided by 60 for output in minutes.
    3. Initialize new list with all calculate results.
    4. Extracting the project with the longest rendering time.

Args:
    None: All inputs are provided by the nested list 'jobs'
Returns:
    None: Outputs a string with every project and the rendering time in minutes, and outputs a string for the longest rendering project.
"""

jobs = [
    ["Charakter_Animation", 120, 15.5],  
    ["Background_Static", 450, 1.2],
    ["Water_Simulation", 80, 45.0]
]

job_1 = float(jobs[0][1] * jobs[0][2]) / 60     
job_2 = float(jobs[1][1] * jobs[1][2]) / 60
job_3 = float(jobs[2][1] * jobs[2][2]) / 60

# --- Output ---
time = [job_1, job_2, job_3]   
max_time = max(time)    

print(f"Render Dauer in Minuten:\nProjekt_1: {job_1}\nProjekt_2: {job_2}\nProjekt_3: {job_3}") 
print(f"Das längste Projekt dauert: {max_time} min.") 
