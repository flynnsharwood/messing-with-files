import os
from bs4 import BeautifulSoup

def get_max_depth(html_file):
    with open(html_file, encoding="utf8") as f:
        soup = BeautifulSoup(f, 'html.parser')
        root_folder = soup.select_one("dt > h3")
        root_folder_name = root_folder.text.strip()
        folder_list = []

        # Check if there are any subfolders
        if root_folder.find_next_sibling('dl'):
            folder_list.append("- [" + root_folder_name + "](" + html_file + ")")
            extract_links(soup, [root_folder_name], folder_list)

        max_depth = max([len(f.split(os.sep)) for f in folder_list])
        return f"Folder: {root_folder_name}, depth: {max_depth - 1}"

def extract_links(soup, folder_path, folder_list):
    for link in soup.select('a'):
        href = link.get('href')
        name = link.string

        # Check if the link is a folder
        if href and href.startswith("http") == False:
            if href.endswith(".html") or href.endswith(".htm"):
                with open(href, encoding="utf8") as f:
                    sub_soup = BeautifulSoup(f, 'html.parser')
                    subfolder = sub_soup.select_one("dt > h3")
                    if subfolder:
                        subfolder_name = subfolder.text.strip()
                        subfolder_path = folder_path + [subfolder_name]
                        folder_list.append("- [" + " > ".join(subfolder_path) + "](" + href + ")")
                        extract_links(sub_soup, subfolder_path, folder_list)

if __name__ == "__main__":
    input_file = "bookmarks.html"
    output_file = r"D:\Stuff\bookmarks.md"
    
    max_depth = get_max_depth(input_file)

    with open(output_file, 'w', encoding="utf8") as f:
        f.write(max_depth + "\n")
        

    with open(output_file, encoding="utf8") as f:
        print(f.read())
