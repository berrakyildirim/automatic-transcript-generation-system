import os
import pandas as pd
import html

# === Paths ===
transcript_dir = "student_transcripts"
html_dir = "html_transcripts"
os.makedirs(html_dir, exist_ok=True)

# === Process each transcript file ===
files = [f for f in os.listdir(transcript_dir) if f.startswith("transcript_") and f.endswith(".csv")] #check file is valid
if not files:
    print("No transcript files found!!!")
    exit()

for file in files:
    path = os.path.join(transcript_dir, file)
    df = pd.read_csv(path) #read path file
    if df.empty:
        print(f"Skipping empty file: {file}")
        continue

    sid = df["student_id"].iloc[0]
    name = html.escape(df["name"].iloc[0])
    surname = html.escape(df["surname"].iloc[0])
    df = df.sort_values("semester")

    #headers
    html_doc = f""" 
    <html><head><style>
    body{{font-family:Arial}} 
    table{{border-collapse:collapse;width:100%}} 
    th,td{{border:1px solid #ccc;padding:6px;text-align:left}}
    </style></head><body>
    <h1>Transcript</h1>
    <h2>Name: {name} {surname}</h2>
    <h2>Student Number: {sid}</h2>
    """

    #iterate for each semester  and create semester table
    for sem in df["semester"].unique():
        sem_df = df[df["semester"] == sem]
        gpa = sem_df["GPA"].iloc[0]
        cgpa = sem_df["CGPA"].iloc[0]
        points = sem_df["weighted_point"].sum()
        credits = sem_df["credit"].sum()

        html_doc += f"<h3>{sem}</h3><table><tr><th>Course Code</th><th>Course Name</th><th>Grade</th><th>Credit</th><th>Grade Point</th></tr>"
        for _, row in sem_df.iterrows():
            html_doc += f"<tr><td>{row['course_code']}</td><td>{html.escape(str(row.get('course_name', '')))}</td><td>{row['grade']}</td><td>{row['credit']}</td><td>{row['grade_point']}</td></tr>"
        html_doc += f"</table><p><strong>Semester Points:</strong> {points:.2f} | <strong>Credits:</strong> {credits:.1f} | <strong>GPA:</strong> {gpa} | <strong>CGPA:</strong> {cgpa}</p>"

    html_doc += "</body></html>"

    output_path = os.path.join(html_dir, f"transcript_{sid}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_doc)

    print(f"** HTML saved: {output_path}")

print(f"\nAll HTML transcripts saved in: {html_dir}")
