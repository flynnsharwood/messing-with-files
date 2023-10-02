import os
from bs4 import BeautifulSoup

def get_max_depth(html_file):
    with open(html_file, encoding="utf8") as f:
        soup = BeautifulSoup(f, 'html.parser')
        root_folder = soup.select_one("dt > h3")
        root_folder_name = root_folder.text.strip()
        folder_list = []
        md_string = ""

        # Check if there are any subfolders
        if root_folder.find_next_sibling('dl'):
            folder_list.append([root_folder_name])
            extract_links(soup, [root_folder_name], folder_list, md_string, 1)

        max_depth = max([len(f) - 1 for f in folder_list])
        md_string = f"# Folder: {root_folder_name}\n\n"

        for folder in folder_list:
            folder_name = " > ".join(folder)
            md_string += f"{'#' * (len(folder) + 1)} {folder_name}\n\n"

        return (f"Folder: {root_folder_name}, depth: {max_depth}", md_string, len(folder_list))

def extract_links(soup, folder_path, folder_list, md_string, depth):
    for link in soup.select('a'):
        href = link.get('href')
        name = link.string

        # Check if the link is a folder
        if href and href.startswith("http") == False:
            if href.endswith(".html") or href.endswith(".htm"):
                if depth > 5:
                    break
                with open(href, encoding="utf8") as f:
                    sub_soup = BeautifulSoup(f, 'html.parser')
                    subfolder = sub_soup.select_one("dt > h3")
                    if subfolder:
                        subfolder_name = subfolder.text.strip()
                        subfolder_path = folder_path + [subfolder_name]
                        folder_list.append(subfolder_path)
                        md_string += f"- [{' > '.join(subfolder_path)}]({href})\n"
                        extract_links(sub_soup, subfolder_path, folder_list, md_string, depth + 1)
                    else:
                        md_string += f"- [{name}]({href})\n"

    return md_string

if __name__ == "__main__":
    input_file = r"D:\Stuff\bookmarks.html"
    output_file = r"D:\Stuff\bookmarks.md"

    max_depth, md_string, num_bookmarks = get_max_depth(input_file)

    with open(output_file, 'w', encoding="utf8") as f:
        f.write(max_depth + "\n")
        f.write(md_string)

    with open(output_file, encoding="utf8") as f:
        print(f.read())

    print(f"Number of bookmarks: {num_bookmarks}")

