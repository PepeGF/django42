import sys
import os
import re

def check_arguments():
    if len(sys.argv) != 2:
        print("Usage: python render.py <settings.py>")
        sys.exit(1)
    if sys.argv[1].split(".")[-1] != "template":
        print("Error: template file must have a .template extension.")
        sys.exit(4)

def read_settings_file(settings_path: str) -> str:
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings_raw: str = f.read()
        return settings_raw
    except FileNotFoundError:
        print("Error: settings file not found.")
        sys.exit(4)
    except IOError as e:
        print(f"Error reading file '{settings_path}': {e}")
        sys.exit(4)

def settings_raw_to_dict(settings_raw: str) -> dict:
    # settings_raw is a string with lines like "key = value"
    settings_dict = {}
    for line in settings_raw.splitlines():
        if not line.strip():
            continue
        # Match lines like "key = value"
        match = re.match(r'(\w+)\s*=\s*(.+)', line)
        if match:
            key, value = match.groups()
            settings_dict[key] = value.strip('"').strip("'")
    return settings_dict

def read_template(template_path: str) -> str:
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Template file '{template_path}' not found.")
        sys.exit(2)
    except IOError as e:
        print(f"Error reading file '{template_path}': {e}")
        sys.exit(2)

def render_template(template: str, settings: dict) -> str:
    for key, value in settings.items():
        template = template.replace(f"{{{key}}}", value)
    return template

def main():
    check_arguments()
    settings_raw = read_settings_file("settings.py")
    settings = settings_raw_to_dict(settings_raw)
    template = read_template(sys.argv[1])
    rendered = render_template(template, settings)
    output_path = "file.html"
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered)
    except IOError as e:
        print(f"Error writing to file '{output_path}': {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()