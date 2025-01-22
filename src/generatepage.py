import os
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Make sure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)
    
    # Loop through everything in the current directory
    for entry in os.listdir(dir_path_content):
        # Create full path for source
        src_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(src_path):
            # If it's a markdown file, process it
            if entry.endswith('.md'):
                # What should the output HTML file be named?
                html_file = entry.replace('.md', '.html')
                # Where should we put it?
                dest_path = os.path.join(dest_dir_path, html_file)
                # Generate the HTML page
                generate_page(src_path, template_path, dest_path)
        
        elif os.path.isdir(src_path):
            # If it's a directory, we need to:
            # 1. Create corresponding directory in dest_dir_path
            new_dest_dir = os.path.join(dest_dir_path, entry)
            # 2. Recursively process that directory
            generate_pages_recursive(src_path, template_path, new_dest_dir)

          
    
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#") and not line.startswith("##"):
            return "".join(line.split("#")).strip()
    raise Exception("No title found. Error.")