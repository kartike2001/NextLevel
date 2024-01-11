import os
import shutil

project_root = 'C:\\USERS\\KARTI\\ONEDRIVE\\DESKTOP\\PERSONAL PROJECTS\\NEXTLEVEL'


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")


def move_file(src, dst):
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved '{src}' to '{dst}'")
    else:
        print(f"File '{src}' does not exist")


# Create necessary directories
create_directory(os.path.join(project_root, 'templates'))
create_directory(os.path.join(project_root, 'static'))
create_directory(os.path.join(project_root, 'static/css'))
create_directory(os.path.join(project_root, 'static/js'))
create_directory(os.path.join(project_root, 'static/img'))

# Move HTML files to templates directory
html_files = ['game.html', 'index.html', 'leaderboard.html', 'login.html']
for file in html_files:
    move_file(os.path.join(project_root, file), os.path.join(project_root, 'templates', file))

# Move CSS and JS files to static directory
move_file(os.path.join(project_root, 'style.css'), os.path.join(project_root, 'static/css/style.css'))
move_file(os.path.join(project_root, 'functions.js'), os.path.join(project_root, 'static/js/functions.js'))

# Move image files to static/img directory
image_directories = ['assets/img/mentors', 'assets/img/others']
for dir in image_directories:
    src_dir = os.path.join(project_root, dir)
    dst_dir = os.path.join(project_root, 'static/img', os.path.basename(dir))
    if os.path.exists(src_dir):
        shutil.move(src_dir, dst_dir)
        print(f"Moved '{src_dir}' to '{dst_dir}'")
    else:
        print(f"Directory '{src_dir}' does not exist")

print("Project restructuring complete.")
