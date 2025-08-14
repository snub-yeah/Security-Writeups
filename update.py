import os
import json
from datetime import datetime

def update_posts_json():
    json_file = 'posts.json'

    # read existing posts
    with open(json_file, 'r') as f:
        data = json.load(f)
        existing_posts = data['posts']

    # add date field to existing posts that don't have it
    for post in existing_posts:
        if 'date' not in post:
            # get the file path and add date from modification time
            file_path = post['path'].lstrip('/')  # remove leading slash for os.path
            if os.path.exists(file_path):
                mod_time = os.path.getmtime(file_path)
                post['date'] = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # get existing paths to avoid duplicates
    existing_paths = {post['path'] for post in existing_posts}


    base_path = '2025'
    next_id = max([post['id'] for post in existing_posts], default=0) + 1

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                # construct the full path relative to the root
                relative_path = os.path.join('/', root, file)
                relative_path = relative_path.replace('\\', '/')  # normalize path separators

                # if this path isn't in our existing posts, add it
                if relative_path not in existing_paths:
                    # extract title from filename (removing .md extension)
                    title = os.path.splitext(file)[0]
                    formatted_title = title.replace('_', ' ')

                    # get file modification time for date
                    full_file_path = os.path.join(root, file)
                    mod_time = os.path.getmtime(full_file_path)
                    file_date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

                    # create new post entry
                    new_post = {
                        "id": next_id,
                        "title": formatted_title,
                        "path": relative_path,
                        "date": file_date
                    }

                    existing_posts.append(new_post)
                    next_id += 1

    # sort posts by id
    data['posts'] = sorted(existing_posts, key=lambda x: x['id'])

    # write updated data back to file
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    update_posts_json()
