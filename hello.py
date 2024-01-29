import pandas as pd

file_path = 'C:/Users/karti/OneDrive/Desktop/Personal Projects/NextLevel/mentors.csv'


def format_mentor_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Column names in the CSV file:", df.columns.tolist())

        relevant_columns = ['First Name', 'Last Name', 'Job Title',
                            'If it is okay for students to connect with you on LinkedIn,please provide your LinkedIn profile name (ex\xa0https://www.linkedin.com/in/susan-davis-orourke/)',
                            'Mentor Headshot or photo for marketing purposes', 'Where do you work?']
        df = df[relevant_columns]

        df.columns = ['first_name', 'last_name', 'job_title', 'linkedin', 'photo', 'work']

        formatted_data = []
        for index, row in df.iterrows():
            if pd.isna(row['first_name']) or pd.isna(row['last_name']):
                continue

            photo_filename = row['photo']
            if not isinstance(photo_filename, str):
                photo_filename = "default.jpg"

            entry = {
                'name': f"{row['first_name']} {row['last_name']}",
                'img': f"static/img/mentors/{photo_filename.split('/')[-1]}",
                'dsc': str(row['job_title']) + ", " + str(row['work']),
                'linked': row['linkedin']
            }
            formatted_data.append(entry)

        return formatted_data
    except Exception as e:
        return f"An error occurred: {e}"


mentor_data = format_mentor_data(file_path)
for mentor in mentor_data:
    print(mentor)
